from models.common_imports import Base, ForeignKey, Mapped, mapped_column

class Certification_Formation(Base):
    """
    Table de relation entre les certifications et les formations.

    Cette table crée une relation many-to-many entre les formations et les certifications,
    en utilisant les identifiants des certifications et des formations comme clés primaires.

    Attributs:
        code_certification (Mapped[int]): Clé étrangère référencant le code de la certification dans la table 'certification'.
        id_formation (Mapped[int]): Clé étrangère référencant l'identifiant de la formation dans la table 'formation'.
    """
    __tablename__ = "certification_formation"

    code_certification: Mapped[int] = mapped_column(ForeignKey("certification.code"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
        
class Nsf_Formation(Base):
    """
    Table de relation entre les NSF (Nomenclature des Sciences et Formations) et les formations.

    Cette table crée une relation many-to-many entre les formations et les NSF,
    en utilisant les codes NSF et les identifiants de formation comme clés primaires.

    Attributs:
        code_nsf (Mapped[int]): Clé étrangère référencant le code NSF dans la table 'nsf'.
        id_formation (Mapped[int]): Clé étrangère référencant l'identifiant de la formation dans la table 'formation'.
    """
    __tablename__ = "nsf_formation"
    
    code_nsf: Mapped[int] = mapped_column(ForeignKey("nsf.code"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
    
class Referentiel_Formation(Base):
    """
    Table de relation entre les référentiels et les formations.

    Cette table crée une relation many-to-many entre les formations et les référentiels,
    en utilisant les identifiants de référentiel et de formation comme clés primaires.

    Attributs:
        id_referentiel (Mapped[int]): Clé étrangère référencant l'identifiant du référentiel dans la table 'referentiel'.
        id_formation (Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
    """
    __tablename__ = "referentiel_formation"
    
    id_referentiel: Mapped[int] = mapped_column(ForeignKey("referentiel.id"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
    
class Referentiel_Formacode(Base):
    """
    Table de relation entre les référentiels et les formacodes.

    Cette table crée une relation many-to-many entre les référentiels et les formacodes,
    en utilisant les identifiants de référentiel et les codes formacodes comme clés primaires.

    Attributs:
        id_referentiel (Mapped[int]): Clé étrangère référencant l'identifiant du référentiel dans la table 'referentiel'.
        code_formacode (Mapped[int]): Clé étrangère référencant le code formacode dans la table 'formacode'.
    """
    __tablename__ = "referentiel_formacode"
    
    id_referentiel: Mapped[int] = mapped_column(ForeignKey("referentiel.id"), primary_key=True)
    code_formacode: Mapped[int] = mapped_column(ForeignKey("formacode.code"), primary_key=True)
