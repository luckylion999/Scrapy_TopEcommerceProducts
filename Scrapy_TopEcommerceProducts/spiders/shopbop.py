from urllib.parse import urljoin
from Scrapy_TopEcommerceProducts.items import ProductItem
import scrapy


class Shopbop(scrapy.Spider):
    name = "shopbop_scraper"
    allowed_domains = ["www.shopbop.com"]
    start_urls = ['https://www.shopbop.com/special-top-sellers/br/v=1/13055.htm']

    def parse(self, response):
        link_list = response.xpath('//ul[@class="leftNavSubcategory sub-nav"]/li/a/@href').extract()
        department_list = response.xpath('//ul[@class="leftNavSubcategory sub-nav"]/li/a/text()').extract()
        for i in range(len(link_list)):
            item = ProductItem()
            item['department'] = department_list[i].strip()
            yield scrapy.Request(
                url=urljoin(response.url, link_list[i]),
                callback=self.parse_products,
                meta={'item': item}
            )

    def parse_products(self, response):
        title_list = response.xpath('//li[contains(@id, "product-")]//div[@class="title"]/text()').extract()
        image_list = response.xpath('//li[contains(@id, "product-")]//span[@class="productBrowseMainImage"]'
                                    '/img/@src').extract()
        link_list = response.xpath('//li[contains(@id, "product-")]//a[@class=" photo"]/@href').extract()
        length = len(title_list)
        if length > 20:
            length = 20
        for i in range(length):
            item = response.meta.get('item')
            item['rank'] = i+1
            item['title'] = title_list[i].strip()
            item['image'] = image_list[i].strip()
            item['link'] = urljoin(response.url, link_list[i])
            yield item
