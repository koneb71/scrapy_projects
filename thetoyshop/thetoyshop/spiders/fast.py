# -*- coding: utf-8 -*-
import json
import math
import re

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from thetoyshop.items import ThetoyshopItem
from thetoyshop.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB
import MySQLdb
from MySQLdb.cursors import DictCursor

class FastSpider(CrawlSpider):
    name = 'fast'
    allowed_domains = ['thetoyshop.com']
    # start_urls = ['https://www.thetoyshop.com/c/present-finder?q=%3Arelevance%3Aprice%3A%25C2%25A30%2B-%2B%25C2%25A314.99%3Aprice%3A%25C2%25A315%2B-%2B%25C2%25A329.99%3Aprice%3A%25C2%25A330%2B-%2B%25C2%25A344.99%3Aprice%3A%25C2%25A345%2B-%2B%25C2%25A359.99%3Aprice%3A%25C2%25A360%2B-%2B%25C2%25A374.99%3Aprice%3A%25C2%25A375%252B']

    def __init__(self, store='toyshop', url=None, *args, **kwargs):
        super(FastSpider, self).__init__(*args, **kwargs)
        self.db = MySQLdb.connect(host=MYSQL_HOST,
                                  user=MYSQL_USERNAME,
                                  passwd=MYSQL_PASSWORD,
                                  db=MYSQL_DB, cursorclass=DictCursor)
        self.store = store
        self.url = url

    def start_requests(self):
        if self.url:
            return Request(self.url, callback=self.parse_pages)

        requests = []
        c = self.db.cursor()
        c.execute("""Select url from w_scrape_urls where store = %s""", (self.store,))
        sites = c.fetchall()
        for site in sites:
            requests.append(Request(site['url'], callback=self.parse_pages))

        c.close()
        return requests

    def parse_pages(self, response):
        requests = []
        total_products = int(str(response.xpath("//*[@class='pagination-bar-results']/text()").get()).replace(" Products found", ''))
        total_pages = int(math.floor(total_products / 36))
        url = "https://www.thetoyshop.com/c/present-finder?q=%3Arelevance%3Aprice%3A%25C2%25A30%2B-%2B%25C2%25A314.99%3Aprice%3A%25C2%25A315%2B-%2B%25C2%25A329.99%3Aprice%3A%25C2%25A330%2B-%2B%25C2%25A344.99%3Aprice%3A%25C2%25A345%2B-%2B%25C2%25A359.99%3Aprice%3A%25C2%25A360%2B-%2B%25C2%25A374.99%3Aprice%3A%25C2%25A375%252B&page={}"

        for page in range(1, total_pages+1):
            requests.append(
                Request(url.format(str(page)), callback=self.parse_items, dont_filter=True)
            )
        requests.append(
            Request(response.url, callback=self.parse_items, dont_filter=True)
        )
        return requests

    def parse_items(self, response):
        requests = []
        for i in response.xpath("//*[@class='product-item']"):
            item = ItemLoader(ThetoyshopItem(), i)

            item.add_xpath('URL', ".//*[@class='details']/a[@class='name']/@href")
            item.add_xpath('Name', ".//a[@class='name']/text()")
            item.add_xpath('Image', ".//a[@class='thumb']/img/@src")
            item.add_xpath('Price', ".//*[@class='details']/a[@class='name']/@data-productprice")
            item.add_value('Stock', "in stock" if str(i.xpath(".//a[@class='name']/@data-instock").get()) == "true" else "out of stock")
            requests.append(item.load_item())

        return requests