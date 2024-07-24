from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
from scrapy.crawler import CrawlerProcess
import re
from simplonscrapy.items import SimplonscrapyItem

# 1er spider:
class SimplonspiderSpider(CrawlSpider):
    """
    A Scrapy spider that scrapes Simplon website for formation details.
    """
        
    name = "simplonspider"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = [
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"Découvrez la formation")]'), callback='parse_item', follow=False),
    ]

    def start_requests(self):
        """
        Generates initial requests to start scraping using the URLs defined in `start_urls`.
        Uses Playwright to handle JavaScript content.
        """
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})  # Utilisation de playwright pour JavaScript

    def parse_item(self, response):
        """
        Parses the formation details from the response.
        
        Extracts:
            - Title of the formation
            - RNCP identifier
            - RS identifier
            - Exit level of the formation
            - Minimum and maximum price of the formation

        Args:
            response (scrapy.http.Response): The response object containing the HTML content of the page.

        Yields:
            dict: A dictionary with extracted formation details.
        """
        item = {}

        # Récupérer le titre de la formation
        item['titre'] = response.xpath('//h1/text()').get()

        # Récupérer l'identifiant RNCP
        item['rncp'] = response.xpath('//a[contains(text(),"RNCP")]/@href').get()

        # Récupérer l'identifiant RS
        item['rs'] = response.xpath('//a[contains(@href,"/rs/")]/@href').get()

        item['formation_id']=response.url


        # Récupérer le niveau de sortie de la formation
        item['niveau_sortie']= response.xpath('//a[contains(text(),"RNCP")]/following-sibling::text()[1]').get()


        # Récupérer le prix min et max de la formation
        prix_text = response.xpath('//p[contains(text(),"coût horaire")]').get()
        if prix_text:
            prix_min_text = re.search(r'varie de (\d+)', prix_text)
            prix_max_text = re.search(r'à (\d+)', prix_text)
            item['prix_min'] = prix_min_text.group(1) if prix_min_text else None
            item['prix_max'] = prix_max_text.group(1) if prix_max_text else None
        else:
            item['prix_min'] = None
            item['prix_max'] = None


        yield item

####################################################################################
# 2ème spider :
class Simplonspider2Spider(CrawlSpider):
    """
    A Scrapy spider that scrapes Simplon website for session details.
    """
    name = "simplonspider2"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = [
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"Toutes les sessions")]'), callback='parse_item2', follow=False),
    ]

    def start_requests(self):
        """
        Generates initial requests to start scraping using the URLs defined in `start_urls`.
        Uses Playwright to handle JavaScript content.
        """
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})  # Utilisation de playwright pour JavaScript

    def parse_item2(self, response):
        """
        Parses the session details from the response.

        Extracts:
            - Title of the formation
            - Region of the formation
            - Start date of the formation
            - Exit level of the formation
            - Duration of the formation in days
            - City of the formation

        Args:
            response (scrapy.http.Response): The response object containing the HTML content of the page.

        Yields:
            dict: A dictionary with extracted session details.
        """
        item = {}

        # Récupérer le titre de la formation
        item['titre'] = response.xpath('//h2[@class="card-title"]/text()').get()

        # Récupérer la région de la formation
        item['region'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "location_on")]/following-sibling::text()').get()

        # Récupérer la date de début de la formation
        item['date_debut'] = response.xpath('//div[@class="card-session-info calendar"]/i[contains(text(), "event")]/following-sibling::text()').get()

        # Récupérer le niveau de sortie de la formation
        item['niveau_sortie'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "school")]/following-sibling::text()').get()

        # Récupérer la durée de la formation
        item['duree_jours'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "hourglass_empty")]/following-sibling::text()').get()

        # Récupérer la type deformation
        # item['type_formation'] = response.xpath('//div[@class="card-content-tag"]/a/text()').get()

        # Récupérer le lieu de la formation
        item['ville'] = response.xpath('//div[@class="card-content"]/text()[normalize-space()]').get()

        # Extraire l'URL et obtenir l'identifiant de la formation
        item['formation_id']=response.url

        yield item
##########################################################################
#3ème spider:
class SimplonCrawlSpider(CrawlSpider):
    """
    A Scrapy spider that scrapes Simplon and France Compétences websites for formation details.
    """
    name = "simplonspider3"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]


    rules = (
        Rule(LinkExtractor(allow=('/formation/',), restrict_xpaths='//a[contains(text(),"Découvrez la formation")]'), callback='parse_formation', follow=True),
    )

    def parse_formation(self, response):
        """
        Parses formation details from the response and makes additional requests for RNCP and RS details.

        Args:
            response (scrapy.http.Response): The response object containing the HTML content of the page.

        Yields:
            dict: A dictionary with extracted formation details and requests for additional information.
        """
        item = SimplonscrapyItem()
        #item = {}

        # Récupérer le titre de la formation
        item['titre'] = response.xpath('//h1/text()').get().strip()

        # Récupérer l'identifiant RNCP
        rncp_href = response.xpath('//a[contains(text(),"RNCP")]/@href').get()
        if rncp_href:
            rncp_href = response.urljoin(rncp_href)
            request = scrapy.Request(rncp_href, callback=self.rncp_parse_france_competences)
            request.meta['item'] = item
            yield request
        else:
            item['rncp'] = None
            item['formacodes_rncp'] = None
            item['nsf_codes'] = None
            yield item

        # Extraire l'URL et obtenir l'identifiant de la formation
        item['formation_id']=response.url


    def rncp_parse_france_competences(self, response):
        """
        Parses RNCP details from France Compétences and updates the item with additional information.

        Args:
            response (scrapy.http.Response): The response object containing the HTML content of the RNCP page.

        Yields:
            dict: An updated dictionary with RNCP details.
        """
        item = response.meta['item']

        # Extraire des informations supplémentaires depuis la page de France Compétences
        item['rncp'] = response.xpath('//span[@class="tag--fcpt-certification__status font-bold"]/text()').get()
        item['formacodes_rncp'] = response.xpath('//p[contains(text(),"Formacode(s)")]/following-sibling::div/p/span/text()').getall()
        item['nsf_codes'] = response.xpath('//p[contains(text(),"Code(s) NSF")]/following-sibling::div/p/span/text()').getall()
        
        yield item
    
    # Récupérer l'identifiant RS
        rs_href = response.xpath('//a[contains(text(),"RS")]/@href').get()
        if rs_href:
            rs_href = response.urljoin(rs_href)
            request = scrapy.Request(rs_href, callback=self.rs_parse_france_competences)
            request.meta['item'] = item
            yield request
        else:
            item['rs'] = None
            item['formacodes_rs'] = None
            item['nsf_codes'] = None
            yield item

        # Extraire l'URL et obtenir l'identifiant de la formation
        item['formation_id']=response.url


    def rs_parse_france_competences(self, response):
        """
        Parses RS details from France Compétences and updates the item with additional information.

        Args:
            response (scrapy.http.Response): The response object containing the HTML content of the RS page.

        Yields:
            dict: An updated dictionary with RS details.
        """
        item = response.meta['item']

        # Extraire des informations supplémentaires depuis la page de France Compétences
        item['rs'] = response.xpath('//span[@class="tag--fcpt-certification__status font-bold"]/text()').get()
        item['formacodes_rs'] = response.xpath('//p[contains(text(),"Formacode(s)")]/following-sibling::div/p/span/text()').getall()
        item['nsf_codes'] = response.xpath('//p[contains(text(),"Code(s) NSF")]/following-sibling::div/p/span/text()').getall()
        
        yield item