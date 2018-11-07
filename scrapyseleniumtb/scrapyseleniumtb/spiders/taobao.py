# -*- coding: utf-8 -*-
import scrapy
from scrapyseleniumtb.items import ProductItem
from urllib.parse import quote


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for key in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 0):
                url = self.base_url + quote(key)
                yield scrapy.Request(url=url, callback=self.parse, meta={"page": page}, dont_filter=True)

    def parse(self, response):
        if response.status == 200:
            products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"]//div[contains(@class, "item")]')
            for product in products:
                item = ProductItem()
                # item['image'] = 'https:' + str(product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract_first()).strip()
                item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
                yield item
        else:
            print("status is 500")