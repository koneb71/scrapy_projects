# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
import pandas as pd

from indian_river.items import IndianRiverItem

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


class AppraiserSpider(CrawlSpider):
    name = 'appraiser'
    allowed_domains = ['ircpa.org']
    start_urls = ['http://www.ircpa.org/Search.aspx']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        fd = "/Users/neiellcare/Documents/workplace/indian_river/Indian River Pro 01-01-2016 to 08-31-2018.xlsx"
        # data = pd.read_csv(fd)
        data = pd.read_excel(fd)
        # data['case_file_date'] = data['case_file_date'].astype(str)
        self.data = data.fillna('').to_dict('records')

    def parse(self, response):
        url = "http://www.ircpa.org/Disclaimer.aspx?Redirect=%2fSearch.aspx&CheckForCookies=Yes"
        return FormRequest(url,
                           formdata={
                               "__EVENTTARGET": str(response.xpath("//*[@id='__EVENTTARGET']/@value").get()),
                               "__EVENTARGUMENT": str(response.xpath("//*[@id='__EVENTARGUMENT']/@value").get()),
                               "__VIEWSTATE": str(response.xpath("//*[@id='__VIEWSTATE']/@value").get()),
                               "__VIEWSTATEGENERATOR": str(response.xpath("//*[@id='__VIEWSTATEGENERATOR']/@value").get()),
                               "ctl00$ContentPlaceHolder1$btnDisclaimerAccept": "Accept",
                               "ctl00$tbSearchBox": "Enter Parcel, Owner, or Address       ",
                           }, callback=self.search_profile, dont_filter=True)

    def search_profile(self, response):
        requests = []
        url = "http://www.ircpa.org/Search.aspx"

        for profile in self.data:
            requests.append(
                FormRequest(url,
                            formdata={
                                "__EVENTTARGET": str(response.xpath("//*[@id='__EVENTTARGET']/@value").get()),
                                "__EVENTARGUMENT": str(response.xpath("//*[@id='__EVENTARGUMENT']/@value").get()),
                                "__VIEWSTATE": str(response.xpath("//*[@id='__VIEWSTATE']/@value").get()),
                                "__VIEWSTATEGENERATOR": str(
                                    response.xpath("//*[@id='__VIEWSTATEGENERATOR']/@value").get()),
                                "ctl00$ContentPlaceHolder1$btnDisclaimerAccept": "Accept",
                                "ctl00$ContentPlaceHolder1$Owner$tbOwnerLastName": profile['first decedent last'],
                                "ctl00$ContentPlaceHolder1$Owner$tbOwnerFirstName": profile['Decedent first and middle only'],
                                "ctl00$ContentPlaceHolder1$Owner$btnSearchOwner": "Search",
                                "ctl00$tbSearchBox": "Enter Parcel, Owner, or Address       ",
                            }, callback=self.parse_results, dont_filter=True, meta={"data": profile, "search": 'first'})
            )

        return requests

    def parse_results(self, response):
        meta = response.meta['data']
        requests = []
        if "No results" in str(response.body) and response.meta['search'] == 'first':
            return FormRequest("http://www.ircpa.org/Search.aspx",
                        formdata={
                            "__EVENTTARGET": str(response.xpath("//*[@id='__EVENTTARGET']/@value").get()),
                            "__EVENTARGUMENT": str(response.xpath("//*[@id='__EVENTARGUMENT']/@value").get()),
                            "__VIEWSTATE": str(response.xpath("//*[@id='__VIEWSTATE']/@value").get()),
                            "__VIEWSTATEGENERATOR": str(
                                response.xpath("//*[@id='__VIEWSTATEGENERATOR']/@value").get()),
                            "ctl00$ContentPlaceHolder1$btnDisclaimerAccept": "Accept",
                            "ctl00$ContentPlaceHolder1$Owner$tbOwnerLastName": meta['decedent last'],
                            "ctl00$ContentPlaceHolder1$Owner$tbOwnerFirstName": meta['decedent first'],
                            "ctl00$ContentPlaceHolder1$Owner$btnSearchOwner": "Search",
                            "ctl00$tbSearchBox": "Enter Parcel, Owner, or Address       ",
                        }, callback=self.parse_results, dont_filter=True, meta={"data": meta, "search": 'second'})
        url = "http://www.ircpa.org/Data.aspx?ParcelID={}"
        print(len(response.xpath("//*[@class='searchresults']//tr[@class='rowstyle']")))
        for result in response.xpath("//*[@class='searchresults']//tr[@class='rowstyle']/td[1]//text()").extract():
            requests.append(
                Request(url.format(str(result)), callback=self.parse_profile, meta={'data': meta}, dont_filter=True)
            )

        return requests

    def parse_profile(self, response):
        meta = response.meta['data']
        item = ItemLoader(IndianRiverItem(), response)
        item.add_xpath("parcel_id", "//*[@id='ContentPlaceHolder1_Base_fvDataProfile_ParcelLabel']//text()")
        item.add_xpath("owner", "//*[@id='ContentPlaceHolder1_Base_fvDataProfile_OwnerLabel']//text()")
        item.add_xpath("site_address", "//*[@id='ContentPlaceHolder1_Base_fvDataProfile_AddressLabel']//text()")
        item.add_xpath("mailing_address", "//*[@id='ContentPlaceHolder1_Base_fvDataMailingAddress']//td//text()")
        item.add_xpath("dor", "//*[@id='ContentPlaceHolder1_Base_FormView1_PropertyUseDescriptionLabel']//text()")
        item.add_xpath("appraisal_date", "//*[@id='ContentPlaceHolder1_Base_FormView1_AppraisalDateLabel']/text()")
        item.add_xpath("short_legal_description", "//*[@id='ContentPlaceHolder1_Base_fvDataLegal_Legal1']//text()")

        item.add_value("case_number", str(meta['Case Number']))
        item.add_value("party_type", str(meta['PartyType']))
        item.add_value("status", str(meta['Status']))
        item.add_value("decedent_dob", str(meta['decedent DOB']))
        item.add_value("decedent_last", str(meta['first decedent last']))
        item.add_value("decedent_first", str(meta['Decedent first and middle only']))

        # return item.load_item()
        return FormRequest(str(response.url),
                           formdata={
                               "__EVENTTARGET": "ctl00$ContentPlaceHolder1$mnuData",
                               "__EVENTARGUMENT": "2",
                               "__VIEWSTATE": str(response.xpath("//*[@id='__VIEWSTATE']/@value").get()),
                               "__VIEWSTATEGENERATOR": str(
                                   response.xpath("//*[@id='__VIEWSTATEGENERATOR']/@value").get()),
                               "ctl00$tbSavePropertyAs": "",
                               "ctl00$tbSearchBox": "Enter Parcel, Owner, or Address       ",
                           }, callback=self.parse_sales, meta={'item': item},dont_filter=True)

    def parse_sales(self, response):
        item = response.meta['item']
        item.reset(response=response)

        item.add_xpath('sales_date1', "//td[text()='1']/following-sibling::td[1]/text()")
        item.add_xpath('sales_amount1', "//td[text()='1']/following-sibling::td[2]/text()")
        item.add_xpath('sales_link1', "//td[text()='1']/following-sibling::td[last()]/text()")
        item.add_xpath('sales_description1', "//td[text()='1']/following-sibling::td[4]/text()")
        item.add_xpath('sales_date2', "//td[text()='2']/following-sibling::td[1]/text()")
        item.add_xpath('sales_amount2', "//td[text()='2']/following-sibling::td[2]/text()")
        item.add_xpath('sales_link2', "//td[text()='2']/following-sibling::td[last()]/text()")
        item.add_xpath('sales_description2', "//td[text()='2']/following-sibling::td[4]/text()")
        # return item.load_item()
        return FormRequest(str(response.url),
                           formdata={
                               "__EVENTTARGET": "ctl00$ContentPlaceHolder1$mnuData",
                               "__EVENTARGUMENT": "3",
                               "__VIEWSTATE": str(response.xpath("//*[@id='__VIEWSTATE']/@value").get()),
                               "__VIEWSTATEGENERATOR": str(
                                   response.xpath("//*[@id='__VIEWSTATEGENERATOR']/@value").get()),
                               "ctl00$tbSavePropertyAs": "",
                               "ctl00$tbSearchBox": "Enter Parcel, Owner, or Address       ",
                           }, callback=self.parse_improvements, meta={'item': item}, dont_filter=True)

    def parse_improvements(self, response):
        item = response.meta['item']
        item.reset(response=response)

        item.add_xpath("actual_year_built", "//*[contains(text(), 'ActualYearBuilt:')]/following-sibling::*[1]/text()")
        item.add_xpath("effective_year_built", "//*[contains(text(), 'EffectiveYearBuilt:')]/following-sibling::*[1]/text()")

        return item.load_item()