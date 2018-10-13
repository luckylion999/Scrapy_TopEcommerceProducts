from urllib.parse import urljoin
from Scrapy_TopEcommerceProducts.items import ProductItem
import scrapy
import re


class Amazon(scrapy.Spider):
    name = "amazon_scraper"
    allowed_domains = ["amazon.com"]
    START_URL = 'https://www.amazon.com/'
    PAGE_URL = [
        'https://www.amazon.com/Best-Sellers/zgbs/fashion/ref=zg_bs_nav_0',
        'https://www.amazon.com/Best-Sellers/zgbs/fashion/ref=zg_bs_pg_2?_encoding=UTF8&pg=2',
        'https://www.amazon.com/Best-Sellers-Womens-Clothing/zgbs/fashion/1040660',
        'https://www.amazon.com/Best-Sellers-Womens-Clothing/zgbs/fashion/1040660/ref=zg_bs_pg_2?_encoding=UTF8&pg=2'
    ]
    HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/67.0.3396.99 Safari/537.36'
              }

    def start_requests(self):
        yield scrapy.Request(
            url=self.START_URL,
            callback=self.parse,
            headers=self.HEADER
        )

    def parse(self, response):
        for url in self.PAGE_URL:
            yield scrapy.Request(
                url=url,
                callback=self.parse_links,
                headers=self.HEADER
            )

    def parse_links(self, response):
        href_list = response.xpath('//span[@class="aok-inline-block zg-item"]'
                                   '/a[@class="a-link-normal"]/@href').extract()
        for href in href_list:
            yield scrapy.Request(
                url=urljoin(response.url, href),
                callback=self.parse_product,
                headers=self.HEADER
            )

    def parse_product(self, response):
        item = ProductItem()
        title = response.xapth('//span[@id="productTitle"]/text()').extract_first()
        item['title'] = title if title else None
        image = response.xpath('https://images-na.ssl-images-amazon.com/images/I/518qIa6a8WL._UY741_.jpg').extract_first()
        item['image'] = image if image else None
        yield item
