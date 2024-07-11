import azure.functions as func
import datetime
import json
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from simplonscrapy.simplonscrapy.spiders import simplonFormations
from azure.functions.decorators.core import AuthLevel

app = func.FunctionApp()


@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    process = CrawlerProcess(get_project_settings())
    process.crawl(MovieSpider)
    process.start()  # the script will block here until the crawling is finished

    return func.HttpResponse("scrapping finish", status_code=200, mimetype="application/json")