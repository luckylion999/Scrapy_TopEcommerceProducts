import scrapy


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    department = scrapy.Field()
    rank = scrapy.Field()
    link = scrapy.Field()
