"""
Module définissant les modèles pour les items extraits avec Scrapy.

Ce module contient la définition de la classe `SimplonscrapyItem` qui spécifie les champs des items à extraire
à partir des pages web lors du processus de scraping.

Documentation:
https://docs.scrapy.org/en/latest/topics/items.html
"""

import scrapy

class SimplonscrapyItem(scrapy.Item):
    """
    Classe représentant un item extrait avec Scrapy.

    Cette classe définit les différents champs que Scrapy extrait à partir des pages web cibles. Chaque champ
    correspond à une information spécifique que l'on souhaite extraire.
    """
    
    # Define the fields for your item here:
    
    titre = scrapy.Field()
    """str: Le titre de la formation."""
    
    rncp = scrapy.Field()
    """str: Le code RNCP (Répertoire National des Certifications Professionnelles)."""
    
    rs = scrapy.Field()
    """str: Le code RS (Répertoire Spécifique)."""
    
    formation_id = scrapy.Field()
    """str: L'identifiant unique de la formation."""
    
    niveau_sortie = scrapy.Field()
    """str: Le niveau de sortie de la formation."""
    
    prix = scrapy.Field()
    """float: Le prix de la formation."""
    
    prix_min = scrapy.Field()
    """float: Le prix minimum de la formation."""
    
    prix_max = scrapy.Field()
    """float: Le prix maximum de la formation."""
    
    region = scrapy.Field()
    """str: La région où la formation est dispensée."""
    
    date_debut = scrapy.Field()
    """str: La date de début de la formation."""
    
    duree_jours = scrapy.Field()
    """int: La durée de la formation en jours."""
    
    # type_formation = scrapy.Field()
    # """str: Le type de formation (commenté)."""
    
    ville = scrapy.Field()
    """str: La ville où la formation est dispensée."""
    
    formacodes_rs = scrapy.Field()
    """list: Les formacodes associés au code RS."""
    
    formacodes_rncp = scrapy.Field()
    """list: Les formacodes associés au code RNCP."""
    
    nsf_codes = scrapy.Field()
    """list: Les codes NSF (Nomenclature des Spécialités de Formation)."""
