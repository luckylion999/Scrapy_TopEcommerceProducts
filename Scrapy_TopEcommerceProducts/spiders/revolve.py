from urllib.parse import urljoin
from Scrapy_TopEcommerceProducts.items import ProductItem
import scrapy


class Revolve(scrapy.Spider):
    name = "revolve_scraper"
    allowed_domains = ["www.revolve.com"]
    start_urls = ['https://www.revolve.com/bestSeller/all-best-sellers/br/2022d4/?navsrc=left']

    def parse(self, response):
        link_list = response.xpath('//aside[contains(@class, "s-left-nav-container")]'
                                   '//ul[contains(@class, "ui-list")]/li/a/@href').extract()
        department_list = response.xpath('//aside[contains(@class, "s-left-nav-container")]'
                                         '//ul[contains(@class, "ui-list")]/li/a/text()').extract()
        for i in range(len(link_list)):
            if i > 0:
                item = ProductItem()
                item['department'] = department_list[i]
                yield scrapy.Request(
                    url=urljoin(response.url, link_list[i]),
                    callback=self.parse_products,
                    meta={'item': item}
                )

    def parse_products(self, response):
        title_list = response.xpath('//ul[@id="plp-prod-list"]/li//div[contains(@class, "product-titles__name")]'
                                    '/text()').extract()
        image_list1 = response.xpath('//ul[@id="plp-prod-list"]/li'
                                    '//img[contains(@class, "products-grid__image-link-img")]'
                                    '/@src').extract()
        image_list2 = response.xpath('//ul[@id="plp-prod-list"]/li'
                                    '//img[contains(@class, "products-grid__image-link-img")]'
                                    '/@data-src').extract()
        link_list = response.xpath('//ul[@id="plp-prod-list"]/li//a[contains(@class, "plp__image-link")]'
                                   '/@href').extract()
        length = len(title_list)
        if length > 20:
            length = 20
        for i in range(length):
            item = response.meta.get('item')
            item['rank'] = i+1
            item['title'] = title_list[i]
            if i < 9:
                item['image'] = image_list1[i]
            else:
                item['image'] = image_list2[i-9]
            item['link'] = urljoin(response.url, link_list[i])
            yield item
