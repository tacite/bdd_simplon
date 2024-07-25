from models.common_imports import Base, relationship, mapped_column, Mapped
from models.association_table import Certification_Formation, Nsf_Formation
from typing import Optional, List
from datetime import datetime

class Formation(Base):
    __tablename__ = "formation"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titre: Mapped[str]
    date_debut: Mapped[Optional[str]]
    duree_jours: Mapped[Optional[int]]
    duree_heures: Mapped[Optional[int]]
    region: Mapped[Optional[str]]
    code_region: Mapped[Optional[str]]
    ville: Mapped[Optional[str]]
    niveau_sortie: Mapped[Optional[str]]
    prix: Mapped[Optional[float]]
    source_info: Mapped[str]
    simplon_id: Mapped[Optional[int]]
    
    # many-to-many relationship to certification, bypassing the 'certification_formation' table
    certification: Mapped[List["Certification"]] = relationship(secondary="certification_formation", back_populates="formation")

    # many-to-many relationship to nsf, bypassing the 'nsf_formation' table
    nsf: Mapped[List["Nsf"]] = relationship(secondary="nsf_formation", back_populates='formation')

    referentiel: Mapped[List["Referentiel"]] = relationship(secondary="referentiel_formation", back_populates="formation")
        
class Certification(Base):
    __tablename__ = "certification"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]
    
    # many_to_many relationship to formation, bypassing the 'certification_formation' table
    formation: Mapped[List["Formation"]] = relationship(secondary="certification_formation", back_populates="certification")
        
class Nsf(Base):
    __tablename__ = "nsf"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]
    
    # many-to-many relationship to formation, bypassing the 'nsf_formation' table
    formation: Mapped[List["Formation"]] = relationship(secondary="nsf_formation", back_populates="nsf")

class Referentiel(Base):
    __tablename__ = "referentiel"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[int]
    type: Mapped[str]
    
    #many-to-many relationship to formation, bypassing the 'referentiel_formation' table
    formation: Mapped[List["Formation"]] = relationship(secondary="referentiel_formation", back_populates="referentiel")
    
    formacode: Mapped[List["Formacode"]] = relationship(secondary="referentiel_formacode", back_populates="referentiel")

class Formacode(Base):
    __tablename__ = "formacode"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]

    referentiel: Mapped[List["Referentiel"]] = relationship(secondary="referentiel_formacode", back_populates="formacode")
    