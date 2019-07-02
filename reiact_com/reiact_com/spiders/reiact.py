# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from reiact_com.items import ReiactComItem


class ReiactSpider(scrapy.Spider):
    name = "reiact"
    allowed_domains = ["reiact.com.au"]
    start_urls = ['https://reiact.com.au/institute-members/']

    def parse(self, response):
        res = response.xpath("//*[contains(@class, 'vc_row-flex')]")
        agencies = []

        for agency in res:
            item = ItemLoader(ReiactComItem(), agency)

            item.add_xpath("company", ".//h4//text()")
            item.add_xpath("street", ".//tbody/tr[1]/td[2]//text()")
            item.add_xpath("suburb", ".//tbody/tr[2]/td[2]//text()")
            item.add_xpath("phone", ".//tbody/tr[3]/td[2]//text()")
            item.add_xpath("website", ".//tbody/tr[4]/td[2]/a/@href")

            agencies.append(item.load_item())
        return agencies