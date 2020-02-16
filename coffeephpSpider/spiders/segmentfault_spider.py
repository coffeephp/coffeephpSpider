import scrapy

from coffeephpSpider.items import SegmentfaultItem

class SegmentfaultSpider(scrapy.Spider):
    name = "segmentfault"
    allowed_domains = ["segmentfault.com"]
    start_urls = [
        "https://segmentfault.com/t/php/blogs",
        "https://segmentfault.com/t/mysql/blogs",
        "https://segmentfault.com/t/redis/blogs",
        "https://segmentfault.com/t/nginx/blogs",
        "https://segmentfault.com/t/linux/blogs",
        "https://segmentfault.com/t/laravel/blogs",
        "https://segmentfault.com/t/swoole/blogs",
    ]

    def parse(self, response):
        for sel in response.xpath('//*[@id="blog"]/section'):
            item = SegmentfaultItem()
            item['title'] = sel.xpath('div[@class="summary"]/h2/a/text()').extract()
            item['url'] = sel.xpath('div[@class="summary"]/h2/a/@href').extract()
            yield item
