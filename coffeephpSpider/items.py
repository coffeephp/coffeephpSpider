# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SegmentfaultItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()

class JuejinItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()

class ToutiaoItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()