import scrapy


class SimplonformationsSpider(scrapy.Spider):
    name = 'simplonFormations'
    allowed_domains = ['hautsdefrance.simplon.co']
    start_urls = ['http://hautsdefrance.simplon.co/']

    def parse(self, response):
        pass
