# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
# from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
import pandas as pd
# import urllib.parse

from manatee_com.items import ManateeComItem

from scrapy.loader import ItemLoader as ScrapyItemLoader

class ItemLoader(ScrapyItemLoader):
    """ Extended Loader
        for Selector resetting.
        """

    def reset(self, selector=None, response=None):
        if response is not None:
            if selector is None:
                selector = self.default_selector_class(response)
            self.selector = selector
            self.context.update(selector=selector, response=response)
        elif selector is not None:
            self.selector = selector
            self.context.update(selector=selector)

class ManateeSpider(CrawlSpider):
    name = 'manatee'
    allowed_domains = ['manateepao.com']
    start_urls = ['https://www.manateepao.com/ManateeFL/search/commonsearch.aspx?mode=owner']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        fd = "/Users/neiellcare/Documents/scrapy_projects/manatee_com/decent_names2.csv"
        data = pd.read_csv(fd)
        # data = pd.read_excel(fd)
        data['case_file_date'] = data['case_file_date'].astype(str)
        self.data = data.fillna('').to_dict('records')

    def parse(self, response):
        if "Disclaimer.aspx?FromUrl=" in response.url:
            viewstate = response.xpath("//*[@name='__VIEWSTATE']/@value").get()
            viewstate_generator = response.xpath("//*[@name='__VIEWSTATEGENERATOR']/@value").get()
            event_validation = response.xpath("//*[@name='__EVENTVALIDATION']/@value").get()

            return FormRequest(
                "https://www.manateepao.com/ManateeFL/Search/Disclaimer.aspx?FromUrl=..%2fsearch%2fcommonsearch.aspx%3fmode%3downer",
                formdata={
                    '__VIEWSTATE': viewstate,
                    '__VIEWSTATEGENERATOR': viewstate_generator,
                    '__EVENTVALIDATION': event_validation,
                    'btAgree': '',
                    'hdURL': '../search/commonsearch.aspx?mode=owner',
                    'action': ''
                },
                callback=self.start_search
            )

    def start_search(self, response):
        requests = []

        for item in self.data[9:]:
            # print(item)
            requests.append(
                FormRequest(
                    'https://www.manateepao.com/ManateeFL/search/CommonSearch.aspx?mode=OWNER',
                    formdata={
                        'ScriptManager1_TSM': str(response.xpath("//*[@name='ScriptManager1_TSM']/@value").get()),
                        '__EVENTTARGET': str(response.xpath("//*[@name='__EVENTTARGET']/@value").get()),
                        '__EVENTARGUMENT': str(response.xpath("//*[@name='__EVENTARGUMENT']/@value").get()),
                        '__VIEWSTATE': str(response.xpath("//*[@name='__VIEWSTATE']/@value").get()),
                        '__VIEWSTATEGENERATOR': str(response.xpath("//*[@name='__VIEWSTATEGENERATOR']/@value").get()),
                        '__EVENTVALIDATION': str(response.xpath("//*[@name='__EVENTVALIDATION']/@value").get()),
                        'PageNum': '1',
                        'SortBy': 'PARID',
                        'SortDir': 'asc',
                        'PageSize': '100',
                        'hdAction': 'Search',
                        'hdIndex': '5',
                        'sIndex': '-1',
                        'hdListType': 'PA',
                        'hdJur': '',
                        'hdSelectAllChecked': 'false',
                        'inpOwner': str(item['first']).upper(),
                        'selSortBy': 'PARID',
                        'selSortDir': 'asc',
                        'selPageSize': '100',
                        'searchOptions$hdBeta': '',
                        'btSearch': '',
                        'RadWindow_NavigateUrl_ClientState': '',
                        'mode': 'OWNER',
                        'mask': '',
                        'param1': '',
                        'searchimmediate': '',
                    }
                , callback=self.parse_results, meta={'data': item, 'search': 'first'}, dont_filter=True
                )
            )

        return requests

    def parse_results(self, response):
        requests = []
        base_url = 'https://www.manateepao.com/ManateeFL/'

        links = response.xpath("//tr[contains(@onclick, '.aspx')]/@onclick")
        if links:
            print(len(links))
            # if len(links) > 1:
            #     meta = response.meta['data']
            #     item = ItemLoader(ManateeComItem(), response)
            #
            #     item.add_value('case_number', meta['case_number'])
            #     item.add_value('party_name', meta['complete party_name_from_probate'])
            #     item.add_value('party_type', meta['party_type'])
            #     item.add_value('case_type', meta['case_type'])
            #     item.add_value('case_status', meta['case_status'])
            #     item.add_value('case_file_date', meta['case_file_date'])
            #     item.add_value('dob', str(meta['dob']))
            #     item.add_value('tags', str(meta['tags']))
            #     item.add_value('is_multiple', "yes")
            #
            #     return item.load_item()
            # else:
            # for link in links[:2]:
            link = str(links[0].get()).split('../')[1].replace("')", '')
            requests.append(
                Request(base_url+link, callback=self.parse_profile, meta=response.meta, dont_filter=True)
            )
        elif response.meta['search'] == 'first':
            print('second: ' + str(response.meta['data']['second']))
            requests.append(
                FormRequest(
                    'https://www.manateepao.com/ManateeFL/search/CommonSearch.aspx?mode=OWNER',
                    formdata={
                        'ScriptManager1_TSM': str(response.xpath("//*[@name='ScriptManager1_TSM']/@value").get()),
                        '__EVENTTARGET': str(response.xpath("//*[@name='__EVENTTARGET']/@value").get()),
                        '__EVENTARGUMENT': str(response.xpath("//*[@name='__EVENTARGUMENT']/@value").get()),
                        '__VIEWSTATE': str(response.xpath("//*[@name='__VIEWSTATE']/@value").get()),
                        '__VIEWSTATEGENERATOR': str(response.xpath("//*[@name='__VIEWSTATEGENERATOR']/@value").get()),
                        '__EVENTVALIDATION': str(response.xpath("//*[@name='__EVENTVALIDATION']/@value").get()),
                        'PageNum': '1',
                        'SortBy': 'PARID',
                        'SortDir': 'asc',
                        'PageSize': '100',
                        'hdAction': 'Search',
                        'hdIndex': '5',
                        'sIndex': '-1',
                        'hdListType': 'PA',
                        'hdJur': '',
                        'hdSelectAllChecked': 'false',
                        'inpOwner': str(response.meta['data']['second']).upper(),
                        'selSortBy': 'PARID',
                        'selSortDir': 'asc',
                        'selPageSize': '100',
                        'searchOptions$hdBeta': '',
                        'btSearch': '',
                        'RadWindow_NavigateUrl_ClientState': '',
                        'mode': 'OWNER',
                        'mask': '',
                        'param1': '',
                        'searchimmediate': '',
                    }
                    , callback=self.parse_results, meta={'data': response.meta['data'], 'search': 'second'}, dont_filter=True
                )
            )
        else:
            meta = response.meta['data']
            item = ItemLoader(ManateeComItem(), response)

            item.add_value('case_number', meta['case_number'])
            item.add_value('party_name', meta['party_name'])
            # item.add_value('party_name', meta['complete party_name_from_probate'])
            item.add_value('party_type', meta['party_type'])
            item.add_value('case_type', meta['case_type'])
            item.add_value('case_status', meta['case_status'])
            item.add_value('case_file_date', meta['case_file_date'])
            item.add_value('dob', str(meta['dob']))
            item.add_value('tags', str(meta['tags']))

            return item.load_item()
        return requests

    def parse_profile(self, response):
        meta = response.meta['data']
        item = ItemLoader(ManateeComItem(), response)

        # item.add_value('src', response.url)
        item.add_xpath('par_id', "//*[contains(text(), 'PARID:')]/text()")
        item.add_xpath('name', '//td[@class="DataletHeaderBottom"][1]//text()')
        item.add_xpath('primary_address', "//*[contains(text(), 'Primary Address Location')]/following-sibling::td[1]/text()")
        item.add_xpath('dor_use_code', "//*[contains(text(), 'DOR Use Code')]/following-sibling::td[1]/text()")
        item.add_xpath('dor_description', "//*[contains(text(), 'DOR Description')]/following-sibling::td[1]/text()")
        item.add_xpath('owner', "//table[@id='Owners']//*[contains(text(), 'Owner')][1]/following-sibling::td[1]/text()")
        item.add_xpath('owner_address', "//table[@id='Owners']//*[contains(text(), 'Address')]/following-sibling::td[1]/text()")
        item.add_xpath('owner_city', "//table[@id='Owners']//*[contains(text(), 'City')]/following-sibling::td[1]/text()")
        item.add_xpath('owner_state', "//table[@id='Owners']//*[contains(text(), 'State')]/following-sibling::td[1]/text()")
        item.add_xpath('owner_zip', "//table[@id='Owners']//*[contains(text(), 'Zip Code')]/following-sibling::td[1]/text()")
        item.add_value('case_number', meta['case_number'])
        item.add_value('party_name', meta['party_name'])
        # item.add_value('party_name', meta['complete party_name_from_probate'])
        item.add_value('party_type', meta['party_type'])
        item.add_value('case_type', meta['case_type'])
        item.add_value('case_status', meta['case_status'])
        item.add_value('case_file_date', meta['case_file_date'])
        item.add_value('dob', str(meta['dob']))
        item.add_value('tags', str(meta['tags']))

        url = response.xpath("//*[@class='unsel']//*[contains(text(), 'Values')]/../@href").get()
        url = "https://www.manateepao.com/ManateeFL/" + str(url).replace("../", '')

        return [Request(url, callback=self.parse_value_page, meta={'item': item}, dont_filter=True)]

    # def update_params(self, url, mode):
    #     params = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(str(url)).query))
    #     url = urllib.parse.urlsplit(str(url)).netloc
    #     path = urllib.parse.urlsplit(str(url)).path
    #     params['mode'] = mode
    #     final_params = urllib.parse.urlencode(params)
    #     return 'https://' + url + path + final_params

    def parse_value_page(self, response):
        # print(response.xpath("//*[contains(text(), 'Just Land Value')]/../following-sibling::td[1]//text()").get())
        item = response.meta['item']
        item.reset(response=response)

        item.add_xpath('just_land_value',
                       "//*[contains(text(), 'Just Land Value')]/../following-sibling::td[1]//text()")
        item.add_xpath('just_improvement_value',
                       "//*[contains(text(), 'Just Improvement Value')]/../following-sibling::td[1]//text()")
        item.add_xpath('total_just_value',
                       "//*[contains(text(), 'Total Just Value')]/../following-sibling::td[1]//text()")

        url = response.xpath("//*[@class='unsel']//*[contains(text(), 'Sales')]/../@href").get()
        url = "https://www.manateepao.com/ManateeFL/" + str(url).replace("../", '')

        return [Request(url, callback=self.parse_sales_page, meta={'item': item}, dont_filter=True)]

    def parse_sales_page(self, response):
        item = response.meta['item']
        item.reset(response=response)

        item.add_xpath('account_number',
                       "//table[@id='Sales']//*[contains(text(), 'Account#')]/following-sibling::td[1]//text()")
        item.add_xpath('sales_date',
                       "//table[@id='Sales']//*[contains(text(), 'Date')]/following-sibling::td[1]//text()")
        item.add_xpath('sales_amount',
                       "//table[@id='Sales']//*[contains(text(), 'Sale Amount')]/following-sibling::td[1]//text()")

        url = response.xpath("//*[@class='unsel']//*[contains(text(), 'Residential')]/../@href").get()
        url = "https://www.manateepao.com/ManateeFL/" + str(url).replace("../", '')

        return [Request(url, callback=self.parse_year_built_page, meta={'item': item}, dont_filter=True)]

    def parse_year_built_page(self, response):
        item = response.meta['item']
        item.reset(response=response)

        item.add_xpath('year_built',
                       "//table[@id='Residential']//*[contains(text(), 'Year')]/following-sibling::td[1]//text()")

        return item.load_item()