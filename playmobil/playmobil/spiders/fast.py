# -*- coding: utf-8 -*-
from requests.utils import quote

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from playmobil.items import PlaymobilItem
from playmobil.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB
import MySQLdb
from MySQLdb.cursors import DictCursor


class FastSpider(CrawlSpider):
    name = 'fast'
    allowed_domains = ['playmobil.co.uk']
    # start_urls = ['https://www.playmobil.co.uk/onlineshop/products/knights']
    image_url = "https://media.playmobil.com/i/playmobil/{}_product_detail/{}?locale=en-GB,en,*&$product_search_hit_tile_xl$&strip=true&qlt=80&fmt.jpeg.chroma=1,1,1&unsharp=0,1,1,7&fmt.jpeg.interlaced=true"
    load_more = "https://www.playmobil.co.uk/onlineshop/products/knights?srule=Topseller&start={}&modus=gridonly&format=ajax"

    def __init__(self, store='playmobil', url=None, *args, **kwargs):
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
        items = []
        offset = 12
        max_page = int(response.xpath("//*[@id='search-result-content']/@data-maxpage").get())

        items += self.parse_items(response.xpath("//*[@class='product-tile']"))
        for index in range(0, max_page):
            items.append(
                Request(self.load_more.format(offset), dont_filter=True, callback=self.parse_load_more)
            )
            offset += 12
        return items

    def parse_load_more(self, response):
        return self.parse_items(response.xpath("//*[@class='product-tile']"))

    def parse_items(self, response):
        items = []
        for res in response:
            item = ItemLoader(PlaymobilItem(), res)

            item.add_xpath("URL", ".//*[@class='product-name']//a/@href")
            item.add_xpath("Name", ".//*[@class='product-name']//text()")
            item.add_value("Image", self.image_url.format(str(res.xpath("./@data-itemid").get()), quote(
                res.xpath(".//*[@class='product-name']//a/@title").get(), safe='')))
            item.add_xpath("Price", ".//*[@class='price-sales ']/text()")

            items.append(item.load_item())
        return items
