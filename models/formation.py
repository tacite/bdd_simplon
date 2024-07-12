from common_imports import String, Integer, Column, Date, Float, Boolean, Base, relationship

class Formation(Base):
    __tablename__ = "formation"
    
    id = Column(Integer, primary_key=True)
    titre = Column(String)
    date_debut = Column(Date)
    date_fin = Column(Date)
    duree_jours = Column(Integer)
    duree_heure = Column(Integer)
    region = Column(String)
    code_region = Column(String)
    ville = Column(String)
    niveau_sortie = Column(String)
    prix_mini = Column(Float)
    prix_max = Column(Float)
    handicap = Column(Boolean)
    source_info = Column(String)
    
    rs = relationship('RS', secondary="rs_formation")
    rncp = relationship('RNCP', secondary="rncp_formation")
    nsf = relationship('NSF', secondary="nsf_formation")
    certification = relationship('Certification', secondary="certification_formation")