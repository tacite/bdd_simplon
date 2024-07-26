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
        """Initialize the pipeline by creating a SQLAlchemy session."""
        self.Session = sessionmaker(bind=engine)
        
    def process_item(self, item, spider):
        """
        ## process_item()

        Process each item by cleaning the data and inserting it into the database.

        Args:
            item (dict): The item to process.
            spider (scrapy.Spider): The spider that scraped the item.

        Returns:
            dict: The processed item.
        """
        adapter = ItemAdapter(item)
        # Clean the data
        item = self.clean_rncp(item)
        item = self.clean_rs(item)
        item = self.clean_formation_id(item)
        item = self.clean_niveau_sortie(item)
        item = self.clean_prix(item)
        item = self.clean_region(item)
        item = self.clean_start_date(item)
        item = self.clean_duree(item)
        item = self.clean_lieu_formation(item)
        item = self.clean_formacodes_rs(item)
        item = self.clean_formacodes_rncp(item)
        item = self.clean_nsf_codes(item)

        # Insert the data into the database
        session = self.Session()
        formation = Formation(
            titre=adapter.get('titre'),
            niveau_sortie=adapter.get('niveau_sortie'),
            prix=adapter.get('prix'),
            region=adapter.get('region'),
            date_debut=adapter.get('date_debut'),
            duree_jours=adapter.get('duree_jours'),
            ville=adapter.get('ville')
        )
        session.add(formation)
        session.flush()

        # Retrieve nsf_codes
        nsf_codes = adapter.get('nsf_codes')
        for nsf_code in nsf_codes:
            existe_nsf_code = self.session.query(Nsf).filter_by(code=nsf_code).first()
            if not existe_nsf_code:
                existe_nsf_code = Nsf(code=nsf_code)
            formation.nsf_codes.append(existe_nsf_code)

        # Retrieve referentiels
        rncp = adapter.get('rncp')
        for r in rncp:
            existe_rncp = self.session.query(Referentiel).filter_by(type='RNCP', code=r).first()
            if not existe_rncp:
                existe_rncp = Referentiel(type='RNCP', code=r)
            formacodes = adapter.get('formacodes_rncp')
            for formacode in formacodes:
                existe_formacode = self.session.query(Formacode).filter_by(code=formacode).first()
                if not existe_formacode:
                    existe_formacode = Formacode(code=formacode)
                existe_rncp.formacode.append(existe_formacode)
            self.session.add(existe_rncp)
            formation.referentiel.append(existe_rncp)

        rs = adapter.get('rs')
        for r in rs:
            existe_rs = self.session.query(Referentiel).filter_by(type='RS', code=r).first()
            if not existe_rs:
                existe_rs = Referentiel(type='RS', code=r)
            formacodes = adapter.get('formacodes_rs')
            for formacode in formacodes:
                existe_formacode = self.session.query(Formacode).filter_by(code=formacode).first()
                if not existe_formacode:
                    existe_formacode = Formacode(code=formacode)
                existe_rs.formacode.append(existe_formacode)
            self.session.add(existe_rs)
            formation.referentiel.append(existe_rs)

        # Retrieve formacodes
        formacodes = adapter.get('formacodes')
        for formacode in formacodes:
            existe_formacode = self.session.query(Formacode).filter_by(code=formacode).first()
            if not existe_formacode:
                existe_formacode = Formacode(code=formacode)
            formacodes.append(existe_formacode)

        session.commit()
        session.close()

        return item
    
    def clean_rncp(self, item):
        """
        ## clean_rncp()

        Clean the 'rncp' field by extracting only the digits.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        rncp = adapter.get("rncp")
        if rncp:
            rncp_numbers = ''.join(re.findall(r'\d+', rncp))
            adapter['rncp'] = rncp_numbers if rncp_numbers else None
        else:
            adapter['rncp'] = None
        return item

    def clean_rs(self, item):
        """
        ## clean_rs()

        Clean the 'rs' field by extracting the appropriate segment.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
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

    def clean_formation_id(self, item):
        """
        ## clean_formation_id()

        Clean the 'formation_id' field by extracting the last segment.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        formation_id = adapter.get("formation_id")
        if formation_id:
            formation_id = formation_id.split('/')[-1]
            adapter['formation_id'] = formation_id
        return item

    def clean_niveau_sortie(self, item):
        """
        ## clean_niveau_sortie()

        Clean the 'niveau_sortie' field by stripping any whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item

    def clean_prix(self, item):
        """
        ## clean_prix()

        Clean the 'prix_min' and 'prix_max' fields, calculate the average price.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        prix_min = adapter.get("prix_min")
        prix_max = adapter.get("prix_max")

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

        adapter['prix_min'] = prix_min
        adapter['prix_max'] = prix_max

        if prix_min is not None and prix_max is not None:
            prix = (prix_max + prix_min) / 2
        else:
            prix = None

        adapter['prix'] = prix

        return item

    def clean_region(self, item):
        """
        ## clean_region() 

        Clean the 'region' field by removing newline characters and stripping whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        region = adapter.get("region")
        if region:
            adapter['region'] = adapter['region'].replace('\n', '').strip()
        return item
    
    def clean_start_date(self, item):
        """
        ## clean_start_date() 
        Clean the 'date_debut' field by removing newline characters and stripping whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        date_debut = adapter.get("date_debut")
        if date_debut:
            adapter['date_debut'] = adapter['date_debut'].replace('\n', '').strip()
        return item

    def clean_niveau_sortie(self, item):
        """
        ## clean_niveau_sortie()

        Clean the 'niveau_sortie' field by stripping any whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item
    
    def clean_duree(self, item):
        """
        ## clean_duree() 

        Clean the 'duree_jours' field by stripping any whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        duree_jours = adapter.get("date_debut")
        if duree_jours:
            adapter['duree_jours'] = adapter['duree_jours'].strip()
        return item

    def clean_type_formation(self, item):
        """
        ## clean_type_formation()

        Clean the 'type_formation' field by stripping any whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        type_formation = adapter.get("type_formation")
        if type_formation:
            adapter['type_formation'] = adapter['type_formation'].strip()
        return item
    
    def clean_lieu_formation(self, item):
        """
        ## clean_lieu_formation()

        Clean the 'ville' field by removing newline characters and stripping whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        ville = adapter.get("ville")
        if ville:
            adapter['ville'] = adapter['ville'].replace('\n', '').strip()
        return item
    
    def clean_formacodes_rs(self, item):
        """
        ## clean_formacodes_rs()

        Clean the 'formacodes_rs' field by removing colons and stripping whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        formacodes = adapter.get("formacodes_rs")
        if formacodes:
            formacodes_cleaned = [fc.replace(':', '').strip() for fc in formacodes]
            adapter['formacodes_rs'] = int(', '.join(formacodes_cleaned))
        else:
            adapter['formacodes_rs'] = None
        return item

    def clean_formacodes_rncp(self, item):
        """
        ## clean_formacodes_rncp()

        Clean the 'formacodes_rncp' field by removing colons and stripping whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        formacodes = adapter.get("formacodes_rncp")
        if formacodes:
            formacodes_cleaned = [fc.replace(':', '').strip() for fc in formacodes]
            adapter['formacodes_rncp'] = int(', '.join(formacodes_cleaned))
        else:
            adapter['formacodes_rncp'] = None
        return item
    
    def clean_nsf_codes(self, item):
        """
        ## clean_nsf_codes()
        
        Clean the 'nsf_codes' field by removing colons and stripping whitespace.

        Args:
            item (dict): The item to clean.

        Returns:
            dict: The cleaned item.
        """
        adapter = ItemAdapter(item)
        nsf_codes = adapter.get("nsf_codes")
        if nsf_codes:
            nsf_codes_cleaned = [nsf.replace(':', '').strip() for nsf in nsf_codes]
            adapter['nsf_codes'] = ', '.join(nsf_codes_cleaned)
        else:
            adapter['nsf_codes'] = None
        return item
