# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest

from .domain import DomainSpider

import os


def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)


def describe_profile_spider():
    to_test = DomainSpider.from_crawler(get_crawler())

    def describe_data_extraction():
        resp = response_from("search.html")
        results = to_test.parse_agencies(resp)

        def should_return_only_one_item():
            assert count_requests_in_parse_result(results) == 19
            assert count_items_in_parse_result(results) == 0

    def describe_data2_extraction():
        resp = response_from("search2.htm")
        results = to_test.parse_agencies(resp)

        def should_return_only_one_item():
            assert count_requests_in_parse_result(results) == 19
            assert count_items_in_parse_result(results) == 0


    def describe_another_data_extraction():
        resp = response_from("agency.html")
        results = to_test.parse_profile(resp)

        def should_return_only_one_item():
            assert count_requests_in_parse_result(results) == 0
            assert count_items_in_parse_result(results) == 1

        def should_work_with_example():
            item = results
            print(item)

            assert item['company'] == u'Greg Hocking Holdsworth'
            assert item['email'] == u'albertpark@greghocking.com.au'
            assert item['phone'] == u'+61386445500'
            assert item['postcode'] == u'3206'
            assert item['state'] == u'VIC'
            assert item['street'] == u'332 Montague St'
            assert item['suburb'] == u'Albert Park'
            assert item['website'] == u'https://www.greghocking.com.au/'