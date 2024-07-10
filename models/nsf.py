from common_imports import String, Column, Base

class Nsf(Base):
    __tablename__ = "nsf"
    
    code = Column(String, primary_key=True)
    designation = Column(String)