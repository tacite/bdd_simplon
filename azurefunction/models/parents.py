from models.common_imports import Base, relationship, mapped_column, Mapped
from models.association_table import Certification_Formation, Nsf_Formation
from typing import Optional, List
from datetime import datetime

class Formation(Base):
    """
    Représente une formation.

    Attributs:
        id (Mapped[int]): Identifiant unique de la formation.
        titre (Mapped[str]): Titre de la formation.
        date_debut (Mapped[Optional[datetime]]): Date de début de la formation (optionnelle).
        duree_jours (Mapped[Optional[int]]): Durée de la formation en jours (optionnelle).
        duree_heures (Mapped[Optional[int]]): Durée de la formation en heures (optionnelle).
        region (Mapped[str]): Région où la formation est dispensée.
        code_region (Mapped[str]): Code de la région.
        ville (Mapped[Optional[str]]): Ville où la formation est dispensée (optionnelle).
        niveau_sortie (Mapped[Optional[str]]): Niveau de sortie de la formation (optionnelle).
        prix (Mapped[Optional[float]]): Prix de la formation (optionnel).
        source_info (Mapped[str]): Source de l'information concernant la formation.

    Relations:
        certification (Mapped[List["Certification"]]): Relation many-to-many avec la table 'certification'.
        nsf (Mapped[List["Nsf"]]): Relation many-to-many avec la table 'nsf'.
        referentiel (Mapped[List["Referentiel"]]): Relation many-to-many avec la table 'referentiel'.
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
    
    # many-to-many relationship to certification, bypassing the 'certification_formation' table
    certification: Mapped[List["Certification"]] = relationship(secondary="certification_formation", back_populates="formation")

    # many-to-many relationship to nsf, bypassing the 'nsf_formation' table
    nsf: Mapped[List["Nsf"]] = relationship(secondary="nsf_formation", back_populates='formation')

    referentiel: Mapped[List["Referentiel"]] = relationship(secondary="referentiel_formation", back_populates="formation")
        
class Certification(Base):
    """
    Représente une certification.

    Attributs:
        code (Mapped[int]): Code unique de la certification.
        designation (Mapped[str]): Désignation de la certification.

    Relations:
        formation (Mapped[List["Formation"]]): Relation many-to-many avec la table 'formation'.
    """
    __tablename__ = "certification"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]
    
    # many-to-many relationship to formation, bypassing the 'certification_formation' table
    formation: Mapped[List["Formation"]] = relationship(secondary="certification_formation", back_populates="certification")
        
class Nsf(Base):
    """
    Représente une Nomenclature des Sciences et Formations (NSF).

    Attributs:
        code (Mapped[int]): Code unique de la NSF.
        designation (Mapped[str]): Désignation de la NSF.

    Relations:
        formation (Mapped[List["Formation"]]): Relation many-to-many avec la table 'formation'.
    """
    __tablename__ = "nsf"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]
    
    # many-to-many relationship to formation, bypassing the 'nsf_formation' table
    formation: Mapped[List["Formation"]] = relationship(secondary="nsf_formation", back_populates="nsf")

class Referentiel(Base):
    """
    Représente un référentiel.

    Attributs:
        id (Mapped[int]): Identifiant unique du référentiel.
        code (Mapped[int]): Code unique du référentiel.
        type (Mapped[str]): Type de référentiel (e.g., RNCP, Inventaire).

    Relations:
        formation (Mapped[List["Formation"]]): Relation many-to-many avec la table 'formation'.
        formacode (Mapped[List["Formacode"]]): Relation many-to-many avec la table 'formacode'.
    """
    __tablename__ = "referentiel"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[int]
    type: Mapped[str]
    
    # many-to-many relationship to formation, bypassing the 'referentiel_formation' table
    formation: Mapped[List["Formation"]] = relationship(secondary="referentiel_formation", back_populates="referentiel")
    
    formacode: Mapped[List["Formacode"]] = relationship(secondary="referentiel_formacode", back_populates="referentiel")

class Formacode(Base):
    """
    Représente un code de formation.

    Attributs:
        code (Mapped[int]): Code unique de la formation.
        designation (Mapped[str]): Désignation du code de formation.

    Relations:
        referentiel (Mapped[List["Referentiel"]]): Relation many-to-many avec la table 'referentiel'.
    """
    __tablename__ = "formacode"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    designation: Mapped[str]

    referentiel: Mapped[List["Referentiel"]] = relationship(secondary="referentiel_formacode", back_populates="formacode")
