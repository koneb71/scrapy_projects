# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider

from canada_colleges.items import CanadaCollegesItem


class CollegesSpider(CrawlSpider):
    name = 'colleges'
    allowed_domains = ['cicic.ca']
    start_urls = ['https://www.cicic.ca/869/results.canada?search=&t=1,2']
    base_url = "https://www.cicic.ca"

    def parse(self, response):
        requests = []
        for res in response.xpath("//*[@class='rgMasterTable']//tbody//td/a/@href"):
            requests.append(
                Request(self.base_url + str(res.extract()).replace(" ", "%20"), callback=self.parse_item)
            )

        formLink = ''.join(response.xpath("//form[@id='form1']/@action").extract()).replace(".", "", 1)
        if formLink:
            url =  self.base_url + "/869" + formLink
            data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                # "__EVENTARGUMENT": response.xpath("//*[@id='__EVENTARGUMENT']/@value").extract(),
                "__VSTATE": response.xpath("//*[@id='__VSTATE']/@value").extract(),
                "__VIEWSTATE": response.xpath("//*[@id='__VIEWSTATE']/@value").extract(),
                "__EVENTVALIDATION": response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract(),
                "ctl12$ctl00$EDsearchBox": "",
                "ctl12_ctl00_EDsearchBox_ClientState": '{"enabled":true,"logEntries":[{"Type":1,"Index":0,"Data":{"text":"","value":""}}],"delimiters":[]}',
                "ctl12$ctl00$Chketab_university": "on",
                "ctl12$ctl00$Chketab_college": "on",
                "ctl12$ctl00$gridresults$ctl00$ctl03$ctl01$ctl28": "",
                "ctl12$ctl00$gridresults$ctl00$ctl03$ctl01$PageSizeComboBox": "30",
                "ctl12_ctl00_gridresults_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState": "",
                "ctl12_ctl00_gridresults_ClientState": "",
            }

            for code in response.xpath("//*[@class='rgWrap rgNumPart']//a/@href")[1:-1]:
                c = ''.join(code.extract()).replace('href="javascript:__doPostBack(&#39;', '').replace('&#39;,&#39;&#39;)', '')
                data['__EVENTTARGET'] = c
                requests.append(
                    FormRequest(url, method="POST", formdata=data, callback=self.parse)
                )

            if ''.join(response.xpath("//*[@class='rgWrap rgNumPart']//a//text()")[-1].extract()) == '...':
                data['__EVENTTARGET'] = ''.join(response.xpath("//*[@class='rgWrap rgNumPart']//a/@href")[-1].extract()).replace('href="javascript:__doPostBack(&#39;', '').replace('&#39;,&#39;&#39;)', '')
                requests.append(
                    FormRequest(url, method="POST", formdata=data, callback=self.parse_next_page)
                )

        return requests

    def parse_next_page(self, response):
        requests = []
        formLink = ''.join(response.xpath("//form[@id='form1']/@action").extract()).replace(".", "", 1)
        if formLink:
            url =  self.base_url + "/869" + formLink
            data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                # "__EVENTARGUMENT": response.xpath("//*[@id='__EVENTARGUMENT']/@value").extract(),
                "__VSTATE": response.xpath("//*[@id='__VSTATE']/@value").extract(),
                "__VIEWSTATE": response.xpath("//*[@id='__VIEWSTATE']/@value").extract(),
                "__EVENTVALIDATION": response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract(),
                "ctl12$ctl00$EDsearchBox": "",
                "ctl12_ctl00_EDsearchBox_ClientState": '{"enabled":true,"logEntries":[{"Type":1,"Index":0,"Data":{"text":"","value":""}}],"delimiters":[]}',
                "ctl12$ctl00$Chketab_university": "on",
                "ctl12$ctl00$Chketab_college": "on",
                "ctl12$ctl00$gridresults$ctl00$ctl03$ctl01$ctl28": "",
                "ctl12$ctl00$gridresults$ctl00$ctl03$ctl01$PageSizeComboBox": "30",
                "ctl12_ctl00_gridresults_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState": "",
                "ctl12_ctl00_gridresults_ClientState": "",
            }

            for code in response.xpath("//*[@class='rgWrap rgNumPart']//a/@href")[1:-1]:
                c = ''.join(code.extract()).replace('href="javascript:__doPostBack(&#39;', '').replace('&#39;,&#39;&#39;)',
                                                                                                       '')
                data['__EVENTTARGET'] = c
                requests.append(
                    FormRequest(url, method="POST", formdata=data, callback=self.iter_items)
                )
            return requests

    def iter_items(self, response):
        requests = []
        for res in response.xpath("//*[@class='rgMasterTable']//tbody//td/a/@href"):
            requests.append(
                Request(self.base_url + str(res.extract()), callback=self.parse_item)
            )
        return requests

    def parse_item(self, response):
        item = ItemLoader(CanadaCollegesItem(), response)

        item.add_value("src", response.url)
        item.add_xpath('name', "//*[@id='ctl12__4f26c2801046c_titre']//text()")
        item.add_xpath('email', "//span[@id='ctl12__4f26c2801046c_orgemail']/text()")
        item.add_xpath('website', "//div[1]/a[@target='_blank']/@href")

        return item.load_item()
