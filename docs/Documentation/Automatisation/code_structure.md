# Code Structure

Cette section contient les différentes parties de l'exécution de la fonction Azure.

### CSVtoPostgresDataPipeline

- **data**: ce dossier contient le fichier `V12_V13.xls`, qui liste les formacodes et leurs descriptions.
- **main.py**: ce fichier appelle les fichiers suivants :
    - **download_file.py**: récupère les formations de France Compétences au format CSV.
    - **fill_database.py**: crée les tables de la base de données SQL avec SQLAlchemy et les remplit.

### models

Ce dossier contient les fichiers de modélisation de la base de données :

- **parents.py**: modélise les tables.
- **common_imports.py**: se connecte à la base de données.
- **association_table.py**: définit la composition des tables d'association.

### simplonscrapy

Ce dossier contient toute la structure du framework Scrapy.

- **simplonscrapy**:
    - **spiders**: ce dossier contient le fichier de scraping **simplonspider.py**.
    - **database.py**: se connecte à la base de données.
    - **items.py**: définit les items à transférer dans la base de données.
    - **middlewares.py**: définit et configure les composants qui interceptent et modifient les requêtes et réponses tout au long du processus de scraping.
    - **pipelines.py**: nettoie les données et les charge dans la base de données.
    - **settings.py**: ajuste les paramètres de scraping.

### Fichiers supplémentaires

- **Dockerfile**: dockerise l'automatisation du scraping et du chargement de la base de données.
- **function_app.py**: script pour la fonction exécutée dans Azure qui automatise les tâches.
- **host.json**: fichier de configuration JSON pour `function_app`.
- **requirements.txt**: fichier de dépendances.
