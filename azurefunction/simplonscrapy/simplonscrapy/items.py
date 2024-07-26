"""
Module defining the models for items extracted with Scrapy.

This module contains the definition of the `SimplonscrapyItem` class, which specifies the fields of items to extract
from web pages during the scraping process.

Documentation:
https://docs.scrapy.org/en/latest/topics/items.html
"""

import scrapy

class SimplonscrapyItem(scrapy.Item):
    """
    ## SimplonscrapyItem()

    Class representing an item extracted with Scrapy.

    This class defines the various fields that Scrapy extracts from the target web pages. Each field
    corresponds to a specific piece of information to be extracted.
    """
    
    # Define the fields for your item here:
    
    titre = scrapy.Field()
    """str: The title of the training."""
    
    rncp = scrapy.Field()
    """str: The RNCP (Répertoire National des Certifications Professionnelles) code."""
    
    rs = scrapy.Field()
    """str: The RS (Répertoire Spécifique) code."""
    
    formation_id = scrapy.Field()
    """str: The unique identifier of the training."""
    
    niveau_sortie = scrapy.Field()
    """str: The level of completion of the training."""
    
    prix = scrapy.Field()
    """float: The price of the training."""
    
    prix_min = scrapy.Field()
    """float: The minimum price of the training."""
    
    prix_max = scrapy.Field()
    """float: The maximum price of the training."""
    
    region = scrapy.Field()
    """str: The region where the training is provided."""
    
    date_debut = scrapy.Field()
    """str: The start date of the training."""
    
    duree_jours = scrapy.Field()
    """int: The duration of the training in days."""
    
    # type_formation = scrapy.Field()
    # """str: The type of training (commented out)."""
    
    ville = scrapy.Field()
    """str: The city where the training is provided."""
    
    formacodes_rs = scrapy.Field()
    """list: The formacodes associated with the RS code."""
    
    formacodes_rncp = scrapy.Field()
    """list: The formacodes associated with the RNCP code."""
    
    nsf_codes = scrapy.Field()
    """list: The NSF (Nomenclature des Spécialités de Formation) codes."""
