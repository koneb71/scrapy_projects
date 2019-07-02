# -*- coding: utf-8 -*-
import json
import logging
import os
import sys

from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
import pandas as pd

from realestate_com.items import RealestateComItem

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class RealestateSpider(CrawlSpider):
    name = "realestate"
    allowed_domains = ["realestate.com.au"]
    base_url = "https://www.realestate.com.au"

    def start_requests(self):
        data = pd.read_csv(open("/Users/neiellcare/Documents/Grant Scrapy Projects/realestate_com/au_postcodes.csv"))
        postcodes = list(set(data['postcode']))
        requests = []
        for code in postcodes[:1]:
            requests.append(Request("https://suggest.realestate.com.au/consumer-suggest/suggestions?max=20&query=" + str(code) + "&type=suburb%2Cprecinct&src=homepage", callback=self.parse_location_links))
        return requests

    def parse_location_links(self, response):
        requests = []
        data = json.loads(response.body)
        for loc in data['_embedded']['suggestions']:
            link = self.base_url + "/find-agent/in-%s,+%s+%s" % (str(loc['source']['name']).replace(" ", "+").lower(), loc['source']['state'], loc['source']['postcode'] )
            requests.append(Request(link.replace(",", '%2c')+"/list-1?source=find-agency-location", callback=self.parse_agencies))
        return requests

    def parse_agencies(self, response):
        requests = []
        for agency in response.xpath("//*[@class='listingInfo']"):
            item = ItemLoader(RealestateComItem(), agency)

            item.add_xpath("company", ".//h2//text()")
            item.add_xpath("street", ".//span[@class='street-address']/text()")
            item.add_xpath("suburb", ".//span[@class='locality']/text()")
            item.add_xpath("state", ".//span[@class='region']/text()")
            item.add_xpath("postcode", ".//span[@class='postal-code']/text()")
            item.add_xpath("phone", ".//li[@class='tel phone']/a/@data-value")
            item.add_xpath("website", ".//li[@class='url web last']/a/@href")

            requests.append(item.load_item())

        if response.xpath("//*[@class='nextLink']/a/@href").extract_first():
            requests.append(Request(self.base_url+str(response.xpath("//*[@class='nextLink']/a/@href").extract_first()), callback=self.parse_agencies))
        return requests