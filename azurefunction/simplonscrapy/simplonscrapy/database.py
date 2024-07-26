# database.py

"""
Database connection and SQLAlchemy model configuration module.

This module connects to a PostgreSQL database using SQLAlchemy, loads environment variables
for connection information, and configures database models.

Dependencies:
- sqlalchemy
- dotenv
- os
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve database connection information from environment variables
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDATABASE = os.getenv('PGDATABASE')

print(f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}')
DATABASE_URL = "postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"

# Create a SQLAlchemy engine instance
engine = create_engine(DATABASE_URL)

# Create a base class for your models
Base = declarative_base()

# Create a sessionmaker instance
Session = sessionmaker(bind=engine)

# Create tables in the database
Base.metadata.create_all(engine)
