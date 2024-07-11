from common_imports import Base, Column, Integer, String

class Rs(Base):
    __tablename__ = "rs"
    
    code = Column(Integer, primary_key=True)
    designation = Column(String)