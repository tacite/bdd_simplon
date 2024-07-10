from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy

# 1er spider :
class SimplonspiderSpider(CrawlSpider):
    name = "simplonspider"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = [
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"Découvrez la formation")]'), callback='parse_item', follow=False),
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})  # Utilisation de playwright pour JavaScript

    def parse_item(self, response):
        item = {}

        # Récupérer le titre de la formation
        item['title'] = response.xpath('//h1/text()').get()

        # Récupérer l'identifiant RNCP
        rncp_href = response.xpath('//a[contains(text(),"RNCP")]/@href').get()
        if rncp_href:
            rncp_id = rncp_href.split('/')[-2]  # Récupérer le dernier segment avant le dernier '/'
            item['rncp'] = rncp_id
        else:
            item['rncp'] = None

        # Récupérer l'identifiant RS
        rs_href = response.xpath('//a[contains(@href,"/rs/")]/@href').get()
        if rs_href:
            rs_id = rs_href.split('/')[-2]  # Récupérer le dernier segment avant le dernier '/'
            item['rs'] = rs_id
        else:
            item['rs'] = None

        # Extraire l'URL et obtenir l'identifiant de la formation
        formation_url = response.url
        formation_id = formation_url.split('/')[-1]
        item['formation_id'] = formation_id

        # Récupérer le niveau de sortie de la formation
        rncp_text = response.xpath('//a[contains(text(),"RNCP")]/following-sibling::text()[1]').get()
        if rncp_text:
            niveau_sortie = rncp_text.strip()
            item['niveau_sortie'] = niveau_sortie
        else:
            item['niveau_sortie'] = None

        # Récupérer le prix min et max de la formation
        prix_text = response.xpath('//p[contains(text(),"coût horaire")]').get()
        if prix_text:
            prix_min_text = prix_text.split('varie de ')[1].split(' euros')[0].split(' à ')[0]
            prix_max_text = prix_text.split('à ')[1].split(' euros')[0]

            prix_min = ''.join(filter(str.isdigit, prix_min_text))  # Filtrer et concaténer uniquement les chiffres
            prix_max = ''.join(filter(str.isdigit, prix_max_text))  # Filtrer et concaténer uniquement les chiffres

            item['prixmin'] = prix_min
            item['prixmax'] = prix_max
        else:
            item['prixmin'] = None
            item['prixmax'] = None

        yield item

####################################################################################
# 2ème spider :
class Simplonspider2Spider(CrawlSpider):
    name = "simplonspider2"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = [
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"Toutes les sessions")]'), callback='parse_item2', follow=False),
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})  # Utilisation de playwright pour JavaScript

    def parse_item2(self, response):
        item = {}

        # Récupérer le titre de la formation
        item['title'] = response.xpath('//h2[@class="card-title"]/text()').get()

        # Récupérer la région de la formation
        item['region'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "location_on")]/following-sibling::text()').get()

        # Récupérer la date de début de la formation
        item['start_date'] = response.xpath('//div[@class="card-session-info calendar"]/i[contains(text(), "event")]/following-sibling::text()').get()

        # Récupérer le niveau de sortie de la formation
        item['niveau_sortie'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "school")]/following-sibling::text()').get()
        if item['niveau_sortie']:
            item['niveau_sortie'] = item['niveau_sortie'].strip().replace("Sortie :", "").strip()

        # Récupérer la durée de la formation
        item['duree'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "hourglass_empty")]/following-sibling::text()').get()
        if item['duree']:
            item['duree'] = item['duree'].strip()

        yield item

