import sys
import os
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import sessionmaker, Session
import crud
import schemas
from models import *
from typing import List, Optional
from database import engine

# Ajouter le chemin du dossier `azurefunction` au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../azurefunction')))

# Maintenant, vous pouvez importer les modèles
from models.parents import Formation, Referentiel, Formacode, Nsf, Certification
from models.association_table import Nsf_Formation, Referentiel_Formacode, Certification_Formation, Referentiel_Formation

Session_db = sessionmaker(bind=engine, autoflush=False)

app = FastAPI()

# Dépendance pour obtenir une session de base de données
def get_db():
    """
    ## get_db()
     
    Dependency function to get a SQLAlchemy session.

    Yields:
        Session: A SQLAlchemy session.
    """
    db = Session_db()
    try:
        yield db
    finally:
        db.close()

@app.get("/source_info/{source_info}", response_model=schemas.FormationSource)
def read_source(source_info: str, db: Session = Depends(get_db)):
    """
    ## read_source()

    Retrieve formations based on the source information.

    Args:
        source_info (str): The source information to filter formations.
        db (Session): The SQLAlchemy session (injected by FastAPI).

    Returns:
        List[dict]: A list of formation details.

    Raises:
        HTTPException: If no formations are found for the given source information.
    """
    formations = crud.get_formation_by_source_info(db, source_info)
    if not formations:
        raise HTTPException(status_code=404, detail="Source not found")
    return formations

@app.get("/region/{region}", response_model=schemas.FormationSource)
def read_region(region: str, db: Session = Depends(get_db)):
    """
    ## read_region()

    Retrieve formations based on the region.

    Args:
        region (str): The region to filter formations.
        db (Session): The SQLAlchemy session (injected by FastAPI).

    Returns:
        dict: A dictionary containing the region and corresponding formations.

    Raises:
        HTTPException: If no formations are found for the given region.
    """
    regions = crud.get_formation_by_region(db, region)
    if regions is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return {"region": region}

@app.get("/formacode/{code}", response_model=schemas.FormationSource)
def read_formacode(code: str, db: Session = Depends(get_db)):
    """
    ## read_formacode()
    
    Retrieve formations based on the formacode.

    Args:
        code (str): The formacode to filter formations.
        db (Session): The SQLAlchemy session (injected by FastAPI).

    Returns:
        dict: A dictionary containing the formacode and corresponding formations.

    Raises:
        HTTPException: If no formations are found for the given formacode.
    """
    formacode = crud.get_formation_by_formacode(db, code)
    if formacode is None:
        raise HTTPException(status_code=404, detail="Formacode not found")
    return {"formacode": formacode}
