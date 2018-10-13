# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    department = scrapy.Field()
    rank = scrapy.Field()
    link = scrapy.Field()
