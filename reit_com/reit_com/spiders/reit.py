# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from reit_com.items import ProfileItem


class ReitSpider(CrawlSpider):
    name = 'reit'
    allowed_domains = ['reit.com.au']
    start_urls = ['http://reit.com.au/members/southern-members/',
                  'http://reit.com.au/members/northern-members/',
                  'http://reit.com.au/members/north-west-members/']

    def parse(self, response):
        requests = []
        for profile in response.xpath("//tbody/tr"):
            item = ItemLoader(ProfileItem(), profile)
            item.add_xpath("company", "./td[1]//text()")
            item.add_xpath("website", "./td[1]/a/@href")
            item.add_xpath("street", "./td[2]//text()")
            item.add_xpath("suburb", "./td[3]//text()")
            item.add_xpath("postcode", "./td[4]//text()")
            item.add_xpath("phone", "./td[5]//text()")

            requests.append(item.load_item())

        return requests