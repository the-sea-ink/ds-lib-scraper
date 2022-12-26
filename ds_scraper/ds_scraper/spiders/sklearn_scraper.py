from io import StringIO
from lxml import etree

import scrapy
from scrapy.crawler import CrawlerProcess


class NoneFilter:
    def __init__(self, feed_options):
        self.feed_options = feed_options

    def accepts(self, item):
        #if len(item["description"]) == 0:
            #return False
        return True


class SklearnScraper(scrapy.Spider):
    parser = etree.HTMLParser()
    name = "sklearn"
    # starting URL
    start_urls = [
        'https://scikit-learn.org/stable/modules/classes.html'

    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "COOKIES_ENABLED": False,
        "FEEDS": {
            "sklearn.csv": {
                "format": "csv",
                "item_filter": NoneFilter
            },

        }
    }

    f = open("sklearn.csv", 'w').close()

    def parse(self, response):
        # parse function names
        names = response.xpath('//table[@class="autosummary longtable docutils align-default"]//a[@class="reference '
                               'internal"]//span[@class="pre"]//text()').getall()
        for name in names:
            url = "https://scikit-learn.org/stable/modules/generated/sklearn." + name + ".html"
            # if url == 'https://pandas.pydata.org/docs/reference/api/pandas.io.json.build_table_schema.html':
            yield scrapy.Request(url, callback=self.parse_data)


    def parse_data(self, response):
        # put separated parameters together
        description = "".join(response.xpath('(//dd//p)[1]//text()').getall()),
        description = str(description).replace("\n", " ").replace("('", "").replace("',)", "")

        html_params = response.xpath('(//dt[@class="sig sig-object py"])[1]//em[@class="sig-param"]').getall()
        edited_params = []
        for separated_html_params in html_params:
            parsed_elem = etree.parse(StringIO(separated_html_params), self.parser)
            elem_parts = parsed_elem.xpath("//text()")
            param = ""
            for param_part in elem_parts:
                param = param + param_part
            edited_params.append(param)


        yield {
            "title": response.xpath('//dt[@class="sig sig-object py"]/@id').get(),
            "description": description,
            "link": response.request.url,
            "parameters": edited_params
        }


process = CrawlerProcess()
process.crawl(SklearnScraper)
process.start()

# scraping in terminal: scrapy shell link


