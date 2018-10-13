from urllib.parse import urljoin
from Scrapy_TopEcommerceProducts.items import ProductItem
import scrapy


class Farfetch(scrapy.Spider):
    name = "farfetch_scraper"
    allowed_domains = ["www.farfetch.com"]
    start_urls = ['https://www.farfetch.com']
    CATEGORY_URLS = [
        'https://www.farfetch.com/sets/women/best-sellers-women.aspx?view=180&scale=280&category=135971',
        'https://www.farfetch.com/sets/women/best-sellers-women.aspx?view=180&scale=280&category=135967',
        'https://www.farfetch.com/sets/women/best-sellers-women.aspx?view=180&scale=280&category=137175',
        'https://www.farfetch.com/sets/women/best-sellers-women.aspx?view=180&scale=280&category=135977',
        'https://www.farfetch.com/sets/women/best-sellers-women.aspx?view=180&scale=280&category=136301'
    ]
    DEPARTMENT_NAMES = [
        'Bags',
        'Clothing',
        'Fine Jewellery',
        'Jewelry',
        'Shoes'
    ]

    def start_requests(self):
        for i in range(len(self.CATEGORY_URLS)):
            item = ProductItem()
            item['department'] = self.DEPARTMENT_NAMES[i]
            yield scrapy.Request(
                url=self.CATEGORY_URLS[i],
                callback=self.parse_products,
                meta={'item': item}
            )

    def parse_products(self, response):
        title_list = response.xpath('//p[@itemprop="name"]/text()').extract()
        image_list = response.xpath('//img[@itemprop="image"]/@data-img').extract()
        link_list = response.xpath('//a[@itemprop="url"]/@href').extract()
        length = len(title_list)
        if length > 20:
            length = 20
        for i in range(length):
            item = response.meta.get('item')
            item['rank'] = i+1
            item['title'] = title_list[i]
            item['image'] = image_list[i]
            item['link'] = urljoin(response.url, link_list[i])
            yield item
