from common_imports import Base, Column, Integer, String, ForeignKey

class Rs_Formacode(Base):
    __tablename__ = "rs_formacode"
    
    code_rs = Column(Integer, ForeignKey("rs.code"))
    code_formacode = Column(String, ForeignKey("formacode.code"))