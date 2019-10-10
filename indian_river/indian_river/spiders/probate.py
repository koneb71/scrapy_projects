# -*- coding: utf-8 -*-
import datetime
import time

import scrapy
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
import pandas as pd


class ProbateSpider(CrawlSpider):
    name = 'probate'
    allowed_domains = ['indian-river.org']
    start_urls = ['https://court.indian-river.org/']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        df = pd.read_excel(
            "/Users/neiellcare/Documents/workplace/indian_river/Indian River Pro 01-01-2016 to 08-31-2018.xlsx")
        df = df.fillna('')
        self.result = df.to_dict(orient='records')

    def parse(self, response):
        url = 'https://court.indian-river.org/BenchmarkWeb/CurrentUser.aspx/Login'
        return FormRequest(url, formdata={
            'username': 'paul@bestloantovalue.com',
            'password': 'Saurus123',
            'time': str(datetime.datetime.utcnow().microsecond)
        }, callback=self.is_logged_in, headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://court.indian-river.org/BenchmarkWeb/Home.aspx/Search',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://court.indian-river.org',
            'Host': 'court.indian-river.org',
        })

    def is_logged_in(self, response):
        print(response.body)
        requests = []
        if b'True' == response.body:
            print(len(self.result))
            for item in self.result[:5]:
                requests.append(
                    Request("https://court.indian-river.org/BenchmarkWeb/Home.aspx/Search", callback=self.search_items,
                            meta={'search': item['Case Number']}, dont_filter=True)
                )
        return requests

    def search_items(self, response):
        print(str(response.xpath("//*[@class='searchform']//*[@name='__RequestVerificationToken']/@value").get()))
        data = {
            '__RequestVerificationToken': str(response.xpath("//*[@name='__RequestVerificationToken']/@value").get()),
            'type': 'CaseNumber',
            'openedFrom': '',
            'openedTo': '',
            'closedTo': '',
            'closedFrom': '',
            'courtTypes': '6',
            'caseTypes': '109,118,110,112,113,114,115,116,246,136,84,85,87,86,88,89,90,129,130,247,152,97,98,137,138,'
                         '139,106,93,100,101,102,103,104,99,107,131,108,250,117,353,120,122,123,125,126,124,121,119,'
                         '270,127,105,271,128',
            'partyTypes': '1,2,3,4,5',
            'divisions': '20,18,9,12,3,2,15,5,17,13,6,16,7,19,14,4,8',
            'statutes': '',
            'partyBirthYear': '',
            'partyDOB': '',
        }
        data['search'] = response.meta['search']

        return FormRequest('https://court.indian-river.org/BenchmarkWeb//CourtCase.aspx/CaseSearch', formdata=data,
                           callback=self.parse_profile, dont_filter=True)

    def parse_profile(self, response):
        # print(response.body)
        with open('test.html', 'w') as f:
            f.write(str(response.body))
        # print(len(response.xpath("//*[contains(@href, '/BenchmarkWeb/Party.aspx')]/text()")))
