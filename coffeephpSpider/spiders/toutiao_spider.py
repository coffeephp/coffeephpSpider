import scrapy
from scrapy_splash import SplashRequest
from coffeephpSpider.items import ToutiaoItem

class ToutiaoSpider(scrapy.Spider):
    name = "toutiao"
    allowed_domains = ["toutiao.io"]
    start_urls = [
        "https://toutiao.io/c/arch",
        "https://toutiao.io/c/be",
        "https://toutiao.io/posts/hot/7",
        "https://toutiao.io/subjects/46756"
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="main"]/div[2]/div[1]/div'):
            item = ToutiaoItem()
            item['title'] = sel.xpath('div[2]/h3/a/text()').extract()
            item['url'] = sel.xpath('div[2]/h3/a/@href').extract()
            yield item