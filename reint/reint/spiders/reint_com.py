# -*- coding: utf-8 -*-
import addressify
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from reint.items import ReintItem


class ReintComSpider(CrawlSpider):
    name = "reint_com"
    allowed_domains = ["reint.com.au"]
    base_url = "https://reint.com.au"

    def start_requests(self):
        requests = []

        for page in range(0, 111, 10):
            requests.append(Request("%s/find-an-agency?start=%s" % (self.base_url, page), callback=self.parse_agencies_links))
        return requests

    def parse_agencies_links(self, response):
        agencies = []

        for agency in response.xpath("//a[@class='splms-person-title']/@href").extract():
            agencies.append(Request(self.base_url+agency, callback=self.parse))
        return agencies

    def parse(self, response):
        item = ItemLoader(ReintItem(), response)

        item.add_xpath("company", "//*[@class='specialist-name']/h3/text()")
        item.add_xpath("phone", "//*[@class='specialist-contact-info']/p/text()")
        item.add_xpath("email", "//*[@class='specialist-contact-info']/a/text()")
        item.add_xpath("website", "//*[@class='specialist-contact-info']/ul//a/@href")

        try:
            address = ''.join(response.body).split('Street Address: ')[1]
            address = address.split("<br />")[0]
            get_address = addressify.Client(api_key="3dad1556-e357-44ec-b40f-bc54cb22e9c6").parse_address(
                ''.join(address))

            item.add_value("street", get_address.street_line)
            item.add_value("suburb", get_address.suburb)
            item.add_value("state", get_address.state)
            item.add_value("postcode", get_address.postcode)
        except:
            address = ''.join(response.body).split('Street Address: ')[1]
            try:
                address = address.split("</div>")[0]

                get_address = addressify.Client(api_key="3dad1556-e357-44ec-b40f-bc54cb22e9c6").parse_address(
                    ''.join(address))

                item.add_value("street", get_address.street_line)
                item.add_value("suburb", get_address.suburb)
                item.add_value("state", get_address.state)
                item.add_value("postcode", get_address.postcode)
            except:
                print("No address")



        return item.load_item()
