from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
from .database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_formations(
    skip: int = 0, 
    limit: int = 10, 
    source_info: Optional[str] = None, 
    region: Optional[str] = None, 
    formacode: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Formation)
    
    if source_info:
        query = query.filter(models.Formation.source_info == source_info)
    
    if region:
        query = query.filter(models.Formation.region == region)
    
    if formacode:
        query = query.filter(models.Formation.formacode == formacode)
    
    formations = query.offset(skip).limit(limit).all()
    return formations
