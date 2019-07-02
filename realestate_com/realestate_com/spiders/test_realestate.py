# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest

from .realestate import RealestateSpider

import os


def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)


def describe_profile_spider():
    to_test = RealestateSpider.from_crawler(get_crawler())

    def describe_data_extraction():
        resp = response_from("links.htm")
        results = to_test.parse_agencies(resp)

        def should_return_only_one_item():
            assert count_requests_in_parse_result(results) == 1
            assert count_items_in_parse_result(results) == 20

        def should_work_with_example():
            item = results
            print(item)

            assert {'company': u'- Oasis Residences',
                    'phone': u'03 9662 3627',
                    'postcode': u'3205',
                    'state': u'Vic',
                    'street': u'1-13 Cobden Street',
                    'suburb': u'South Melbourne',
                    'website': u'http://www.oasisresidences.com.au'} in item
