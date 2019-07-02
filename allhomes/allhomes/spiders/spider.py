# -*- coding: utf-8 -*-
import json
import os
import sys

from scrapy import Request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
import pandas as pd

from allhomes.items import AllhomesItem


class SpiderSpider(CrawlSpider):
    name = "spider"
    allowed_domains = ["allhomes.com.au"]

    def start_requests(self):
        data = pd.read_csv(open("/Users/neiellcare/Documents/Grant Scrapy Projects/realestate_com/au_postcodes.csv"))
        postcodes = list(set(data['postcode']))
        requests = []
        for code in postcodes[:2]:
            requests.append(Request("https://www.allhomes.com.au/wsvc/agency/search/autocomplete?query=%s" % code, callback=self.parse_location_links))
        return requests

    def parse_location_links(self, response):
        base_url = "https://www.allhomes.com.au/agents/results/"
        data = json.loads(response.body)['Division']
        requests = []
        for location in data:
            url =  base_url + "%s-%s-%s/" % (str(location['locatedInSuburb']).replace(" ", "-").lower(),
                                            str(location['state']).lower(), str(location['postcode']))
            requests.append(Request(url, callback=self.parse_agencies_links))
        return requests

    def parse_agencies_links(self, response):
        requests = []

        for agency in response.xpath("//*[@class='allhomes-agency-search-results__result-card-container']"):
            url = agency.xpath(".//a[@class='allhomes-agency-search-results__result-card-anchor']/@href").extract()[0]
            requests.append(Request(url, callback=self.parse))
        return requests


    def parse(self, response):
        item = ItemLoader(AllhomesItem(), response)

        parse_string = ''.join(response.body).split('window.renderizrData["agencyProfile"] = ')
        data = json.loads(parse_string[1].split(";</script>")[0])

        item.add_value("company", data['agency']['name'])
        item.add_value("street", data['agency']['address']['street'])
        item.add_value("suburb", data['agency']['address']['suburb'])
        item.add_value("state", data['agency']['address']['state'])
        item.add_value("postcode", data['agency']['address']['postcode'])
        item.add_value("phone", data['agency']['phone'])
        item.add_value("website", data['agency']['website'])

        return item.load_item()
