import scrapy
from scrapy.crawler import CrawlerProcess


class NoneFilter:

    def __init__(self, feed_options):
        self.feed_options = feed_options

    def accepts(self, item):
        if len(item["description"]) == 0 and len(item("parameters")) == 0:
            return False
        return True


class PandasSpider(scrapy.Spider):
    name = "pandas"
    start_urls = [
        'https://pandas.pydata.org/docs/reference/index.html'

    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
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
        # shorten description to just one sentence
        description = "".join(response.xpath('//dl[@class="py function" or @class="py method" or @class="py exception"]//dd//p/descendant-or-self::*/text()').getall())
        index = description.find(".")
        modified_description = description[:index+1]

        # put parameters together
        params = response.xpath('//em[@class="sig-param"]//span[@class="pre"]/text()').getall()
        edited_params = []
        to_skip = ["*", "**", "args", "kwargs", "="]
        for prev_param, param, next_param in zip(params, params[1:], params[2:]):
            if param == "=":
                edited_params.append(str(prev_param) + str(param) + str(next_param))
            elif param == "*" and next_param == "args":
                edited_params.append(str(param) + str(next_param))
            elif param == "**" and next_param == "kwargs":
                edited_params.append(str(param) + str(next_param))
            elif prev_param or next_param in to_skip:
                continue
            else:
                edited_params.append(param)


        yield {
            "title": response.xpath('//dt[@class="sig sig-object py"]/@id').get(),
            "description": modified_description,
            "link": response.request.url,
            "parameters": edited_params
        }


process = CrawlerProcess()
process.crawl(PandasSpider)
process.start()



