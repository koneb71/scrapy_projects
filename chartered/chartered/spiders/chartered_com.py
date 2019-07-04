# -*- coding: utf-8 -*-
import json

import scrapy
import pandas as pd
from scrapy import Request
from geopy.geocoders import Nominatim


class CharteredComSpider(scrapy.Spider):
    name = 'chartered_com'
    allowed_domains = ['charteredaccountantsanz.com']

    def start_requests(self):
        data = json.loads(pd.read_csv("au_postcodes.csv").to_json(orient='records'))
        requests = []
        for code in data[:4]:
            requests.append(Request(
                "https://www.charteredaccountantsanz.com/api/MapApi/ClosestMembersGrouped?latitude=%s&longitude=%s6&membertype=undefined&limit=500" % (
                str(code['lat']), str(code['lon']))))
        return requests

    def parse(self, response):
        data = json.loads(response.body)

        geolocator = Nominatim(user_agent="charteredaccountantsanz")
        location = geolocator.reverse("%s, %s" % (data[0]['Latitude'], data[0]['Longitude']))

        body = {
            'Point': {
                'Latitude': location['lat'],
                'Longitude': location['lon']
            },
            'CountryCode': location['address']['country_code'],
            'Locality': location['address']['city'],
            'LocationText': location['display_name'],
            'PostCode': location['address']['postcode']
        }

        req = Request('https://www.cpaaustralia.com.au/api/FindACpa/SearchApi.mvc/ExecuteSearch', method='POST',
                      body=json.dumps(body), headers={'Content-Type': 'application/json')
        print(location.raw)
