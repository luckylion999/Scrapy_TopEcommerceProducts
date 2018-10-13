from urllib.parse import urljoin
from Scrapy_TopEcommerceProducts.items import ProductItem
import scrapy


class Netaporter(scrapy.Spider):
    name = "netaporter_scraper"
    allowed_domains = ["www.net-a-porter.com"]
    start_urls = ['https://www.net-a-porter.com/us/en/d/shop/Clothing/All?pn=1&npp=60&image_view=product&dscroll=0']

    def parse(self, response):
        link_list = response.xpath('//ul[@id="subnav"]/li/a/@href').extract()
        department_list = response.xpath('//ul[@id="subnav"]/li/a/span/text()').extract()
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
        title_list = response.xpath('//ul[@class="products"]/li/div[@class="description"]/a/@title').extract()
        image_list = response.xpath('//ul[@class="products"]/li/div[@class="product-image"]/a/img/@data-src').extract()
        link_list = response.xpath('//ul[@class="products"]/li/div[@class="description"]/a/@href').extract()
        length = len(title_list)
        if length > 20:
            length = 20
        for i in range(length):
            item = response.meta.get('item')
            item['rank'] = i+1
            item['title'] = title_list[i]
            item['image'] = 'https:' + image_list[i]
            item['link'] = urljoin(response.url, link_list[i])
            yield item
