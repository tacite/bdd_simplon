from models.common_imports import Base, ForeignKey, Mapped, mapped_column

class Certification_Formation(Base):
    """
    ## Certification_Formation()

    Relationship table between certifications and formations.

    This table creates a many-to-many relationship between formations and certifications,
    using the certification codes and formation IDs as primary keys.

    Attributes:
        code_certification (Mapped[int]): Foreign key referencing the certification code in the 'certification' table.
        id_formation (Mapped[int]): Foreign key referencing the formation ID in the 'formation' table.
    """
    __tablename__ = "certification_formation"

    code_certification: Mapped[int] = mapped_column(ForeignKey("certification.code"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
        
class Nsf_Formation(Base):
    """
    ## Nsf_Formation()

    Relationship table between NSF (Nomenclature of Sciences and Formations) and formations.

    This table creates a many-to-many relationship between formations and NSF,
    using the NSF codes and formation IDs as primary keys.

    Attributes:
        code_nsf (Mapped[int]): Foreign key referencing the NSF code in the 'nsf' table.
        id_formation (Mapped[int]): Foreign key referencing the formation ID in the 'formation' table.
    """
    __tablename__ = "nsf_formation"
    
    code_nsf: Mapped[int] = mapped_column(ForeignKey("nsf.code"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
    
class Referentiel_Formation(Base):
    """
    ## Referentiel_Formation()

    Relationship table between referentials and formations.

    This table creates a many-to-many relationship between formations and referentials,
    using the referential IDs and formation IDs as primary keys.

    Attributes:
        id_referentiel (Mapped[int]): Foreign key referencing the referential ID in the 'referentiel' table.
        id_formation (Mapped[int]): Foreign key referencing the formation ID in the 'formation' table.
    """
    __tablename__ = "referentiel_formation"
    
    id_referentiel: Mapped[int] = mapped_column(ForeignKey("referentiel.id"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
    
class Referentiel_Formacode(Base):
    """
    ## Referentiel_Formacode()
    
    Relationship table between referentials and formacodes.

    This table creates a many-to-many relationship between referentials and formacodes,
    using the referential IDs and formacode codes as primary keys.

    Attributes:
        id_referentiel (Mapped[int]): Foreign key referencing the referential ID in the 'referentiel' table.
        code_formacode (Mapped[int]): Foreign key referencing the formacode code in the 'formacode' table.
    """
    __tablename__ = "referentiel_formacode"
    
    id_referentiel: Mapped[int] = mapped_column(ForeignKey("referentiel.id"), primary_key=True)
    code_formacode: Mapped[int] = mapped_column(ForeignKey("formacode.code"), primary_key=True)
