# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider


class ReiqSpider(CrawlSpider):
    name = 'reiq'
    allowed_domains = ['reiq.com']
    start_urls = ['http://reiq.com/']

    def parse(self, response):
        pass
