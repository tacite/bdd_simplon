from common_imports import Integer, String, Column, Base, ForeignKey

class Nsf_Formation(Base):
    __tablename__ = "nsf_formation"
    
    code_nsf = Column(String, ForeignKey("nsf.code"))
    id_formation = Column(Integer, ForeignKey('formation.id'))