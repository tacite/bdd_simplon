from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
import re
from simplonscrapy.items import SimplonscrapyItem

#########################################################################################################
# 1er spider:
class SimplonspiderSpider(CrawlSpider):
    name = "simplonspider"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    # Définir les règles de scraping
    rules = [
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"Découvrez la formation")]'), callback='parse_item', follow=False),
    ]

    # Démarrage des requêtes avec l'utilisation de Playwright pour gérer le JavaScript
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})  # Utilisation de playwright pour JavaScript

    # Méthode pour analyser les éléments de la page
    def parse_item(self, response):
        item = {}

        # Récupérer le titre de la formation
        item['title'] = response.xpath('//h1/text()').get()

        # Récupérer l'identifiant RNCP
        item['rncp'] = response.xpath('//a[contains(text(),"RNCP")]/@href').get()

        # Récupérer l'identifiant RS
        item['rs'] = response.xpath('//a[contains(@href,"/rs/")]/@href').get()

        # Extraire l'URL et obtenir l'identifiant de la formation
        item['formation_id']=response.url


        # Récupérer le niveau de sortie de la formation
        item['niveau_sortie']= response.xpath('//a[contains(text(),"RNCP")]/following-sibling::text()[1]').get()


        # Récupérer le prix min et max de la formation
        # Utiliser XPath pour trouver un paragraphe contenant le texte "coût horaire"
        prix_text = response.xpath('//p[contains(text(),"coût horaire")]').get()
        
        # Vérifier si du texte correspondant au coût horaire a été trouvé
        if prix_text:
            # Utiliser des expressions régulières pour extraire le prix minimum
            # Rechercher la phrase "varie de" suivie d'un ou plusieurs chiffres
            prix_min_text = re.search(r'varie de (\d+)', prix_text)
            
            # Utiliser des expressions régulières pour extraire le prix maximum
            # Rechercher la phrase "à" suivie d'un ou plusieurs chiffres
            prix_max_text = re.search(r'à (\d+)', prix_text)
            
            # Si le prix minimum a été trouvé, extraire le groupe de capture correspondant aux chiffres
            # Sinon, définir le prix minimum à None
            item['prix_min'] = prix_min_text.group(1) if prix_min_text else None
            
            # Si le prix maximum a été trouvé, extraire le groupe de capture correspondant aux chiffres
            # Sinon, définir le prix maximum à None
            item['prix_max'] = prix_max_text.group(1) if prix_max_text else None
        else:
            # Si aucun texte correspondant au coût horaire n'a été trouvé,
            # définir les prix minimum et maximum à None
            item['prix_min'] = None
            item['prix_max'] = None

        # Retourner l'item collecté avec toutes les informations extraites
        yield item

####################################################################################
# 2ème spider :
class Simplonspider2Spider(CrawlSpider):
    name = "simplonspider2"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    # Définir les règles de scraping
    rules = [
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"Toutes les sessions")]'), callback='parse_item2', follow=False),
    ]

    # Démarrage des requêtes avec l'utilisation de Playwright pour gérer le JavaScript
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})

    # Méthode pour analyser les éléments de la page
    def parse_item2(self, response):
        item = {}

        # Récupérer le titre de la formation
        item['title2'] = response.xpath('//h2[@class="card-title"]/text()').get()

        # Récupérer la région de la formation
        item['region'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "location_on")]/following-sibling::text()').get()

        # Récupérer la date de début de la formation
        item['start_date'] = response.xpath('//div[@class="card-session-info calendar"]/i[contains(text(), "event")]/following-sibling::text()').get()

        # Récupérer le niveau de sortie de la formation
        item['niveau_sortie'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "school")]/following-sibling::text()').get()

        # Récupérer la durée de la formation
        item['duree'] = response.xpath('//div[@class="card-session-info"]/i[contains(text(), "hourglass_empty")]/following-sibling::text()').get()

        # Récupérer le type de formation
        item['type_formation'] = response.xpath('//div[@class="card-content-tag"]/a/text()').get()

        # Récupérer le lieu de la formation
        item['lieu_formation'] = response.xpath('//div[@class="card-content"]/text()[normalize-space()]').get()

        # Extraire l'URL et obtenir l'identifiant de la formation
        item['formation_id'] = response.url

        # Retourner l'item collecté
        yield item
##########################################################################
#3ème spider:
class SimplonCrawlSpider(CrawlSpider):
    name = "simplonspider3"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    # Définir les règles de scraping
    rules = (
        Rule(LinkExtractor(allow=('/formation/',), restrict_xpaths='//a[contains(text(),"Découvrez la formation")]'), callback='parse_formation', follow=True),
    )

    # Méthode pour analyser les éléments de la page de formation
    def parse_formation(self, response):
        item = SimplonscrapyItem()

        # Récupérer le titre de la formation
        item['title'] = response.xpath('//h1/text()').get().strip()

        # Vérifier si l'identifiant RNCP a été trouvé
        if rncp_href:
            # Compléter l'URL relative RNCP avec le domaine de base pour obtenir l'URL absolue
            rncp_href = response.urljoin(rncp_href)
            
            # Créer une nouvelle requête pour récupérer la page France Compétences liée à l'identifiant RNCP
            request = scrapy.Request(rncp_href, callback=self.parse_france_competences)
            
            # Passer l'item en cours à la requête suivante pour préserver les données déjà extraites
            request.meta['item'] = item
            
            # Déclencher la nouvelle requête pour analyser la page France Compétences
            yield request
        else:
            # Si aucun identifiant RNCP n'est trouvé, définir les valeurs correspondantes à None
            item['rncp'] = None
            item['formacodes'] = None
            item['nsf_codes'] = None
            
            # Retourner l'item collecté sans les informations supplémentaires de France Compétences
            yield item

        # Extraire l'URL et obtenir l'identifiant de la formation
        item['formation_id']=response.url

    # Méthode pour analyser les éléments de la page France Compétences
    def rncp_parse_france_competences(self, response):
        item = response.meta['item']

        # Extraire des informations supplémentaires depuis la page de France Compétences
        item['rncp'] = response.xpath('//span[@class="tag--fcpt-certification__status font-bold"]/text()').get()
        item['formacodes'] = response.xpath('//p[contains(text(),"Formacode(s)")]/following-sibling::div/p/span/text()').getall()
        item['nsf_codes'] = response.xpath('//p[contains(text(),"Code(s) NSF")]/following-sibling::div/p/span/text()').getall()
        
        yield item
    
    # idem avec le RS
        rs_href = response.xpath('//a[contains(text(),"RS")]/@href').get()
        if rs_href:
            rs_href = response.urljoin(rs_href)
            request = scrapy.Request(rs_href, callback=self.rs_parse_france_competences)
            request.meta['item'] = item
            yield request
        else:
            item['rs'] = None
            item['formacodes'] = None
            item['nsf_codes'] = None
            yield item

        # Extraire l'URL et obtenir l'identifiant de la formation
        item['formation_id']=response.url


    def rs_parse_france_competences(self, response):
        item = response.meta['item']

        # Extraire des informations supplémentaires depuis la page de France Compétences
        item['rs'] = response.xpath('//span[@class="tag--fcpt-certification__status font-bold"]/text()').get()
        item['formacodes'] = response.xpath('//p[contains(text(),"Formacode(s)")]/following-sibling::div/p/span/text()').getall()
        item['nsf_codes'] = response.xpath('//p[contains(text(),"Code(s) NSF")]/following-sibling::div/p/span/text()').getall()
        
        yield item