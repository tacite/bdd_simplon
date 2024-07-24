from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class FormationSource(BaseModel):
    titre: str
    designation_formacode: Optional[str]= None
    designation_nsf: Optional[str]= None
    designation_rs: Optional[str]= None
    designation_rncp: Optional[str]= None
    designation_certification: Optional[str]= None
    date_debut: Optional[date]= None
    duree_jours: Optional[int]= None
    duree_heures: Optional[int]= None
    region: Optional[str]= None
    code_region: Optional[str]= None
    ville: Optional[str]= None
    niveau_sortie: Optional[str]= None
    prix: Optional[float]= None
    source_info: Optional[str]= None
