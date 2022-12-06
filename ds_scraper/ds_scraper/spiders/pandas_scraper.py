import scrapy
from scrapy.crawler import CrawlerProcess


class NoneFilter:

    def __init__(self, feed_options):
        self.feed_options = feed_options

    def accepts(self, item):
        if len(item["description"]) == 0:
            return False
        return True


class PandasSpider(scrapy.Spider):
    name = "pandas"
    start_urls = [
        'https://pandas.pydata.org/docs/reference/index.html'

    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "COOKIES_ENABLED": False,
        "FEEDS": {
            "items.csv": {
                "format": "csv",
                "item_filter": NoneFilter
            },

        }
    }

    f = open("items.csv", 'w').close()

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
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        modified_descr = "".join(response.xpath('//dl[@class="py function" or @class="py method" or @class="py exception"]//dd//p/descendant-or-self::*/text()').getall())
        index = modified_descr.find(".")
        description = modified_descr[:index+1]
        yield {
            "title": response.xpath('//dt[@class="sig sig-object py"]/@id').get(),
            "description": description,
            "link": response.request.url
        }


process = CrawlerProcess()
process.crawl(PandasSpider)
process.start()

# TODO add default paramenters


