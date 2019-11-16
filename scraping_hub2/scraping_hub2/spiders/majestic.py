import logging
# logging.getLogger('scrapy').setLevel(logging.WARNING)
import time
import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import urllib.parse
from scrapy.item import Item, Field
from scrapy_splash import SplashRequest
import pandas as pd
import numpy as np
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class spider1(scrapy.Spider):
    name = 'majestic_spider'
    # handle_httpstatus_list = [404, 302]

    start_urls = [
        'http://api.majestic.com/api/json?app_api_key=9610EFFCAC1C725301CD49753E2A0FA2&cmd=GetIndexItemInfo&items=1&item0=http://www.restorefx.com/national-and-local-resources.html&datasource=fresh']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["keyword", "search_operator",
                               "link", "email",
                               "link_majestic", "citation_flow", "trust_flow"],
    }

    def start_requests(self):
        for url in self.start_urls:
            # df = pd.read_csv('~/Desktop/anna_outreach/new/resource_page_outreach/google_site_operator_outreach_data_test.csv')
            # df = pd.read_csv('~/Desktop/anna_outreach/new/sponsors/google_sponsors_emails3.csv')
            # df = pd.read_csv('~/Desktop/anna_outreach/new/blog_outreach/blog_outreach_emails6.csv')
            ##df = pd.read_csv('/home/hronis/Desktop/anna_outreach/new/info_video/info_video_outreach_emails_completed.csv')
            ##df2 = df[['inurl', 'state', 'query', 'link', 'email']]
            ##df = pd.read_csv('~/scrapy_projects/peirama_splash/link_building_outreach_car_accident_emails.csv')
            ##df = pd.read_csv('~/Desktop/marcela_outreach/outreach_emails.csv')
            df = pd.read_csv(
                '~/Desktop/marcela_outreach/new/emails/dmillerlaw/outreach_emails_for_dmillerlaw_processed.csv')
            df2 = df[['keyword', 'search_operator', 'link', 'email']]
            for i, j, k, l in df2.itertuples(index=False):
                link = 'http://api.majestic.com/api/json?app_api_key=9610EFFCAC1C725301CD49753E2A0FA2&cmd=GetIndexItemInfo&items=1&item0=' + k + '&datasource=fresh'
                yield scrapy.Request(link, self.parse, meta={'keyword': i,
                                                             'search_operator': j, 'link': k, 'email': l})

    def parse(self, response):
        item = lefta()
        data = json.loads(response.text)
        item['link_majestic'] = data['DataTables']['Results']['Data'][0]['Item']
        item['citation_flow'] = data['DataTables']['Results']['Data'][0]['CitationFlow']
        item['trust_flow'] = data['DataTables']['Results']['Data'][0]['TrustFlow']
        item['keyword'] = response.meta['keyword']
        # item['intitle'] = response.meta['intitle']
        item['search_operator'] = response.meta['search_operator']
        ##item['query'] = response.meta['query']
        item['link'] = response.meta['link']
        # item['link2'] = response.meta['link2']
        item['email'] = response.meta['email']
        yield item


class lefta(scrapy.Item):
    link_majestic = scrapy.Field()
    citation_flow = scrapy.Field()
    trust_flow = scrapy.Field()
    keyword = scrapy.Field()
    # intitle = scrapy.Field()
    search_operator = scrapy.Field()
    ##query = scrapy.Field()
    link = scrapy.Field()
    email = scrapy.Field()
    # link2 = scrapy.Field()


