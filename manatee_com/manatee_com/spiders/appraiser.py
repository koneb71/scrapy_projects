# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy import Request, FormRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from manatee_com.items import AppraiserItem


class AppraiserSpider(CrawlSpider):
    name = 'appraiser'
    allowed_domains = ['manateeclerk.com']
    # start_urls = ['http://manateeclerk.com/']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        fd = "/Users/neiellcare/Documents/scrapy_projects/manatee_com/manatee_batch5.xlsx"
        data = pd.read_excel(fd, sheet_name=0)
        # data = data.rename(columns={'Case Number': 'case_number',
        #                             'Party Type': 'party_type',
        #                             'Case Type': 'case_type',
        #                             'Case Status': 'case_status',
        #                             'File Date': 'file_date',
        #                             'DOB': 'dob',
        #                             'Tags': 'tags'})
        data['FILING DATE'] = data['FILING DATE'].astype(str)
        self.data = data.fillna('').to_dict('records')

    def start_requests(self):
        requests = []
        for item in self.data:
            url = "https://records.manateeclerk.com/CourtRecords/Search/CaseNumber?caseNumber=%s&page=1&pageSize=25&myCases=False" % item['CASE NUMBER']
            requests.append(
                Request(url, callback=self.parse_profile_link, meta={'data': item})
            )
        return requests

    def parse_profile_link(self, response):
        token = str(response.xpath("//*[@name='__RequestVerificationToken']/@value").get())
        caseId = str(response.xpath("//*[@name='caseId']/@value").get())
        search_address = str(response.xpath("//*[@name='searchAddress']/@value").get())

        return FormRequest("https://records.manateeclerk.com/CourtRecords/Case/Details",
                           formdata={
                               '__RequestVerificationToken': token,
                               'caseId': caseId,
                               'searchAddress': search_address
                           }, meta=response.meta, callback=self.parse_info)

    def parse_info(self, response):
        meta = response.meta['data']
        item = ItemLoader(AppraiserItem(), response)
        print(response.xpath("//*[contains(text(), 'Decedent')]/following-sibling::td[1]/text()[2]").get())

        # item.add_value('src', response.url)
        item.add_xpath('party_name', "//*[contains(text(), 'Case:')]/following-sibling::span[1]/text()")
        item.add_xpath('date_filed', "//*[contains(text(), 'Filed:')]/following-sibling::span[1]/text()")
        item.add_value('decedent_name', response.xpath("//*[contains(text(), 'Decedent')]/following-sibling::td[1]/text()").get())
        item.add_value('decedent_mailing_address', response.xpath("//*[contains(text(), 'Decedent')]/following-sibling::td[1]/text()[2]").get())
        item.add_value('decedent_physical_address', response.xpath("//*[contains(text(), 'Decedent')]/following-sibling::td[1]/text()[3]").get())
        item.add_value('personal_rep_name', response.xpath("//*[contains(text(), 'Personal Rep')]/following-sibling::td[1]/text()").get())
        item.add_value('personal_rep_address', response.xpath("//*[contains(text(), 'Personal Rep')]/following-sibling::td[1]/text()[2]").get())
        item.add_xpath('docket_date', "//*[@id='dockets']//tbody//tr[last()]/td[2]/text()")
        item.add_xpath('docket_description', "//*[@id='dockets']//tbody//tr[last()]/td[3]/text()")
        item.add_xpath('file_date', "//*[contains(text(), 'Filings')]/following-sibling::div[1]/div[2]/div[2]/text()")
        item.add_xpath('file_type', "//*[contains(text(), 'Filings')]/following-sibling::div[1]/div[2]/div[4]/text()")
        item.add_value('case_number', str(meta['CASE NUMBER']))
        item.add_value('dob', str(meta['DOB']))
        item.add_value('tags', str(meta['TAGS']))
        item.add_value('party_type', str(meta['PARTY TYPE']))
        item.add_value('case_type', str(meta['CASE TYPE']))
        item.add_value('case_status', str(meta['CASE STATUS']))
        item.add_value('par_id', str(meta['PARCEL ID']))
        item.add_value('primary_address', str(meta['PRIMARY ADDRESS']))
        item.add_value('dor_use_code', str(meta['DOR USE CODE']))
        item.add_value('dor_description', str(meta['DOR DESCRIPTION']))
        item.add_value('owner', str(meta['OWNER NAME']))
        item.add_value('owner_address', str(meta['OWNER ADDRESS']))
        item.add_value('owner_city', str(meta['OWNER CITY']))
        item.add_value('owner_state', str(meta['OWNER STATE']))
        item.add_value('owner_zip', str(meta['OWNER ZIP']))
        item.add_value('just_land_value', str(meta['JUST LAND VALUE']))
        item.add_value('just_improvement_value', str(meta['JUST IMPROVEMENT VALUE']))
        item.add_value('total_just_value', str(meta['TOTAL JUST VALUE']))
        item.add_value('account_number', str(meta['ACCOUNT NUMBER']))
        item.add_value('sales_date', str(meta['SALES DATE']))
        item.add_value('sales_amount', str(meta['SALES AMOUNT']))
        item.add_value('year_built', str(meta['YEAR BUILT']))

        return item.load_item()

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
