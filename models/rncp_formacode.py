from common_imports import Integer, Column, Base, ForeignKey

class Rncp_Formacode(Base):
    __tablename__ = "rncp_formacode"
    
    code_rncp = Column(Integer, ForeignKey('rncp.code'))
    code_formacode = Column(Integer, ForeignKey('formacode.code'))