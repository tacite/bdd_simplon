# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Add the project root to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from models.parents import Formation, Formacode, Nsf, Referentiel
from models.common_imports import Base
import re

class SimplonscrapyPipeline1:
    def open_spider(self, spider):
        """
        ## open_spider()

        Initialize the database connection and session when the spider opens.

        Args:
            spider (scrapy.Spider): The spider that is being opened.
        """
        username = "postgres"
        password = ""
        port = 5432
        database = "postgres"
        hostname = "localhost"
        connection_string = "postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"
        # connection_string = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
        engine = create_engine(connection_string)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def process_item(self, item, spider):
        """
        ## process_item()

        Process each item by cleaning the data and inserting it into the database.

        Args:
            item (scrapy.Item): The item to process.
            spider (scrapy.Spider): The spider that scraped the item.

        Returns:
            scrapy.Item: The processed item.
        """        
        adapter = ItemAdapter(item)
        item = self.clean_formation_id(item)
        item = self.clean_niveau_sortie(item)
        formation = Formation(titre=adapter.get('titre'), niveau_sortie=adapter.get('niveau_sortie'),
                            simplon_id=adapter.get('formation_id'), source_info='simplon')
        self.session.add(formation)
        self.session.commit()
        return item
        
    def clean_formation_id(self, item):
        """
        ## clean_formation_id()

        Clean the formation_id by extracting the last part of the URL.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned formation_id.
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

        Clean the niveau_sortie field by stripping whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned niveau_sortie.
        """
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item

        
    def close_spider(self, spider):
        """
        ## close_spider()

        Close the database session when the spider closes.

        Args:
            spider (scrapy.Spider): The spider that is being closed.
        """
        self.session.close()

class SimplonscrapyPipeline2:
    def open_spider(self, spider):
        """
        ## open_spider()

        Initialize the database connection and session when the spider opens.

        Args:
            spider (scrapy.Spider): The spider that is being opened.
        """
        username = "postgres"
        password = ""
        port = 5432
        database = "postgres"
        hostname = "localhost"
        connection_string = "postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"
        # connection_string = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
        engine = create_engine(connection_string)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def process_item(self, item, spider):
        """
        ## process_item()

        Process each item by cleaning the data and inserting it into the database.

        Args:
            item (scrapy.Item): The item to process.
            spider (scrapy.Spider): The spider that scraped the item.

        Returns:
            scrapy.Item: The processed item.
        """
        adapter = ItemAdapter(item)
        item = self.clean_formation_id(item)
        item = self.clean_niveau_sortie(item)
        item = self.clean_region(item)
        item = self.clean_date_debut(item)
        item = self.clean_ville(item)
        item = self.clean_duree(item)
        formation = self.session.query(Formation).filter_by(simplon_id=adapter.get('formation_id')).first()
        if formation:
            formation.niveau_sortie = adapter.get('niveau_sortie')
            formation.region = adapter.get('region')
            formation.date_debut = adapter.get('date_debut')
            formation.ville = adapter.get('ville')
            self.session.commit()
        return item

    def clean_ville(self, item):
        """
        ## clean_ville()

        Clean the ville field by stripping whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned ville.
        """
        adapter = ItemAdapter(item)
        ville = adapter.get("ville")
        if ville:
            ville = ville.strip()
            adapter['ville'] = ville
        return item
    
    def clean_duree(self, item):
        """
        ## clean_duree()

        Clean the duree field by stripping whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned duree.
        """
        adapter = ItemAdapter(item)
        duree_jours = adapter.get("date_debut")
        if duree_jours:
            adapter['duree_jours'] = adapter['duree_jours'].strip()
        return item
    
    def clean_date_debut(self, item):
        """
        ## clean_date_debut()

        Clean the date_debut field by removing unnecessary text and whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned date_debut.
        """
        adapter = ItemAdapter(item)
        date_debut = adapter.get("date_debut")
        if date_debut:
            adapter['date_debut'] = adapter['date_debut'].replace('\n', '').strip().replace("Début : ", '')
        return item
    
    def clean_region(self, item):
        """
        ## clean_region()

        Clean the region field by removing unnecessary text and whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned region.
        """
        adapter = ItemAdapter(item)
        region = adapter.get("region")
        if region:
            adapter['region'] = adapter['region'].replace('\n', '').strip()
        return item
        
    def clean_formation_id(self, item):
        """
        ## clean_formation_id()

        Clean the formation_id by extracting the last part of the URL.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned formation_id.
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

        Clean the niveau_sortie field by stripping whitespace and removing unnecessary text.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned niveau_sortie.
        """
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip().replace("Sortie : ", "")
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item

        
    def close_spider(self, spider):
        """
        ## close_spider()

        Close the database session when the spider closes.

        Args:
            spider (scrapy.Spider): The spider that is being closed.
        """
        self.session.close()

