
# Base de Données de Formations Simplon

## Description
Simplon souhaite créer une base de données pour comparer son offre de formations avec celles des autres centres de formation.
Cela permettra aux salariés de comprendre quelles formations subissent une forte concurrence et offrira aux potentiels apprenants des alternatives si les formations de Simplon sont complètes.

## Table des matières
1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Fonctionnalités](#fonctionnalités)
4. [Contribution](#contribution)
5. [Licence](#licence)
6. [Auteurs](#auteurs)
7. [Remerciements](#remerciements)

## Installation
Télécharger tout le projet en local.

### Prérequis
- Logiciels ou bibliothèques nécessaires : azure-functions / scrapy / sqlalchemy / python-dotenv / psycopg2-binary / fastapi / uvicorn
- Version de Python : 3.12.

### Étapes
1. Cloner le dépôt :
    ```bash
    git clone https://github.com/tacite/bdd_simplon.git
    ```
2. Naviguer dans le répertoire du projet :
    ```bash
    cd azure_resources
    ```
3. Installer les dépendances :
    ```bash
    chmos +x 1_azure_resources.sh
    ./1_azure_resources.sh
    ```

## Utilisation
Instructions sur comment utiliser le projet après l'installation. Inclure des exemples de code ou des commandes.

### Exemple
```bash
python main.py  # Pour exécuter le script principal
