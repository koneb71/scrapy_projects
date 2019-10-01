# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from manatee_com.items import AppraiserItem


class AppraiserSpider(CrawlSpider):
    name = 'appraiser'
    allowed_domains = ['manateeclerk.com']
    # start_urls = ['http://manateeclerk.com/']

    def __init__(self, *a, **kw):
        # super().__init__(*a, **kw)
        fd = "C:\Users\NeiellCare\Documents\workspace\scrapers\manatee_com\manatee 01-01-2016 to 08-31-2019.xlsx"
        data = pd.read_excel(fd, sheet_name=1)
        data = data.rename(columns={'Case Number': 'case_number',
                                    'Party Type': 'party_type',
                                    'Case Type': 'case_type',
                                    'Case Status': 'case_status',
                                    'File Date': 'file_date',
                                    'DOB': 'dob',
                                    'Tags': 'tags'})
        data['file_date'] = data['file_date'].astype(str)
        self.data = data.fillna('').to_dict('records')

    def start_requests(self):
        requests = []
        for item in self.data:
            url = "https://records.manateeclerk.com/CourtRecords/Search/CaseNumber?caseNumber=%s&page=1&pageSize=25&myCases=False" % item['case_number']
            requests.append(
                Request(url, callback=self.parse_decent_name, meta={'data': item})
            )
        return requests

    def parse_decent_name(self, response):
        meta = response.meta['data']
        item = ItemLoader(AppraiserItem(), response)

        item.add_value('src', response.url)
        item.add_xpath('party_name', "//*[@class='data-row']/td[4]//text()")
        item.add_value('case_number', meta['case_number'])
        item.add_value('party_type', meta['party_type'])
        item.add_value('case_type', meta['case_type'])
        item.add_value('case_status', meta['case_status'])
        item.add_value('file_date', meta['file_date'])
        item.add_value('dob', str(meta['dob']))
        item.add_value('tags', str(meta['tags']))

        return item.load_item()