class SimplonscrapyPipeline3:
    def open_spider(self, spider):
        """
        ## open_spider()

        Initialize the database connection and session when the spider opens.

        Args:
            spider (scrapy.Spider): The spider that is being opened.
        """
        username = "postgres"
        password = ""
        port = 5432
        database = "postgres"
        hostname = "localhost"
        connection_string = "postgresql+psycopg2://adminsadahe:SadaHe111@sadaheformationserver.postgres.database.azure.com:5432/sadaheformations"
        # connection_string = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
        engine = create_engine(connection_string)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def process_item(self, item, spider):
        """
        ## process_item()

        Process each item by cleaning the data and inserting it into the database.

        Args:
            item (scrapy.Item): The item to process.
            spider (scrapy.Spider): The spider that scraped the item.

        Returns:
            scrapy.Item: The processed item.
        """
        adapter = ItemAdapter(item)
        item = self.clean_formation_id(item)
        item = self.clean_rs(item)
        item = self.clean_rncp(item)
        item = self.clean_nsf_codes(item)
        item = self.clean_formacodes_rs(item)
        item = self.clean_formacodes_rncp(item)
        
        
        formation = self.session.query(Formation).filter_by(simplon_id=adapter.get('formation_id')).first()
        if formation:
            nsf_codes = adapter.get('nsf_codes')
            if nsf_codes:
                for nsf_code in nsf_codes:
                    nsf = self.session.query(Nsf).filter_by(code=nsf_code).first()
                    if not nsf:
                        nsf = Nsf(code=nsf_code)
                    if nsf not in formation.nsf:
                        formation.nsf.append(nsf)
            rs_code = adapter.get('rs')
            if rs_code:
                rs = self.session.query(Referentiel).filter_by(code=rs_code, type="RS").first()
                if not rs:
                    rs = Referentiel(code=rs_code, type="RS")
                    formacode_rs = adapter.get("formacodes_rs")
                    for code in formacode_rs:
                        formacode = self.session.query(Formacode).filter_by(code=code).first()
                        if not formacode:
                            formacode = Formacode(code=code)
                        rs.formacode.append(formacode)
                if rs not in formation.referentiel:
                    formation.referentiel.append(rs)
            rncp_code = adapter.get('rncp')
            if rncp_code:
                rncp = self.session.query(Referentiel).filter_by(code=rs_code, type="RNCP").first()
                if not rncp:
                    rncp = Referentiel(code=rncp_code, type="RNCP")
                    formacode_rncp = adapter.get("formacodes_rncp")
                    for code in formacode_rncp:
                        formacode = self.session.query(Formacode).filter_by(code=code).first()
                        if not formacode:
                            formacode = Formacode(code=code)
                        rncp.formacode.append(formacode)
                if rncp not in formation.referentiel:
                    formation.referentiel.append(rncp)                    
            self.session.commit()        
        return item

    def clean_formacodes_rs(self, item):
        """
        ## clean_formacodes_rs()

        Clean the formacodes_rs field by removing colons and stripping whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned formacodes_rs.
        """
        adapter = ItemAdapter(item)
        formacodes = adapter.get("formacodes_rs")
        if formacodes:
            formacodes_cleaned = [fc.replace(':', '').strip() for fc in formacodes]
            adapter['formacodes_rs'] = formacodes_cleaned
        else:
            adapter['formacodes_rs'] = None
        return item

    def clean_formacodes_rncp(self, item):
        """
        ## clean_formacodes_rncp()

        Clean the formacodes_rncp field by removing colons and stripping whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned formacodes_rncp.
        """
        adapter = ItemAdapter(item)
        formacodes = adapter.get("formacodes_rncp")
        if formacodes:
            formacodes_cleaned = [fc.replace(':', '').strip() for fc in formacodes]
            adapter['formacodes_rncp'] = formacodes_cleaned
        else:
            adapter['formacodes_rncp'] = None
        return item
    
    def clean_nsf_codes(self, item):
        """
        ## clean_nsf_codes()

        Clean the nsf_codes field by removing colons and stripping whitespace.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned nsf_codes.
        """
        adapter = ItemAdapter(item)
        nsf_codes = adapter.get("nsf_codes")
        if nsf_codes:
            nsf_codes_cleaned = [nsf.replace(':', '').strip() for nsf in nsf_codes]
            adapter['nsf_codes'] = nsf_codes_cleaned
        else:
            adapter['nsf_codes'] = None
        return item

    def clean_rncp(self, item):
        """
        ## clean_rncp()

        Clean the rncp field by removing unnecessary text.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned rncp.
        """
        adapter = ItemAdapter(item)
        rncp = adapter.get("rncp")
        if rncp:
            adapter['rncp'] = rncp.replace('RNCP', '')
        else:
            adapter['rncp'] = None
        return item

    def clean_rs(self, item):
        """
        ## clean_rs()

        Clean the rs field by removing unnecessary text.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned rs.
        """
        adapter = ItemAdapter(item)
        rs = adapter.get("rs")
        if rs:
            adapter['rs'] = rs.replace("RS", '')
        else:
            adapter['rs'] = None
        return item    

    def clean_formation_id(self, item):
        """
        ## clean_formation_id()

        Clean the formation_id by extracting the last part of the URL.

        Args:
            item (scrapy.Item): The item to process.

        Returns:
            scrapy.Item: The item with cleaned formation_id.
        """
        adapter = ItemAdapter(item)
        formation_id = adapter.get("formation_id")
        if formation_id:
            formation_id = formation_id.split('/')[-1]
            adapter['formation_id'] = formation_id
        return item

    def close_spider(self, spider):
        """
        ## close_spider()

        Close the database session when the spider closes.

        Args:
            spider (scrapy.Spider): The spider that is being closed.
        """
        self.session.close()
