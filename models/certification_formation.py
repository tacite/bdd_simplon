from common_imports import String, Integer, Base, Column, ForeignKey

class Certification_Formation(Base):
    __tablename__ = "certification_formation"
    
    code_certification = Column(String, ForeignKey("certification.code"))
    id_formation = Column(Integer, ForeignKey("formation.id"))
    