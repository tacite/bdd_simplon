# Définir vos pipelines d'items ici
#
# N'oubliez pas d'ajouter votre pipeline aux paramètres ITEM_PIPELINES
# Voir : https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Utile pour gérer différents types d'items avec une interface unique
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from .database import engine, Formation, Session
import re

class SimplonscrapyPipeline:
    def __init__(self):
        # Créer une fabrique de sessions SQLAlchemy
        self.Session = sessionmaker(bind=engine)
        
    def process_item(self, item, spider):
        # Créer un ItemAdapter pour accéder aux données de l'item de manière standardisée
        adapter = ItemAdapter(item)
        
        # Nettoyer les données de l'item en utilisant différentes fonctions de nettoyage
        item = self.clean_rncp(item)
        item = self.clean_rs(item)
        item = self.clean_formation_id(item)
        item = self.clean_niveau_sortie(item)
        item = self.clean_prix(item)
        item = self.clean_region(item)
        item = self.clean_start_date(item)
        item = self.clean_duree(item)
        item = self.clean_type_formation(item)
        item = self.clean_lieu_formation(item)
        item = self.clean_formacodes(item)
        item = self.clean_nsf_codes(item)

        # Insérer les données nettoyées de l'item dans la base de données
        session = self.Session()
        formation = Formation(
            title=adapter.get('title'),
            rncp=adapter.get('rncp'),
            rs=adapter.get('rs'),
            formation_id=adapter.get('formation_id'),
            niveau_sortie=adapter.get('niveau_sortie'),
            prix_min=adapter.get('prix_min'),
            prix_max=adapter.get('prix_max'),
            region=adapter.get('region'),
            start_date=adapter.get('start_date'),
            duree=adapter.get('duree'),
            type_formation=adapter.get('type_formation'),
            lieu_formation=adapter.get('lieu_formation'),
            formacodes=adapter.get('formacodes'),
            nsf_codes=adapter.get('nsf_codes')
        )
        session.add(formation)
        session.commit()
        session.close()

        return item
    
    def clean_rncp(self, item):
        # Nettoyer l'identifiant RNCP en extrayant uniquement les caractères numériques
        adapter = ItemAdapter(item)
        rncp = adapter.get("rncp")
        if rncp:
            # Utiliser une expression régulière pour trouver tous les chiffres dans l'identifiant RNCP
            rncp_numbers = ''.join(re.findall(r'\d+', rncp))
            adapter['rncp'] = rncp_numbers if rncp_numbers else None
        else:
            adapter['rncp'] = None
        return item

    def clean_rs(self, item):
        # Nettoyer l'identifiant RS en extrayant le segment pertinent de l'URL
        adapter = ItemAdapter(item)
        rs = adapter.get("rs")
        if rs:
            # Diviser l'URL en segments et extraire l'avant-dernier segment
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
        # Nettoyer l'identifiant de la formation en extrayant le dernier segment de l'URL
        adapter = ItemAdapter(item)
        formation_id = adapter.get("formation_id")
        if formation_id:
            # Diviser l'URL par '/' et prendre le dernier segment
            formation_id = formation_id.split('/')[-1]
            adapter['formation_id'] = formation_id
        return item

    def clean_niveau_sortie(self, item):
        # Nettoyer le niveau de sortie de la formation en supprimant les espaces superflus
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie:
            # Supprimer les espaces avant et après le texte
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item

    def clean_prix(self, item):
        # Nettoyer les prix minimum et maximum en conservant uniquement les caractères numériques
        adapter = ItemAdapter(item)
        prix_min = adapter.get("prix_min")
        prix_max = adapter.get("prix_max")
        if prix_min:
            # Conserver uniquement les chiffres dans le prix minimum
            adapter['prix_min'] = ''.join(filter(str.isdigit, prix_min))
        if prix_max:
            # Conserver uniquement les chiffres dans le prix maximum
            adapter['prix_max'] = ''.join(filter(str.isdigit, prix_max))
        return item

    def clean_region(self, item):
        # Nettoyer la région en supprimant les espaces et les sauts de ligne superflus
        adapter = ItemAdapter(item)
        region = adapter.get("region")
        if region:
            # Remplacer les sauts de ligne par des espaces et supprimer les espaces superflus
            adapter['region'] = adapter['region'].replace('\n', '').strip()
        return item
    
    def clean_start_date(self, item):
        # Nettoyer la date de début de la formation en supprimant les espaces et les sauts de ligne superflus
        adapter = ItemAdapter(item)
        start_date = adapter.get("start_date")
        if start_date:
            # Remplacer les sauts de ligne par des espaces et supprimer les espaces superflus
            adapter['start_date'] = adapter['start_date'].replace('\n', '').strip()
        return item

    def clean_duree(self, item):
        # Nettoyer la durée de la formation en supprimant les espaces superflus
        adapter = ItemAdapter(item)
        duree = adapter.get("duree")
        if duree:
            # Supprimer les espaces avant et après le texte
            adapter['duree'] = adapter['duree'].strip()
        return item

    def clean_type_formation(self, item):
        # Nettoyer le type de formation en supprimant les espaces superflus
        adapter = ItemAdapter(item)
        type_formation = adapter.get("type_formation")
        if type_formation:
            # Supprimer les espaces avant et après le texte
            adapter['type_formation'] = adapter['type_formation'].strip()
        return item
    
    def clean_lieu_formation(self, item):
        # Nettoyer le lieu de la formation en supprimant les espaces et les sauts de ligne superflus
        adapter = ItemAdapter(item)
        lieu_formation = adapter.get("lieu_formation")
        if lieu_formation:
            # Remplacer les sauts de ligne par des espaces et supprimer les espaces superflus
            adapter['lieu_formation'] = adapter['lieu_formation'].replace('\n', '').strip()
        return item
    
    def clean_formacodes(self, item):
        # Nettoyer les formacodes en supprimant les deux-points et en supprimant les espaces superflus
        adapter = ItemAdapter(item)
        formacodes = adapter.get("formacodes")
        if formacodes:
            # Pour chaque formacode, supprimer les deux-points et les espaces avant et après le texte
            formacodes_cleaned = [fc.replace(':', '').strip() for fc in formacodes]
            # Joindre les formacodes nettoyés en une chaîne de caractères
            adapter['formacodes'] = ', '.join(formacodes_cleaned)
        else:
            adapter['formacodes'] = None
        return item
    
    def clean_nsf_codes(self, item):
        # Nettoyer les codes NSF en supprimant les deux-points et en supprimant les espaces superflus
        adapter = ItemAdapter(item)
        nsf_codes = adapter.get("nsf_codes")
        if nsf_codes:
            # Pour chaque code NSF, supprimer les deux-points et les espaces avant et après le texte
            nsf_codes_cleaned = [nsf.replace(':', '').strip() for nsf in nsf_codes]
            # Joindre les codes NSF nettoyés en une chaîne de caractères
            adapter['nsf_codes'] = ', '.join(nsf_codes_cleaned)
        else:
            adapter['nsf_codes'] = None
        return item
