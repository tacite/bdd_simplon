import logging
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from collections import OrderedDict
from typing import Optional
import sys
import os
import csv
from math import ceil

# Add the project root to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.parents import Formation, Certification, Formacode, Nsf, Referentiel
from models.common_imports import Base

# Retrieve database connection information from environment variables
username = "postgres"
password = ""
port = 5432
database = "postgres"
hostname = "localhost"

def exists(session: Session, obj: object, **kwargs) -> Optional['obj']:
    """
    Check if an object exists in the database based on given filters.

    Parameters:
    session (Session): The SQLAlchemy session to use for the query.
    obj (object): The model class to query.
    kwargs: Filter arguments for the query.

    Returns:
    obj or None: The found object or None if it does not exist.
    """
    db_obj = session.scalar(select(obj).filter_by(**kwargs))
    if db_obj is not None:
        return db_obj
    else:
        return None


def fill_formacode(session: Session) -> None:
    """
    Fill the Formacode table from a CSV file.

    Parameters:
    session (Session): The SQLAlchemy session to use for database operations.

    Returns:
    None
    """
    logging.info('fill_formacode start')
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
    logging.info('fill_formacode end')

        
def fill_certification(row: OrderedDict, session: Session) -> Certification:
    """
    Fill the Certification table based on the data from a CSV row.

    Parameters:
    row (OrderedDict): The data row from the CSV file.
    session (Session): The SQLAlchemy session to use for database operations.

    Returns:
    Certification: The Certification object created or retrieved from the database.
    """
    logging.info('fill_certification start')

    certif = exists(session, Certification, code=row['code_certifinfo'])
    if not isinstance(certif, Certification):
        certif = Certification(code=row['code_certifinfo'], designation=row['intitule_certification'])
    logging.info('fill_certification end')

    return certif

def fill_nsf(row: OrderedDict, session: Session) -> list[Nsf]:
    """
    Fill the NSF table based on the data from a CSV row.

    Parameters:
    row (OrderedDict): The data row from the CSV file.
    session (Session): The SQLAlchemy session to use for database operations.

    Returns:
    list[Nsf]: A list of NSF objects created or retrieved from the database.
    """
    logging.info('fill_nsf start')

    nsfs: list[Nsf] = []
    for number in range(1, 4):
        code = row[f"code_nsf_{number}"]
        if code:
            nsf = exists(session, Nsf, code=f"{code}")
            if not isinstance(nsf, Nsf):
                nsf = Nsf(code=row[f"code_nsf_{number}"], designation=row[f"libelle_nsf_{number}"])
            nsfs.append(nsf)
    logging.info('fill_nsf end')

    return nsfs

def fill_formacodes(row: OrderedDict, session: Session) -> list[Formacode]:
    """
    Fill the Formacode table based on the data from a CSV row.

    Parameters:
    row (OrderedDict): The data row from the CSV file.
    session (Session): The SQLAlchemy session to use for database operations.

    Returns:
    list[Formacode]: A list of Formacode objects retrieved from the database.
    """
    logging.info('fill_formacodes start')

    formacodes: list[Formacode] = []
    for number in range(1, 6):
        code = row[f"code_formacode_{number}"]
        if code:
            formacode = exists(session, Formacode, code=code)
            formacodes.append(formacode)
    logging.info('fill_formacodes end')

    return formacodes

def fill_referentiel(row: OrderedDict, session: Session) -> Referentiel:
    """
    Fill the Referentiel table based on the data from a CSV row.

    Parameters:
    row (OrderedDict): The data row from the CSV file.
    session (Session): The SQLAlchemy session to use for database operations.

    Returns:
    Referentiel: The Referentiel object created or retrieved from the database.
    """
    logging.info('fill_referentiel start')

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
    logging.info('fill_referentiel end')

    return referentiel

def fill_database() -> None:
    """
    Fill the database with data from a CSV file.

    The function connects to the database, drops all existing tables, creates new tables,
    and populates them with data from a CSV file.

    Parameters:
    None

    Returns:
    None
    """
    logging.info('fill_database start')

    connection_string="postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"
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
            if count == 3000:
                session.commit()
                session.close()       
                exit()
            count += 1
            heures = int(row['nombre_heures_total_mean'])
            jours = ceil(heures/8)
            formation = Formation(titre=row['intitule_formation'], region=row['nom_region'], code_region=row['code_region'],
                                niveau_sortie=row['libelle_niveau_sortie_formation'], source_info="france_competence",
                                duree_heures=heures, duree_jours=jours, prix=row['frais_ttc_tot_mean'])
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
    logging.info('fill_database end')


if __name__ == "__main__":
    """
    Main entry point of the script. Calls the fill_database function to fill the
    database with data from the CSV file.
    """
    fill_database()
