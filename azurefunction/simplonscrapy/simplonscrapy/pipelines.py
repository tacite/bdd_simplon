# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import sys
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from .database import engine, Session
# Add the project root to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from models.parents import Formation, Formacode, Nsf, Referentiel
import re


class SimplonscrapyPipeline:
    def __init__(self):
        # Créer une session SQLAlchemy
        self.Session = sessionmaker(bind=engine)
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Nettoyer les données
        item = self.clean_rncp(item)
        item = self.clean_rs(item)
        item = self.clean_formation_id(item)
        item = self.clean_niveau_sortie(item)
        item = self.clean_prix(item)
        item = self.clean_region(item)
        item = self.clean_start_date(item)
        item = self.clean_duree(item)
        # item = self.clean_type_formation(item)
        item = self.clean_lieu_formation(item)
        item = self.clean_formacodes(item)
        item = self.clean_nsf_codes(item)

        # Insérer les données dans la base de données
        session = self.Session()
        formation = Formation(
            titre=adapter.get('titre'),
            formation_id=adapter.get('formation_id'),
            niveau_sortie=adapter.get('niveau_sortie'),
            prix=adapter.get('prix'),
            # prix_min=adapter.get('prix_min'),
            # prix_max=adapter.get('prix_max'),
            region=adapter.get('region'),
            date_debut=adapter.get('date_debut'),
            duree_jours=adapter.get('duree_jours'),
            # type_formation=adapter.get('type_formation'),
            ville=adapter.get('ville'),
            formacodes=adapter.get('formacodes'),
        )
        session.add(formation)
        session.commit()

        # Récupérer les nsf_codes
        nsf_codes=adapter.get('nsf_codes')
        for nsf_code in nsf_codes:
            existe_nsf_code=self.session.query(Nsf).filter_by(code=nsf_code).first()
            if not existe_nsf_code:
                existe_nsf_code=Nsf(code=nsf_code)
                self.session.add(existe_nsf_code)
            formation.nsf_codes.append(existe_nsf_code)

        # Récupérer les referentiels
        rncp=adapter.get('rncp'),
        for r in rncp:
            existe_rncp=self.session.query(Referentiel).filter_by(type=r).first()
            if not existe_rncp:
                existe_rncp=Referentiel(type=r)
                self.session.add(existe_rncp)
            formation.referentiel.append(existe_rncp)

        rs=adapter.get('rs'),
        for r in rs:
            existe_rs=self.session.query(Referentiel).filter_by(type=r).first()
            if not  existe_rs:
                existe_rs=Referentiel(type=r)
                self.session.add(existe_rs)
            formation.referentiel.append(existe_rs)

        # Récupérer les Formacodes
        formacodes=adapter.get('formacodes')
        for formacode in formacodes:
            existe_formacode=self.session.query(Formacode).filter_by(code=formacode).first()
            if not existe_formacode:
                existe_formacode=Formacode(code=formacode)
                self.session.add(existe_formacode)
            formacodes.append(existe_formacode)


        session.close()

        return item
    
    def clean_rncp(self, item):
        adapter = ItemAdapter(item)
        rncp = adapter.get("rncp")
        if rncp:
            # Extraire uniquement les chiffres du rncp
            rncp_numbers = ''.join(re.findall(r'\d+', rncp))
            adapter['rncp'] = rncp_numbers if rncp_numbers else None
        else:
            adapter['rncp'] = None
        return item

    def clean_rs(self, item):
        adapter = ItemAdapter(item)
        rs = adapter.get("rs")
        if rs:
            segments = rs.split('/')
            if len(segments) > 2:
                rs_id = segments[-2]
                adapter['rs'] = rs_id
            else:
                adapter['rs'] = rs  
        else:
            adapter['rs'] = None
        return item    

    def clean_formation_id(self,item):
        adapter=ItemAdapter(item)
        formation_id=adapter.get("formation_id")
        if formation_id:
            formation_id = formation_id.split('/')[-1]
            adapter['formation_id'] = formation_id
        return item

    def clean_niveau_sortie(self,item):
        adapter=ItemAdapter(item)
        niveau_sortie=adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item

    # def clean_prix(self,item):
    #     adapter = ItemAdapter(item)
    #     prix_min = adapter.get("prix_min")
    #     prix_max = adapter.get("prix_max")
    #     if prix_min:
    #         adapter['prix_min'] = ''.join(filter(str.isdigit, prix_min))
    #     if prix_max:
    #         adapter['prix_max'] = ''.join(filter(str.isdigit, prix_max))
    #     prix = (prix_max-prix_min)/2
    #     adapter['prix'] = prix
    #     return item
    def clean_prix(self, item):
        adapter = ItemAdapter(item)
        prix_min = adapter.get("prix_min")
        prix_max = adapter.get("prix_max")

        # Nettoyer et extraire les chiffres des prix min et max
        if prix_min:
            prix_min = ''.join(filter(str.isdigit, prix_min))
            if prix_min.isdigit():
                prix_min = float(prix_min)
            else:
                prix_min = None
        if prix_max:
            prix_max = ''.join(filter(str.isdigit, prix_max))
            if prix_max.isdigit():
                prix_max = float(prix_max)
            else:
                prix_max = None

        # Mettre à jour l'adapter avec les valeurs nettoyées
        adapter['prix_min'] = prix_min
        adapter['prix_max'] = prix_max

        # Calculer la moyenne du prix si les deux valeurs sont présentes
        if prix_min is not None and prix_max is not None:
            prix = (prix_max + prix_min) / 2
        else:
            prix = None

        adapter['prix'] = prix

        return item


    def clean_region(self,item):
        adapter = ItemAdapter(item)
        region = adapter.get("region")
        if region:
            adapter['region'] = adapter['region'].replace('\n', '').strip()
        return item
    
    
    def clean_start_date(self,item):
        adapter = ItemAdapter(item)
        date_debut = adapter.get("date_debut")
        if date_debut:
            adapter['date_debut'] = adapter['date_debut'].replace('\n', '').strip()
        return item

    def clean_niveau_sortie(self, item):
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item
    
    def clean_duree(self,item):
        adapter = ItemAdapter(item)
        duree_jours = adapter.get("date_debut")
        if duree_jours :
            adapter['duree_jours'] = adapter['duree_jours'].strip()
        return item

    def clean_type_formation(self,item):
        adapter = ItemAdapter(item)
        type_formation = adapter.get("type_formation")
        if type_formation:
            adapter['type_formation'] = adapter['type_formation'].strip()
        return item
    
    def clean_lieu_formation(self,item):
        adapter = ItemAdapter(item)
        ville = adapter.get("ville")
        if ville:
             adapter['ville'] = adapter['ville'].replace('\n', '').strip()
        return item
    
    def clean_formacodes(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("formacodes")
        if formacodes:
            formacodes_cleaned = [fc.replace(':', '').strip() for fc in formacodes]
            adapter['formacodes'] = ', '.join(formacodes_cleaned)
        else:
            adapter['formacodes'] = None
        return item
    
    def clean_nsf_codes(self, item):
        adapter = ItemAdapter(item)
        nsf_codes = adapter.get("nsf_codes")
        if nsf_codes:
            nsf_codes_cleaned = [nsf.replace(':', '').strip() for nsf in nsf_codes]
            adapter['nsf_codes'] = ', '.join(nsf_codes_cleaned)
        else:
            adapter['nsf_codes'] = None
        return item

