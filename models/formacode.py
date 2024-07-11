from common_imports import String, Integer, Column, Base, relationship

class Formacode(Base):
    __tablename__ = "formacode"
    
    code = Column(Integer, primary_key=True)
    designation = Column(String)
    
    rs = relationship('RS', secondary="rs_formacode")
    rncp = relationship('RNCP', secondary='rncp_formacode')