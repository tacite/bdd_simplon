# database.py

"""
Module de connexion à la base de données et de configuration des modèles SQLAlchemy.

Ce module se connecte à une base de données PostgreSQL en utilisant SQLAlchemy, charge les variables d'environnement 
pour les informations de connexion et configure les modèles de base de données.

Dépendances :
- sqlalchemy
- dotenv
- os
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion à la base de données depuis les variables d'environnement
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDATABASE = os.getenv('PGDATABASE')

print(f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}')
DATABASE_URL="postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"

# Créer une instance d'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Créer une classe de base pour vos modèles
Base = declarative_base()

# Créer une instance de sessionmaker
Session = sessionmaker(bind=engine)

# Créer les tables dans la base de données
Base.metadata.create_all(engine)
