import scrapy
from scrapy_splash import SplashRequest
from coffeephpSpider.items import JuejinItem

class JuejinSpider(scrapy.Spider):
    name = "juejin"
    allowed_domains = ["juejin.im"]
    start_urls = [
        "https://juejin.im/tag/Linux",
        "https://juejin.im/tag/Nginx",
        "https://juejin.im/tag/MySQL",
        "https://juejin.im/tag/PHP",
        "https://juejin.im/tag/Laravel",
        "https://juejin.im/tag/Swoole",
        "https://juejin.im/tag/Redis",
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="juejin"]/div[2]/main/div/div[2]/ul/li'):
            item = JuejinItem()
            item['title'] = sel.xpath('div/div/a/div/div/div[2]/a/text()').extract()
            item['url'] = sel.xpath('div/div/a/div/div/div[2]/a/@href').extract()
            yield item