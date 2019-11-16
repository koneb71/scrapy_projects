# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
import MySQLdb
from MySQLdb.cursors import DictCursor

from asda.items import AsdaItem
from asda.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB


class AsdaComSpider(CrawlSpider):
    name = 'asda_com'
    base_url = "https://groceries.asda.com"
    allowed_domains = ['asda.com']
    sites = [
        'https://groceries.asda.com/special-offers/all-offers/by-category/102269',
        'https://groceries.asda.com/special-offers/all-offers/by-category/111556'
    ]

    def __init__(self, store='Asda', url=None, *args, **kwargs):
        super(AsdaComSpider, self).__init__(*args, **kwargs)
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

        last_page = response.xpath("//*[contains(@class, 'lastPage')]/text()").get()
        if last_page:
            last_page = int(last_page)

            for num in range(0, last_page + 1):
                requests.append(Request("%s?No=%s" % (response.url, num * 60), callback=self.parse_items))
        return requests

    def parse_items(self, response):
        lists = []
        for res in response.xpath("//*[@class=' co-product-list']//div[contains(@class, 'co-product')]"):
            item = ItemLoader(AsdaItem(), res)

            item.add_value('Master_URL', response.url)
            item.add_value('URL',
                           self.base_url + ''.join(res.xpath(".//*[@class='co-item__col1']/a/@href").get()))
            item.add_xpath('Name', ".//*[@class='co-product__title']//text()")
            item.add_xpath('Image', ".//*[@class='co-item__col1']/a/img/@src")
            item.add_xpath('Price', ".//*[@class='co-product__price']/text()")
            item.add_xpath('Offer', ".//*[@class='link-save-banner-large__meat-sticker']//text()")
            item.add_xpath('Stock', ".//*[@class='fco-product-quantity__add-butt-cont']/text()")
            item.add_value('Data_Large', res.xpath('.').get())
            item.add_value('Dtime', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            lists.append(item.load_item())
        return lists
