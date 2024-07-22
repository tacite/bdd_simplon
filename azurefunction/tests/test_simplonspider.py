# tests/test_simplonspider.py
import pytest
from scrapy.http import HtmlResponse
from simplonscrapy.spiders.simplonspider import SimplonspiderSpider

@pytest.fixture
def spider():
    return SimplonspiderSpider()

def test_parse_item(spider):
    html_content = '''
    <html>
        <body>
            <h1>Formation Title</h1>
            <a href="/path/to/rncp">RNCP</a>
            <a href="/path/to/rs">RS</a>
            <p>Coût horaire varie de 500 à 1000</p>
        </body>
    </html>
    '''
    response = HtmlResponse(url='https://simplon.co/notre-offre-de-formation.html', body=html_content, encoding='utf-8')
    items = list(spider.parse_item(response))

    assert len(items) == 1
    item = items[0]
    assert item['title'] == 'Formation Title'
    assert item['rncp'] == '/path/to/rncp'
    assert item['rs'] == '/path/to/rs'
    assert item['prix_min'] == '500'
    assert item['prix_max'] == '1000'
