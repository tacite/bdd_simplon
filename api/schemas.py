from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class FormationSource(BaseModel):
    """
    ## class FormationSource()

Data model to represent training information.

Attributes:
    title (str): The title of the training.
    formacode_designation (Optional[str]): The designation of the formacode associated with the training.
    nsf_designation (Optional[str]): The designation of the NSF code associated with the training.
    rs_designation (Optional[str]): The designation of the RS code associated with the training.
    rncp_designation (Optional[str]): The designation of the RNCP code associated with the training.
    certification_designation (Optional[str]): The designation of the certification associated with the training.
    start_date (Optional[date]): The start date of the training.
    duration_days (Optional[int]): The duration of the training in days.
    duration_hours (Optional[int]): The duration of the training in hours.
    region (Optional[str]): The region where the training is conducted.
    region_code (Optional[str]): The code of the region where the training is conducted.
    city (Optional[str]): The city where the training is conducted.
    exit_level (Optional[str]): The exit level of the training.
    price (Optional[float]): The price of the training.
    source_info (Optional[str]): Additional information about the source of the training.
"""

    titre: str
    designation_formacode: Optional[str] = None
    designation_nsf: Optional[str] = None
    designation_rs: Optional[str] = None
    designation_rncp: Optional[str] = None
    designation_certification: Optional[str] = None
    date_debut: Optional[date] = None
    duree_jours: Optional[int] = None
    duree_heures: Optional[int] = None
    region: Optional[str] = None
    code_region: Optional[str] = None
    ville: Optional[str] = None
    niveau_sortie: Optional[str] = None
    prix: Optional[float] = None
    source_info: Optional[str] = None
