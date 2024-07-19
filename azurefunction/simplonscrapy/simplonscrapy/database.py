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

#DATABASE_URL="postgresql+psycopg2://adminsadahe:sad@he@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"
DATABASE_URL = f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'

# Créer une instance d'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Créer une classe de base pour vos modèles
Base = declarative_base()

# Créer une instance de sessionmaker
Session = sessionmaker(bind=engine)

# Créer les tables dans la base de données
Base.metadata.create_all(engine)
