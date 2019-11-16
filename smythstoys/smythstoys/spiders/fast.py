# -*- coding: utf-8 -*-
import json
import math

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
import lxml.html
from smythstoys.items import SmythstoysItem
from smythstoys.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB
import MySQLdb
from MySQLdb.cursors import DictCursor

class FastSpider(CrawlSpider):
    name = 'fast'
    allowed_domains = ['smythstoys.com']
    # start_urls = ['https://www.smythstoys.com/uk/en-gb/toys/c/SM0601']
    load_more = "/load-more?q=%3AukBestsellerRating&page={}"

    def __init__(self, store='smythstoys', url=None, *args, **kwargs):
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
        c.execute("""Select url from w_scrape_urls where store = %s and active = 1""", (self.store,))
        sites = c.fetchall()
        for site in sites:
            requests.append(Request(site['url'], callback=self.parse_pages))

        c.close()
        return requests

    def parse_pages(self, response):
        requests = []
        total_products = int(str(response.xpath("//h4[contains(text(), ' Results')]/text()").get()).replace(" Results", '').replace(" ", '').replace(",", ''))
        total_pages = int(math.ceil(total_products/30)+1)

        for i in range(0, total_pages+1):
            requests.append(
                Request(str(response.url) + self.load_more.format(str(i)), callback=self.parse_item, dont_filter=True)
            )
        return requests

    def parse_item(self, response):
        data = json.loads(str(response.body))['htmlContent']
        data = lxml.html.fromstring(data)
        requests = []

        for res in data.xpath("//*[contains(@class, 'product-padding')]"):
            item = ItemLoader(SmythstoysItem(), res)
            item.add_value("Name", res.xpath(".//*[@class='item-panel']/@data-name")[0])
            item.add_value("URL", res.xpath(".//*[@class='trackProduct']/@href")[0])
            item.add_value("Image", res.xpath(".//*[@class='item-panel']/@data-code")[0])
            item.add_value("Price", res.xpath(".//*[@class='item-panel']/@data-price")[0])
            item.add_value("Model", res.xpath(".//*[@class='item-panel']/@data-code")[0])

            requests.append(item.load_item())

        return requests