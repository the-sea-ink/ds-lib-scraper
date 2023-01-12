from io import StringIO
from lxml import etree

import scrapy
from scrapy.crawler import CrawlerProcess


class NoneFilter:
    def __init__(self, feed_options):
        self.feed_options = feed_options


class SklearnScraper(scrapy.Spider):
    parser = etree.HTMLParser()
    name = "sklearn"
    # starting URL
    start_urls = [
        'https://scikit-learn.org/stable/modules/classes.html'

    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
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
            yield scrapy.Request(url, callback=self.parse_data, meta={'name': name})


    def parse_data(self, response):
        # fix description
        description = "".join(response.xpath('(//dd//p)[1]//text()').getall()),
        description = str(description).replace("\n", " ").replace("('", "").replace("',)", "")

        # put separated parameters together
        html_params = response.xpath('(//dt[@class="sig sig-object py"])[1]//em[@class="sig-param"]').getall()
        edited_params = []
        problematic_parameter = ""
        for separated_html_params in html_params:
            parsed_elem = etree.parse(StringIO(separated_html_params), self.parser)
            elem_parts = parsed_elem.xpath("//text()")
            param = ""
            for param_part in elem_parts:
                param_part = param_part.replace(",", "﹐")
                param = param + param_part
            if "ngram_range" in param and "(" in param and ")" not in param:
                problematic_parameter = param+"﹐"
            elif ")" in param and len(problematic_parameter) != 0:
                problematic_parameter = problematic_parameter + param
                edited_params.append(problematic_parameter)
                problematic_parameter = ""
            else:
                edited_params.append(param)
        #title = response.xpath('//dt[@class="sig sig-object py"]/@id').get()


        yield {
            "title": "sklearn." + response.meta['name'],
            "description": description,
            "link": response.request.url,
            "parameters": edited_params
        }


process = CrawlerProcess()
process.crawl(SklearnScraper)
process.start()

# scraping in terminal: scrapy shell link


