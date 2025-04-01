import json
import os

def resolve_refs(data, schemas):
    """Résout les références $ref dans un objet JSON."""
    if isinstance(data, dict):
        if "$ref" in data:
            ref = data["$ref"].split("/")[-1]
            if ref in schemas:
                return schemas[ref]
        return {k: resolve_refs(v, schemas) for k, v in data.items()}
    elif isinstance(data, list):
        return [resolve_refs(item, schemas) for item in data]
    else:
        return data

def generate_example_array(schema):
    """Génère un exemple de tableau JSON basé sur un schéma."""
    if schema.get('type') == 'array' and 'items' in schema:
        item_schema = schema['items']
        if item_schema.get('type') == 'object' and 'properties' in item_schema:
            example_object = {}
            for prop_name, prop_details in item_schema['properties'].items():
                if prop_details.get('type') == 'integer':
                    example_object[prop_name] = 123
                elif prop_details.get('type') == 'string':
                    example_object[prop_name] = "example"
                elif prop_details.get('type') == 'boolean':
                    example_object[prop_name] = True
                else:
                    example_object[prop_name] = None  # Valeur par défaut pour les autres types
            return [example_object, example_object]  # Génère un tableau avec deux exemples
    return []  # Retourne un tableau vide si le schéma n'est pas un tableau d'objets

def swagger_vers_postman(dossier_swagger, fichier_postman):
    """Convertit un dossier Swagger en une collection Postman avec les corps de requête et les réponses."""

    collection = {
        "info": {
            "_postman_id": "votre_id_unique",  # Générez un UUID unique
            "name": "Collection Swagger",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    # Charge les schémas
    schemas = {}
    dossier_schemas = os.path.join(dossier_swagger, 'components', 'schemas')
    if os.path.exists(dossier_schemas):
        for schema_file in os.listdir(dossier_schemas):
            if schema_file.endswith('.json'):
                schema_name = schema_file[:-5]
                schema_path = os.path.join(dossier_schemas, schema_file)
                with open(schema_path, 'r') as f:
                    schemas[schema_name] = json.load(f)

    # Parcours des chemins d'API
    dossier_paths = os.path.join(dossier_swagger, 'paths')
    if os.path.exists(dossier_paths):
        for path_folder in os.listdir(dossier_paths):
            chemin_details = os.path.join(dossier_paths, path_folder, 'details.json')
            if os.path.exists(chemin_details):
                with open(chemin_details, 'r') as f:
                    path_data = json.load(f)

                # Ajoute chaque opération (GET, POST, etc.) du chemin à la collection
                for method, operation in path_data.items():
                    request = {
                        "name": f"{method.upper()} {path_folder.replace('_', '/')}",
                        "request": {
                            "method": method.upper(),
                            "url": {
                                "raw": "{{base_url}}" + path_folder.replace('_', '/'),
                                "host": ["{{base_url}}"],
                                "path": path_folder.replace('_', '/').split('/')
                            },
                            "description": operation.get('description', '')
                        },
                        "response": []
                    }

                    # Ajoute le corps de la requête (si présent)
                    if 'requestBody' in operation and 'content' in operation['requestBody']:
                        content = operation['requestBody']['content']
                        for content_type, content_details in content.items():
                            if 'schema' in content_details:
                                schema = resolve_refs(content_details['schema'], schemas)
                                if schema.get('type') == 'array':
                                    example_array = generate_example_array(schema)
                                    request['request']['body'] = {
                                        "mode": "raw",
                                        "raw": json.dumps(example_array, indent=4),
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    }
                                else:
                                    request['request']['body'] = {
                                        "mode": "raw",
                                        "raw": json.dumps(schema, indent=4),
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    }

                                break  # Prend le premier type de contenu avec un schéma

                    # Ajoute les réponses à la requête
                    if 'responses' in operation:
                        for status_code, response_details in operation['responses'].items():
                            response = {
                                "name": f"Response {status_code}",
                                "code": int(status_code),
                                "status": response_details.get('description', ''),
                                "body": json.dumps(resolve_refs(response_details.get('content', {}), schemas), indent=4) if 'content' in response_details else ""
                            }
                            request['response'].append(response)

                    collection['item'].append(request)

    # Enregistre la collection Postman dans un fichier JSON
    with open(fichier_postman, 'w') as f:
        json.dump(collection, f, indent=4)

# Exemple d'utilisation
swagger_vers_postman('swagger_decoupe', 'collection_postman.json')
