# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SimplonscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title  = scrapy.Field()
    rncp  = scrapy.Field()
    rs  = scrapy.Field()
    formation_id  = scrapy.Field()
    niveau_sortie  = scrapy.Field()
    prix_min = scrapy.Field()
    prix_max=scrapy.Field()
    region = scrapy.Field()
    start_date = scrapy.Field()
    duree = scrapy.Field()
    type_formation = scrapy.Field()
    lieu_formation = scrapy.Field()
    formacodes = scrapy.Field()
    nsf_codes = scrapy.Field()
