# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from asda.items import AsdaItem


class AsdaComSpider(CrawlSpider):
    name = 'asda_com'
    base_url = "https://groceries.asda.com"
    allowed_domains = ['asda.com']
    sites = [
        'https://groceries.asda.com/special-offers/all-offers/by-category/102269',
        'https://groceries.asda.com/special-offers/all-offers/by-category/111556'
    ]

    def start_requests(self):
        requests = []
        for site in self.sites:
            requests.append(Request(site, callback=self.parse_pages))
        return requests

    def parse_pages(self, response):
        requests = []

        last_page = response.xpath("//*[contains(@class, 'lastPage')]/text()").get()
        if last_page:
            last_page = int(last_page)

            for num in range(0, last_page + 1):
                requests.append(Request("%s?No=%s" % (response.url, num * 60)))
        return requests

    def parse(self, response):
        lists = []
        for res in response.xpath("//*[@class='product-list']//div[contains(@class, 'productListing')]"):
            item = ItemLoader(AsdaItem(), res)

            item.add_value('Master_URL', response.url)
            item.add_value('URL',
                           self.base_url + ''.join(res.xpath(".//*[@class='product-content']/span/a/@href").get()))
            item.add_xpath('Name', ".//*[@class='product-content']/span//text()")
            item.add_xpath('Image', ".//*[@class='imgContainer']/a/img/@src")
            item.add_xpath('Price', ".//*[@class='price']/span[last()]/text()")
            item.add_xpath('Offer', ".//*[@class='offer-2for3']//text()")
            item.add_xpath('Offer', ".//*[@class='ping-offer-finalValue']//text()")
            item.add_xpath('Stock', ".//*[contains(@class, 'fav-test-item')]/text()")
            item.add_value('Data_Large', res.xpath('.').get())
            item.add_value('Dtime', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            lists.append(item.load_item())
        return lists
