from common_imports import Integer, Column, Base, ForeignKey

class Rs_Formation(Base):
    __tablename__ = "rs_formation"
    
    code_rs = Column(Integer, ForeignKey("rs.code"))
    id_formation = Column(Integer, ForeignKey("formation.id"))