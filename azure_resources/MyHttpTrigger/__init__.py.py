import azure.functions as func
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from simplonscrapy.simplonscrapy.spiders import simplonFormations

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Request received.')

    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(simplonFormations)
        process.start()  # Bloque jusqu'à ce que le crawling soit terminé

        return func.HttpResponse("Scraping finished", status_code=200)
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
