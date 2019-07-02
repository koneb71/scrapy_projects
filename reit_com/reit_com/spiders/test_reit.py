# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest

from .reit import ReitSpider

import os

def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

def describe_profile_spider():

    to_test = ReitSpider.from_crawler(get_crawler())

    def describe_search_link_extraction():
        resp = response_from("search.htm")
        results = to_test.parse(resp)

        def should_return_only_one_item():
            # parse results should hold only one item (sometimes parsers have to return a mix!)
            assert count_requests_in_parse_result(results) == 0
            assert count_items_in_parse_result(results) == 82

        def should_work_with_example():
            item = results[0]
            print(item)

            assert item['company'] == u'4one4 Real Estate'
            assert item['phone'] == u'(03) 6273-7414'
            assert item['postcode'] == u'7010'
            assert item['street'] == u'414 Main Road'
            assert item['suburb'] == u'Glenorchy'
            assert item['website'] == u'http://www.4one4realestate.com.au/'