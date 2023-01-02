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


class PandasSpider(scrapy.Spider):
    parser = etree.HTMLParser()
    name = "pandas"
    start_urls = [
        'https://pandas.pydata.org/docs/reference/index.html'

    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "COOKIES_ENABLED": False,
        "FEEDS": {
            "pandas.csv": {
                "format": "csv",
                "item_filter": NoneFilter
            },

        }
    }

    f = open("pandas.csv", 'w').close()

    def parse(self, response):
        links = response.xpath(
            '//div[@class="toctree-wrapper compound"]//li[@class="toctree-l1"]/a[@class="reference internal"]/@href').getall()
        for link in links:
            url = "https://pandas.pydata.org/docs/reference/" + link
            yield scrapy.Request(url, callback=self.parse_function_names)

    def parse_function_names(self, response):
        names = response.xpath(
            '//table[@class="autosummary longtable table autosummary"]/tbody/tr/td/p/a[@class="reference internal"]/@title').getall()
        for name in names:
            url = "https://pandas.pydata.org/docs/reference/api/" + name + ".html"
            #if url == 'https://pandas.pydata.org/docs/reference/api/pandas.io.json.build_table_schema.html':
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        # put separated parameters together
        html_params = response.xpath('//em[@class="sig-param"]').getall()
        edited_params = []
        for separated_html_params in html_params:
            parsed_elem = etree.parse(StringIO(separated_html_params), self.parser)
            elem_parts = parsed_elem.xpath("//text()")
            param = ""
            for param_part in elem_parts:
                param_part = param_part.replace(",", "﹐")
                param = param + param_part
            edited_params.append(param)

        yield {
            "title": response.xpath('//dt[@class="sig sig-object py"]/@id').get(),
            "description": "".join(response.xpath('(//dl[@class="py function" or @class="py method" or @class="py exception"]//dd//p)[1]/descendant-or-self::*/text()').getall()),
            "link": response.request.url,
            "parameters": edited_params
        }


process = CrawlerProcess()
process.crawl(PandasSpider)
process.start()




