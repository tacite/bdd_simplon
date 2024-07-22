from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from collections import OrderedDict
from typing import Optional
import sys
import os
import csv
from math import ceil

# Add the project root to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from models.parents import Formation, Certification, Formacode, Nsf, Referentiel
from models.common_imports import Base
from dotenv import load_dotenv
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion à la base de données depuis les variables d'environnement
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDATABASE = os.getenv('PGDATABASE')
username = "postgres"
password = ""
port = 5432
database = "postgres"
hostname = "localhost"

# fonction qui cherche dans la base de donnée si l'objet obj existe selon les filtres mis en arguments variadiques dans le kwargs
def exists(session: Session, obj: object, **kwargs) -> Optional['obj']:
    db_obj = session.scalar(select(obj).filter_by(**kwargs))
    if db_obj is not None:
        return db_obj
    else:
        return None


def fill_formacode(session: Session) -> None:

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
        
def fill_certification(row: OrderedDict, session: Session) -> Certification:
    certif = exists(session, Certification, code=row['code_certifinfo'])
    if not isinstance(certif, Certification):
        certif = Certification(code=row['code_certifinfo'], designation=row['intitule_certification'])
    return certif

def fill_nsf(row: OrderedDict, session: Session) -> Nsf:
    nsfs: list[Nsf] = []
    for number in range(1, 4):
        code = row[f"code_nsf_{number}"]
        if code:
            nsf = exists(session, Nsf, code=f"{code}")
            if not isinstance(nsf, Nsf):
                nsf = Nsf(code=row[f"code_nsf_{number}"], designation=row[f"libelle_nsf_{number}"])
            nsfs.append(nsf)
    return nsfs

def fill_formacodes(row: OrderedDict, session: Session) -> list[Formacode]:
    formacodes: list[Formacode] = []
    for number in range(1, 6):
        code = row[f"code_formacode_{number}"]
        if code:
            formacode = exists(session, Formacode, code=code)
            formacodes.append(formacode)
    return formacodes

def fill_referentiel(row: OrderedDict, session: Session) -> Referentiel:
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
    return referentiel

def fill_database() -> None:
    connection_string="postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"
    #connection_string = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
    engine = create_engine(connection_string)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    fill_formacode(session)
    
    with open('data/test.csv') as csv_file:
        for row in csv.DictReader(csv_file, delimiter=';'):
            heures = int(row['nombre_heures_total_mean'])
            jours = ceil(heures/8)
            formation = Formation(titre=row['intitule_formation'], region=row['nom_region'], code_region=row['code_region'],
                                niveau_sortie=row['libelle_niveau_sortie_formation'], source_info="france_competence",
                                duree_heures=heures, duree_jours=jours, prix=row['frais_ttc_tot_mean'])
            session.add(formation)
#            session.flush()
            certif = fill_certification(row, session)
            nsfs = fill_nsf(row, session)
            referentiel = fill_referentiel(row, session)
            formation.certification.append(certif)
            for nsf in nsfs:
                formation.nsf.append(nsf)
            formation.referentiel.append(referentiel)
            
        session.commit()
        session.close()
