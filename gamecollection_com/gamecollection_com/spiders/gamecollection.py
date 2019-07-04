# -*- coding: utf-8 -*-
import math

import MySQLdb
from MySQLdb.cursors import DictCursor
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from gamecollection_com.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB

from gamecollection_com.items import GamecollectionComItem


class GamecollectionSpider(CrawlSpider):
    name = 'gamecollection'
    allowed_domains = ['thegamecollection.net']
    base_url = 'https://www.thegamecollection.net/ps4/'

    # start_urls = ['https://www.thegamecollection.net/ps4/']

    def __init__(self, store='gamecollection', url=None, *args, **kwargs):
        super(GamecollectionSpider, self).__init__(*args, **kwargs)
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
            requests.append(Request(site['url'], self.parse_pages))
        c.close()
        return requests

    def parse_pages(self, response):
        requests = []
        total_items = int(response.xpath("//*[contains(@class, 'amount--has-pages')]//strong[last()]/text()").get())
        limit_per_page = 48
        total_pages = math.ceil(total_items / limit_per_page) + 1

        for page in range(1, total_pages):
            requests.append(
                Request('%s?limit=%s&p=%s' % (self.base_url, limit_per_page, page), callback=self.parse_items)
            )
        return requests

    def parse_items(self, response):
        lists = []

        for res in response.xpath("//*[@class='item']"):
            item = ItemLoader(GamecollectionComItem(), res)

            item.add_value('Master_URL', response.url)
            item.add_xpath('URL', "./a/@href")
            item.add_xpath('Name', ".//*[@class='product-name']/text()")
            item.add_xpath('Image', ".//*[@class='product-image']/img/@src")
            item.add_xpath('Price', ".//*[@class='price']/text()")
            item.add_xpath('New_or_old', ".//*[@class='condition']/span/text()")
            item.add_xpath('Stock', ".//*[@class='actions']/button/text()")
            item.add_value('Data_Large', res.xpath('.').get())

            lists.append(item.load_item())
        return lists
