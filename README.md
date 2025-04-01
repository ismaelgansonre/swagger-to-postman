# swagger-to-postman

# Conversion de Swagger volumineux en collection Postman

## Introduction

Ce projet a été développé pour résoudre un problème rencontré lors de la gestion d'un fichier Swagger extrêmement volumineux, dépassant les 150 000 lignes. La taille du fichier rendait difficile son traitement direct dans des outils comme Postman, entraînant des problèmes de performance et de manipulation.

L'objectif principal de ce projet est de découper ce fichier Swagger massif en une structure plus gérable, puis de le convertir en une collection Postman pour faciliter les tests et l'exploration de l'API.

## Découpage du fichier Swagger

Le script Python `decouper_swagger.py` est utilisé pour découper le fichier Swagger en sections plus petites, organisées dans des sous-dossiers. Chaque sous-dossier représente un groupe logique d'API ou de composants, ce qui rend le fichier Swagger plus facile à naviguer et à gérer.

### Utilisation

1.  Placez votre fichier Swagger (au format JSON) dans le même répertoire que le script.
2.  Exécutez le script : `python decouper_swagger.py votre_fichier_swagger.json dossier_sortie`
    * Remplacez `votre_fichier_swagger.json` par le nom de votre fichier Swagger.
    * Remplacez `dossier_sortie` par le nom du dossier où vous souhaitez enregistrer les fichiers découpés.

## Conversion en collection Postman

Le script Python `swagger_vers_postman.py` est utilisé pour convertir les fichiers Swagger découpés en une collection Postman. La collection Postman générée contient toutes les requêtes d'API, les corps de requête et les réponses définies dans le fichier Swagger.

### Utilisation

1.  Assurez-vous que les fichiers Swagger ont été découpés en utilisant le script `decouper_swagger.py`.
2.  Exécutez le script : `python swagger_vers_postman.py dossier_swagger fichier_postman.json`
    * Remplacez `dossier_swagger` par le nom du dossier contenant les fichiers Swagger découpés.
    * Remplacez `fichier_postman.json` par le nom du fichier où vous souhaitez enregistrer la collection Postman.
3.  Importez le fichier `fichier_postman.json` dans Postman.

## Dépendances

* Python 3
* Bibliothèque `json` (incluse dans la bibliothèque standard de Python)
* Bibliothèque `os` (incluse dans la bibliothèque standard de Python)

## Améliorations possibles

* Gestion des schémas complexes : Extraire et inclure les schémas complexes dans la collection Postman pour une meilleure documentation.
* Gestion des types de contenu : Gérer tous les types de contenu définis dans le fichier Swagger (XML, texte, etc.).
* Tests automatisés : Générer des tests automatisés Postman à partir des schémas Swagger.

## Conclusion

Ce projet fournit une solution pour gérer efficacement les fichiers Swagger volumineux en les découpant et en les convertissant en collections Postman. Cela facilite les tests et l'exploration des API, ce qui permet de gagner du temps et d'améliorer la productivité.
