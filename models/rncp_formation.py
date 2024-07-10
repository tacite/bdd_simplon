from common_imports import Integer, Column, Base, ForeignKey

class Rncp_Formation(Base):
    __tablename__ = 'rncp_formation'
    
    code_rncp = Column(Integer, ForeignKey("rncp.code"))
    id_formation = Column(Integer, ForeignKey("formation.id"))