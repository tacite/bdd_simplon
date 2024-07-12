from common_imports import String, Column, Base

class Certification(Base):
    __tablename__ = "certification"
    
    code = Column(String, primary_key=True)
    designation = Column(String)