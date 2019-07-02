# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest

from .spider import SpiderSpider

import os

def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

def describe_profile_spider():

    to_test = SpiderSpider.from_crawler(get_crawler())

    def describe_data_extraction():
        resp = response_from("agency.html")
        results = to_test.parse(resp)

        def should_return_only_one_item():
            # parse results should hold only one item (sometimes parsers have to return a mix!)
            assert count_requests_in_parse_result(results) == 0
            assert count_items_in_parse_result(results) == 1

        def should_work_with_example():
            item = results
            print(item)

            assert item["company"] == u'LJ Hooker Rockdale'
            assert item["phone"] == u'02 9597 6144'
            assert item["postcode"] == u'2216'
            assert item["state"] == u'NSW'
            assert item["street"] == u'426 Princess Hwy'
            assert item["suburb"] == u'Rockdale'
            assert item["website"] == u'http://www.rockdale.ljhooker.com.au'


    def describe_another_data_extraction():
        resp = response_from("agency2.html")
        results = to_test.parse(resp)

        def should_return_only_one_item():
            # parse results should hold only one item (sometimes parsers have to return a mix!)
            assert count_requests_in_parse_result(results) == 0
            assert count_items_in_parse_result(results) == 1

        def should_work_with_example():
            item = results
            print(item)

            assert item["company"] == u'No Bull Real Estate'
            assert item["phone"] == u'02 4955 2624'
            assert item["postcode"] == u'2286'
            assert item["state"] == u'NSW'
            assert item["street"] == u'72 Carrington Street'
            assert item["suburb"] == u'West Wallsend'
