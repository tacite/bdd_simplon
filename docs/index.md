# Database for Simplon

## Purpose

The objective of this project is to provide a database for Simplon. 

Simplon wants to create a database to compare its training programs with those of other training centers. This will enable employees to understand which training programs face strong competition and provide potential learners with alternatives if Simplon's programs are full.

## Dependencies:
- poetry
- psycopg2-binary
- python-dotenv
- scrapy
- SQLAlchemy
- azure CLI
- azure ml CLI
- psql
- fastapi
- mkdocstrings-python

## Setup

1. Create virtual environement and install requierements:

```bash

poetry install

```

2. Create .env file using env_template.txt


3. To create the Azure ressources, execute these tasks:

- open the file ./azure_resources/1_azure_resources
- in the section ___VARIABLES___, choose your own designations for the resources
- execute these commands:

```bash
chmod +x ./azure_resources/1_azure_resources.sh
./azure_resources/1_azure_resources.sh
```

4. Check the resources and execution of the function on the Azure portal


## Launch the API

1. Get your token:

```bash
poetry run python -m api.utils
```

2. Update model_name in ./api/launch_app.sh and then you can execute it
