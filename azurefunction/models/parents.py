from models.common_imports import Base, relationship, mapped_column, Mapped
from models.association_table import Certification_Formation, Nsf_Formation
from typing import Optional, List
from datetime import datetime

class Formation(Base):
    """
    ## Formation()

    Represents a training course.

    Attributes:
        id (Mapped[int]): Unique identifier for the training course.
        titre (Mapped[str]): Title of the training course.
        date_debut (Mapped[Optional[datetime]]): Start date of the training course (optional).
        duree_jours (Mapped[Optional[int]]): Duration of the training course in days (optional).
        duree_heures (Mapped[Optional[int]]): Duration of the training course in hours (optional).
        region (Mapped[str]): Region where the training course is conducted.
        code_region (Mapped[str]): Code of the region.
        ville (Mapped[Optional[str]]): City where the training course is conducted (optional).
        niveau_sortie (Mapped[Optional[str]]): Level upon completion of the training course (optional).
        prix (Mapped[Optional[float]]): Price of the training course (optional).
        source_info (Mapped[str]): Source of information about the training course.

    Relationships:
        certification (Mapped[List["Certification"]]): Many-to-many relationship with the 'certification' table.
        nsf (Mapped[List["Nsf"]]): Many-to-many relationship with the 'nsf' table.
        referentiel (Mapped[List["Referentiel"]]): Many-to-many relationship with the 'referentiel' table.
    """
    __tablename__ = "formation"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titre: Mapped[str]
    date_debut: Mapped[Optional[datetime]]
    duree_jours: Mapped[Optional[int]]
    duree_heures: Mapped[Optional[int]]
    region: Mapped[str]
    code_region: Mapped[str]
    ville: Mapped[Optional[str]]
    niveau_sortie: Mapped[Optional[str]]
    prix: Mapped[Optional[float]]
    source_info: Mapped[str]
    
    # Relation many-to-many avec la table 'certification'
    certification: Mapped[List["Certification"]] = relationship(secondary="certification_formation", back_populates="formation")

    # Relation many-to-many avec la table 'nsf'
    nsf: Mapped[List["Nsf"]] = relationship(secondary="nsf_formation", back_populates='formation')

    referentiel: Mapped[List["Referentiel"]] = relationship(secondary="referentiel_formation", back_populates="formation")
        
class Certification(Base):
    """
    ## Certification()

    Represents a certification.

    Attributes:
        code (Mapped[int]): Unique code of the certification.
        designation (Mapped[str]): Designation of the certification.

    Relationships:
        formation (Mapped[List["Formation"]]): Many-to-many relationship with the 'formation' table.
    """
    __tablename__ = "certification"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]
    
    # Relation many-to-many avec la table 'formation'
    formation: Mapped[List["Formation"]] = relationship(secondary="certification_formation", back_populates="certification")
        
class Nsf(Base):
    """
    ## Nsf()

    Represents a Nomenclature of Sciences and Formations (NSF).

    Attributes:
        code (Mapped[int]): Unique code of the NSF.
        designation (Mapped[str]): Designation of the NSF.

    Relationships:
        formation (Mapped[List["Formation"]]): Many-to-many relationship with the 'formation' table.
    """
    __tablename__ = "nsf"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]
    
    # Relation many-to-many avec la table 'formation'
    formation: Mapped[List["Formation"]] = relationship(secondary="nsf_formation", back_populates="nsf")

class Referentiel(Base):
    """
    ## Referentiel()

    Represents a referential.

    Attributes:
        id (Mapped[int]): Unique identifier for the referential.
        code (Mapped[int]): Unique code of the referential.
        type (Mapped[str]): Type of referential (e.g., RNCP, Inventory).

    Relationships:
        formation (Mapped[List["Formation"]]): Many-to-many relationship with the 'formation' table.
        formacode (Mapped[List["Formacode"]]): Many-to-many relationship with the 'formacode' table.
    """
    __tablename__ = "referentiel"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[int]
    type: Mapped[str]
    
    # Relation many-to-many avec la table 'formation'
    formation: Mapped[List["Formation"]] = relationship(secondary="referentiel_formation", back_populates="referentiel")
    
    formacode: Mapped[List["Formacode"]] = relationship(secondary="referentiel_formacode", back_populates="referentiel")

class Formacode(Base):
    """
    ## Formacode()
    
    Represents a training code.

    Attributes:
        code (Mapped[int]): Unique code of the training.
        designation (Mapped[str]): Designation of the training code.

    Relationships:
        referentiel (Mapped[List["Referentiel"]]): Many-to-many relationship with the 'referentiel' table.
    """
    __tablename__ = "formacode"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]

    referentiel: Mapped[List["Referentiel"]] = relationship(secondary="referentiel_formacode", back_populates="formacode")
