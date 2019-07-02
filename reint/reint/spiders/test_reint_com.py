# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest

from .reint_com import ReintComSpider

import os

def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

def describe_profile_spider():

    to_test = ReintComSpider.from_crawler(get_crawler())

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

            assert item["company"] == u'Castle Real Estate'
            assert item["phone"] == u'08 8932 8658'
            assert item["postcode"] == u'0830'
            assert item["state"] == u'NT'
            assert item["street"] == u'15 CROWSON CL'
            assert item["suburb"] == u'DURACK'
            assert item["website"] == u'http://www.castlerealestate.com.au'
            assert item["email"] == u'admin@castlerealestate.com.au'