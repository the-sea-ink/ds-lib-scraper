import scrapy
from scrapy.crawler import CrawlerProcess


class ScipySpider(scrapy.Spider):
    name = "scipy"
    start_urls = [
        'https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.whiten.html'

    ]
    f = open("bar.json", 'w').close()

    def parse(self, response):
        info = yield {
            "short_title": response.xpath('//section/dl/dt/span[@class="sig-name descname"]/span/text()').get(),
            "title": response.xpath('//section/h1/text()').get(),
            "description": response.xpath('//dd/p/text()')[0].get(),
        }


process = CrawlerProcess(settings={
    "FEEDS": {
        "items.csv": {"format": "csv"}
    },
})

process.crawl(ScipySpider)
process.start()
