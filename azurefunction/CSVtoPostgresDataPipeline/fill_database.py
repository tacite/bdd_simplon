import logging
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from collections import OrderedDict
from typing import Optional, List
import sys
import os
import csv
from math import ceil

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.parents import Formation, Certification, Formacode, Nsf, Referentiel
from models.common_imports import Base

# Informations de connexion à la base de données
username = "postgres"
password = ""
port = 5432
database = "postgres"
hostname = "localhost"

def exists(session: Session, obj: object, **kwargs) -> Optional[object]:
    """
    ## exists()

    Checks if an object exists in the database according to specified filters.

    Args:
        session (Session): The SQLAlchemy session used to interact with the database.
        obj (object): The SQLAlchemy model to query.
        **kwargs: Search filters as key-value pairs.

    Returns:
        Optional[object]: The found object if it exists, otherwise None.
    """
    db_obj = session.scalar(select(obj).filter_by(**kwargs))
    if db_obj is not None:
        return db_obj
    else:
        return None


def fill_formacode(session: Session) -> None:
    """
    ## fill_formacode()

    Fills the Formacode table with data from the CSV file.

    Args:
        session (Session): The SQLAlchemy session used to interact with the database.
    """
    logging.info('fill_formacode début')
    code_list = [str]    
    with open("data/V12_V13.xls", newline='', encoding='windows-1252') as file:
        toto = csv.reader(file, delimiter='\t')
        for row in toto:
            if row[3] and row[4]:
                if row[3] not in code_list:
                    formacode = Formacode(code=row[3], designation=row[4])
                    session.add(formacode)
                    code_list.append(row[3])
        session.commit()
    logging.info('fill_formacode fin')


def fill_certification(row: OrderedDict, session: Session) -> Certification:
    """
    ## fill_certification()

    Creates or retrieves a Certification instance based on the provided data.

    Args:
        row (OrderedDict): The CSV row data as a dictionary.
        session (Session): The SQLAlchemy session used to interact with the database.

    Returns:
        Certification: The created or retrieved Certification object.
    """
    logging.info('fill_certification début')
    certif = exists(session, Certification, code=row['code_certifinfo'])
    if not isinstance(certif, Certification):
        certif = Certification(code=row['code_certifinfo'], designation=row['intitule_certification'])
    logging.info('fill_certification fin')
    return certif

def fill_nsf(row: OrderedDict, session: Session) -> List[Nsf]:
    """
    ## fill_nsf()

    Creates or retrieves Nsf instances based on the provided data.

    Args:
        row (OrderedDict): The CSV row data as a dictionary.
        session (Session): The SQLAlchemy session used to interact with the database.

    Returns:
        List[Nsf]: The list of created or retrieved Nsf objects.
    """
    logging.info('fill_nsf début')
    nsfs: List[Nsf] = []
    for number in range(1, 4):
        code = row[f"code_nsf_{number}"]
        if code:
            nsf = exists(session, Nsf, code=f"{code}")
            if not isinstance(nsf, Nsf):
                nsf = Nsf(code=row[f"code_nsf_{number}"], designation=row[f"libelle_nsf_{number}"])
            nsfs.append(nsf)
    logging.info('fill_nsf fin')
    return nsfs

def fill_formacodes(row: OrderedDict, session: Session) -> List[Formacode]:
    """
    ## fill_formacodes()

    Creates or retrieves Formacode instances based on the provided data.

    Args:
        row (OrderedDict): The CSV row data as a dictionary.
        session (Session): The SQLAlchemy session used to interact with the database.

    Returns:
        List[Formacode]: The list of created or retrieved Formacode objects.
    """
    logging.info('fill_formacodes début')
    formacodes: List[Formacode] = []
    for number in range(1, 6):
        code = row[f"code_formacode_{number}"]
        if code:
            formacode = exists(session, Formacode, code=code)
            formacodes.append(formacode)
    logging.info('fill_formacodes fin')
    return formacodes

def fill_referentiel(row: OrderedDict, session: Session) -> Referentiel:
    """
    ## fill_referentiel()

    Creates or retrieves a Referentiel instance based on the provided data.

    Args:
        row (OrderedDict): The CSV row data as a dictionary.
        session (Session): The SQLAlchemy session used to interact with the database.

    Returns:
        Referentiel: The created or retrieved Referentiel object.
    """
    logging.info('fill_referentiel début')
    type_referentiel = row['type_referentiel']
    codec = ""
    match type_referentiel:
        case "RS":
            codec = row['code_inventaire']
        case "RNCP":
            codec = row['code_rncp']
    
    referentiel = exists(session, Referentiel, code=codec, type=type_referentiel) 
    if not isinstance(referentiel, Referentiel):
        referentiel = Referentiel(code=codec, type=type_referentiel)
        formacodes = fill_formacodes(row, session)
        for formacode in formacodes:
            referentiel.formacode.append(formacode)
        session.add(referentiel)
    logging.info('fill_referentiel fin')
    return referentiel

def fill_database() -> None:
    """
    ## fill_database() 
    
    Fills the database with data from the CSV file.

    This function connects to the database, clears existing tables, recreates the tables,
    and populates the tables with data from the CSV file.
    """
    logging.info('fill_database début')
    connection_string = "postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"
    # connection_string = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
    engine = create_engine(connection_string)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    fill_formacode(session)
    count = 0
    with open('test.csv') as csv_file:
        for row in csv.DictReader(csv_file, delimiter=';'):
            if count == 15000:
                session.commit()
                session.close()       
                exit()
            count += 1
            heures = int(row['nombre_heures_total_mean'])
            jours = ceil(heures / 8)
            formation = Formation(
                titre=row['intitule_formation'], 
                region=row['nom_region'], 
                code_region=row['code_region'],
                niveau_sortie=row['libelle_niveau_sortie_formation'], 
                source_info="france_competence",
                duree_heures=heures, 
                duree_jours=jours, 
                prix=row['frais_ttc_tot_mean']
            )
            session.add(formation)
            session.flush()
            certif = fill_certification(row, session)
            nsfs = fill_nsf(row, session)
            referentiel = fill_referentiel(row, session)
            formation.certification.append(certif)
            for nsf in nsfs:
                formation.nsf.append(nsf)
            formation.referentiel.append(referentiel)
            
        session.commit()
        session.close()
    logging.info('fill_database fin')


if __name__ == "__main__":
    fill_database()
