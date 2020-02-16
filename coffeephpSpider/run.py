# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())
# 执行所有 spider
for spider_name in process.spider_loader.list():
   process.crawl(spider_name)
process.start()