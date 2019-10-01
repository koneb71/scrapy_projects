# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from smythstoys.items import SmythstoysItem
from smythstoys.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB
import MySQLdb
from MySQLdb.cursors import DictCursor


class SlowSpider(CrawlSpider):
    name = 'slow'
    allowed_domains = ['smythstoys.com']
    # start_urls = ['http://smythstoys.com/']

    def __init__(self, store='smythstoys_slow', url=None, *args, **kwargs):
        super(SlowSpider, self).__init__(*args, **kwargs)
        self.db = MySQLdb.connect(host=MYSQL_HOST,
                                  user=MYSQL_USERNAME,
                                  passwd=MYSQL_PASSWORD,
                                  db=MYSQL_DB, cursorclass=DictCursor)
        self.store = store
        self.url = url

    def start_requests(self):
        requests = []
        c = self.db.cursor()
        c.execute("""Select url from w_scrape_urls where store = %s""", (self.store,))
        sites = c.fetchall()
        for site in sites:
            requests.append(Request(site['url'], self.parse_item))
        c.close()
        return requests

    def parse_item(self, response):
        item = ItemLoader(SmythstoysItem(), response)

        item.add_value('URL', response.url)
        item.add_xpath('EAN', "//*[@data-flix-ean]/@data-flix-ean")
        item.add_value('Slow_scrape', "1")
        return item.load_item()
