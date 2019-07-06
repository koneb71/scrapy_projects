# -*- coding: utf-8 -*-
import json

import scrapy
import pandas as pd
from scrapy import Request
from geopy.geocoders import Nominatim
from scrapy.loader import ItemLoader

from cpaaustralia_com.items import CpaaustraliaComItem


class CpaaustraliaSpider(scrapy.Spider):
    name = 'cpaaustralia'
    allowed_domains = ['cpaaustralia.com.au']
    # start_urls = ['http://cpaaustralia.com.au/']

    def start_requests(self):
        data = json.loads(pd.read_csv("au_postcodes.csv").drop_duplicates(subset=['lat', 'lon'], keep='last').to_json(orient='records'))
        requests = []
        print(len(data))
        for code in data[15001:]:
            # geolocator = Nominatim(user_agent="cpaaustralia", timeout=300)
            # location = geolocator.reverse("%s, %s" % (str(code['lat']), str(code['lon'])))
            # location = location.raw
            # print(location)

            dump_data = {"Point":
                             {"Latitude": code['lat'],
                              "Longitude": code['lon']},
                         "LocationText":"",
                         "PostCode":"",
                         "Locality":"",
                         "CountryCode":"AU"}
            # print(dump_data)

            requests.append(Request('https://www.cpaaustralia.com.au/api/FindACpa/SearchApi.mvc/ExecuteSearch',
                          method='POST', body=json.dumps(dump_data),
                          meta={'country': 'AU'},
                          headers={
                                'content-type': 'application/json;charset=UTF-8',
                                'referer': 'https://www.cpaaustralia.com.au/FindACpa/Locate.mvc/Index',
                                '__requestverificationtoken': 'X8+CvDMuPkbMDAImv/Jhcbzz/5aQWX7AWit7TpTkbYiKmfA+tkfrCjsbIWHFJjWrV5DjadfZAr+lXLjN/kBh1qA4aKP4hnORg88an7wCWa71pStmfvW+9TWxzsOXeG29uX2PAAnKTvl2FuPTU4xmbBXQ3Kg=',
                                'cookie': '__RequestVerificationToken_Lw__=TVn+/XA3p1+kwmBf1imZGj+7IH24MgGEIAc8ln9RS5BAFcELHQEJ7Xg3yU1Gm+vN9JNuy93ltHJ+AjNCgdq1TQxXL+kTnEPEMV6jFCOesJtou8uZ/IG2JDJW4CYD3QeMgzuKyieY85mwe2WGV3XxcHi558o=; ARRAffinity=fec4d939f30049bff6f938c61645390e2e68b0974922682d1cbb5a8acfa80f72; _gcl_au=1.1.1295549376.1562073650; ASP.NET_SessionId=xidqrht1uvxnh1sudxk4zffw; SC_ANALYTICS_GLOBAL_COOKIE=2596bd271b034657aec8aa973c51c01f|False; _ga=GA1.3.1662185280.1562073655; _gid=GA1.3.1470680350.1562073655; _fbp=fb.2.1562073656602.1281695903; NSC_JOc2azjqdhw0rphcbiwholbjtxce0dq=ffffffffc3a01f2445525d5f4f58455e445a4a423660; __atuvc=5%7C27; __atuvs=5d1b94ee612587df000; _dc_gtm_UA-42836613-2=1; _gat_UA-42836613-2=1',
                                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
                                'accept': 'application/json, text/plain, */*'
                          }))
        return requests

    def parse(self, response):
        lists = []
        data = json.loads(response.body)
        for company in data['Results']:
            geolocator = Nominatim(user_agent="cpaaustralia", timeout=60)
            location = geolocator.reverse("%s, %s" % (str(company['Point']['Latitude']), str(company['Point']['Longitude'])))
            location = location.raw
            item = ItemLoader(CpaaustraliaComItem())

            item.add_value('company_name', company['CompanyName'])
            item.add_value('address', location['address'].get('road', location['address'].get('village')))
            item.add_value('suburb', location['address'].get('suburb', location['address'].get('city', '')))
            item.add_value('state', location['address'].get('state', ''))
            item.add_value('postcode', company['Postcode'])
            item.add_value('country', response.meta['country'])
            item.add_value('phone', company['Telephone'])
            item.add_value('email', company['EmailAddress'])
            item.add_value('website', company['WebsiteAddress'])

            lists.append(item.load_item())

        return lists
