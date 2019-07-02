# -*- coding: utf-8 -*-
import json
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
import pandas as pd

from domain_com.items import ProfileItem


class DomainSpider(CrawlSpider):
    name = 'domain'
    allowed_domains = ['domain.com.au']
    base_url = "https://www.domain.com.au"

    def start_requests(self):
        data = pd.read_csv(open("/Users/neiellcare/Documents/Grant Scrapy Projects/realestate_com/au_postcodes.csv"))
        requests = []
        for code in data.to_dict(orient='records')[:2]:
            #https://www.domain.com.au/real-estate-agencies/south-melbourne-vic-3205/
            requests.append(Request("https://www.domain.com.au/real-estate-agencies/" + str(code['suburb']).replace(" ", "-").lower() + "-" + str(code['state']).replace(" ", "-").lower() + '-' + str(code['postcode'])+ "/", callback=self.parse_agencies))
        #requests.append(Request("https://www.domain.com.au/real-estate-agencies/moranrealty-17059/", callback=self.parse_profile))
        return requests

    def parse_agencies(self, response):
        try:
            resp = str(response.body).encode("utf-8").decode('unicode-escape').split("<script>window['__domain_group/APP_PROPS'] = ")[1]
        except:
            resp = str(response.body).split("<script>window['__domain_group/APP_PROPS'] = ")[1]
        resp = resp.split("};")[0] + "}"
        data = json.loads(resp)
        requests = []

        for profile in data['feCoAgencyProfileSearchResults']['props']['initialFetchState']['results']:
            requests.append(Request(self.base_url+profile['profileUrl'], callback=self.parse_profile))

        a_tag = response.xpath("//*[@class='paginator']/a")

        for tag in a_tag:
            if "next" in tag.xpath("./span//text()").extract():
                next_link_param = ''.join(tag.xpath("./@href").extract())
                url = urlparse(response.url)
                requests.append(Request(url.scheme+"://"+url.netloc+url.path+next_link_param, callback=self.parse_agencies))
        return requests


    def parse_profile(self, response):
        try:
            resp = str(response.body).encode("utf-8").decode('unicode-escape').split("<script>window['__domain_group/APP_PROPS'] = ")[1]
        except:
            resp = str(response.body).split("<script>window['__domain_group/APP_PROPS'] = ")[1]
        resp = resp.split("};")[0] + "}"
        data = json.loads(resp)
        info = data['fePaTradeProfile']['props']['agencyDetails']

        item = ItemLoader(ProfileItem())

        item.add_value('company', info['name'])
        item.add_value('phone', info['phoneNumber'])
        item.add_value('email', info['email'])
        item.add_value('website', info['social']['web'])
        print(info['address'])
        item.add_value('street', ', '.join(str(info['address']).split(',')[:-1]))
        item.add_value('suburb', ''.join(''.join(str(info['address']).split(',')[-1]).split(' ')[:-2]))
        item.add_value('state', str(info['address']).split(' ')[-2])
        item.add_value('postcode', str(info['address']).split(' ')[-1])

        return item.load_item()



