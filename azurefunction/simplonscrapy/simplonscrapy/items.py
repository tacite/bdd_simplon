# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SimplonscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    titre  = scrapy.Field()
    rncp  = scrapy.Field()
    rs  = scrapy.Field()
    formation_id  = scrapy.Field()
    niveau_sortie  = scrapy.Field()
    prix = scrapy.Field()
    prix_min = scrapy.Field()
    prix_max=scrapy.Field()
    region = scrapy.Field()
    date_debut = scrapy.Field()
    duree_jours = scrapy.Field()
    # type_formation = scrapy.Field()
    ville = scrapy.Field()
    formacodes_rs = scrapy.Field()
    formacodes_rncp = scrapy.Field()
    nsf_codes = scrapy.Field()
