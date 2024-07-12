from common_imports import String, Integer, Column, Base

class Rncp(Base):
    __tablename__ = "rncp"
    
    Code = Column(Integer, primary_key=True)
    designation = Column(String)