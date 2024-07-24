# Documentation Database Simplon

## Introduction

This programm create a database to compare its training programs with those of other training centers.

To achieve this, the program retrieves training courses from the France Compétences website through its API. Then, the program scrapes the Simplon website to gather information on training courses currently being offered.

The API allows querying the created database to find the sought training courses based on the information source (Simplon or France Compétences), the region where the training takes place, and the formacodes.

## Code Structure

- **azure_resources**:
    - ***1_azure_resources.sh***: crée les ressources Azure.
    - ***delete_resources.sh***: supprime les ressources Azure.
- **azurefunction**: ce dossier contient les différentes parties d'exécussion de la function azure.
    - **CSVtoPostgresDataPipeline**:
        - **data**: ce dossier contient le fichier V12_V13.xls, liste des formacodes et leur désignation.
        - ***main.py***: ce fichier appelle les fichiers:
            - ***download_file.py***: récupère les formations de France Compétences sous forme de csv.
            - ***fill_database.py***: crée les tables de la base de données SQL avec la bibliothèque SQLAlchemy et remplit les tables.
    - **models**: ce dossier contient les fichiers de modélisation de la base de données:
        - ***parents.py***: modélisation des tables.
        - ***common_imports.py***: connexion à la base de données.
        - ***assiciation_table.py***: composition des tables d'association
    - **simplonscrapy**: ce dossier contient toute la structure du framework Scrapy.
        - **simplonscrapy**:
            - **spiders**: ce dossier contient le fichier de scrapping ***somplonspider.py***.
            - ***database.py***: connexion à la base de données.
            - ***items.py***: définition des items qui vont être trasférés dans la base de données.
            - ***middlewares.py***: définit et configure les composants qui permettent d'intercepter et de modifier les requêtes et les réponses tout au long du processus de scraping.
            - ***pipelines.py***: nettoyage des données et mise en base de données.
            - ***settings.py***: ajustement des paramétrage de scraping.
    - ***Dockerfile***: dockerisation de l'automatisation du scraping et de la mise en base de données.
    - ***function_app.py***: script de la fonction qui tourne dans Azure et qui automatise les tâches.
    - ***host.json***: json de configuration de function_app.
    - ***requirements.txt***: fichier des dépendances.
- **bdd_structure***: ce dossier contient les schémas de la base de données.

### Authentification


## Endpoints
