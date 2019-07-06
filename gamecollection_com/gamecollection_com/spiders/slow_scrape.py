# -*- coding: utf-8 -*-
import MySQLdb
from MySQLdb.cursors import DictCursor
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from gamecollection_com.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB
from gamecollection_com.items import GamecollectionComItem


class SlowScrapeSpider(CrawlSpider):
    name = 'slow_scrape'
    allowed_domains = ['thegamecollection.net']
    base_url = 'https://www.thegamecollection.net/ps4/'

    # start_urls = ['https://www.thegamecollection.net/ps4/']

    def __init__(self, store='gamecollection_slow', url=None, *args, **kwargs):
        super(SlowScrapeSpider, self).__init__(*args, **kwargs)
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
            requests.append(Request(site['url'], self.parse_item))
        c.close()
        return requests

    def parse_item(self, response):
        item = ItemLoader(GamecollectionComItem(), response)

        item.add_value('Master_URL', response.url)
        item.add_xpath('Barcode', "//th[text()='Barcode']/following-sibling::td[1]/text()")
        item.add_value('Slow_scrape', "1")
        return item.load_item()

