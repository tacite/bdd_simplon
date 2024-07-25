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

    Vérifie si un objet existe dans la base de données selon les filtres spécifiés.

    Args:
        session (Session): La session SQLAlchemy utilisée pour interagir avec la base de données.
        obj (object): Le modèle SQLAlchemy à interroger.
        **kwargs: Les filtres de recherche sous forme de paires clé-valeur.

    Returns:
        Optional[object]: L'objet trouvé s'il existe, sinon None.
    """
    db_obj = session.scalar(select(obj).filter_by(**kwargs))
    if db_obj is not None:
        return db_obj
    else:
        return None


def fill_formacode(session: Session) -> None:
    """
    Remplit la table Formacode avec les données du fichier CSV.

    Args:
        session (Session): La session SQLAlchemy utilisée pour interagir avec la base de données.
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
    Crée ou récupère une instance de Certification basée sur les données fournies.

    Args:
        row (OrderedDict): Les données de la ligne du fichier CSV sous forme de dictionnaire.
        session (Session): La session SQLAlchemy utilisée pour interagir avec la base de données.

    Returns:
        Certification: L'objet Certification créé ou récupéré.
    """
    logging.info('fill_certification début')
    certif = exists(session, Certification, code=row['code_certifinfo'])
    if not isinstance(certif, Certification):
        certif = Certification(code=row['code_certifinfo'], designation=row['intitule_certification'])
    logging.info('fill_certification fin')
    return certif

def fill_nsf(row: OrderedDict, session: Session) -> List[Nsf]:
    """
    Crée ou récupère les instances de Nsf basées sur les données fournies.

    Args:
        row (OrderedDict): Les données de la ligne du fichier CSV sous forme de dictionnaire.
        session (Session): La session SQLAlchemy utilisée pour interagir avec la base de données.

    Returns:
        List[Nsf]: La liste des objets Nsf créés ou récupérés.
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
    Crée ou récupère les instances de Formacode basées sur les données fournies.

    Args:
        row (OrderedDict): Les données de la ligne du fichier CSV sous forme de dictionnaire.
        session (Session): La session SQLAlchemy utilisée pour interagir avec la base de données.

    Returns:
        List[Formacode]: La liste des objets Formacode créés ou récupérés.
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
    Crée ou récupère une instance de Referentiel basée sur les données fournies.

    Args:
        row (OrderedDict): Les données de la ligne du fichier CSV sous forme de dictionnaire.
        session (Session): La session SQLAlchemy utilisée pour interagir avec la base de données.

    Returns:
        Referentiel: L'objet Referentiel créé ou récupéré.
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
    Remplit la base de données avec les données provenant du fichier CSV.

    Cette fonction se connecte à la base de données, vide les tables existantes, recrée les tables et remplit
    les tables avec les données du fichier CSV.
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
