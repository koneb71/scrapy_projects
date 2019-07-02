# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
import pandas as pd

from reisa_com.items import ProfileItem


class ReisaSpider(CrawlSpider):
    name = 'reisa'
    allowed_domains = ['reisa.com.au']

    def start_requests(self):
        requests = []
        for char in 'abcdefghijklmnopqrstuvwxyz1234567890':
            requests.append(Request("https://www.reisa.com.au/find-an-approved-reisa-agency/search/?command=getresults&SearchTerm=" + char, callback=self.parse_agencies_links))
        return requests

    def parse_agencies_links(self, response):
        requests = []

        for link in response.xpath("//*[@class='searchResults']/td[3]/a/@href").extract():
            requests.append(Request(link, callback=self.parse_profile))
        return requests

    def parse_profile(self, response):
        item = ItemLoader(ProfileItem(), response)

        item.add_xpath("company", "//h2/text()")
        item.add_xpath("contact_name", "//h3/text()")
        item.add_xpath("email", "//*[@id='memberdetailtable']//tr/th[contains(text(), 'Email:')]/following-sibling::td[1]/a/@href")
        item.add_xpath("phone", "//*[@id='memberdetailtable']//tr/th[contains(text(), 'Phone:')]/following-sibling::td[1]//text()")
        item.add_xpath("fax", "//*[@id='memberdetailtable']//tr/th[contains(text(), 'Fax:')]/following-sibling::td[1]//text()")
        item.add_xpath("website", "//*[@id='memberdetailtable']//tr/th[contains(text(), 'Web:')]/following-sibling::td[1]/a/@href")

        return item.load_item()
