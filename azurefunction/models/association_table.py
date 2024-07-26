from models.common_imports import Base, ForeignKey, Mapped, mapped_column

class Certification_Formation(Base):
    __tablename__ = "certification_formation"

    code_certification: Mapped[int] = mapped_column(ForeignKey("certification.code"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
        
class Nsf_Formation(Base):
    __tablename__ = "nsf_formation"
    
    code_nsf: Mapped[str] = mapped_column(ForeignKey("nsf.code"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
    
class Referentiel_Formation(Base):
    __tablename__ = "referentiel_formation"
    
    id_referentiel: Mapped[int] = mapped_column(ForeignKey("referentiel.id"), primary_key=True)
    id_formation: Mapped[int] = mapped_column(ForeignKey("formation.id"), primary_key=True)
    
class Referentiel_Formacode(Base):
    __tablename__ = "referentiel_formacode"
    
    id_referentiel: Mapped[int] = mapped_column(ForeignKey("referentiel.id"), primary_key=True)
    code_formacode: Mapped[int] = mapped_column(ForeignKey("formacode.code"), primary_key=True)