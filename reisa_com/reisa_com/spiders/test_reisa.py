# -*- coding: utf-8 -*-
from scrapy.utils.test import get_crawler
from scrapy_tdd import *
import pytest

from .reisa import ReisaSpider

import os

def response_from(file_name):
    return mock_response_from_sample_file(my_path(__file__) + "/samples", file_name)

def describe_profile_spider():

    to_test = ReisaSpider.from_crawler(get_crawler())

    def describe_search_link_extraction():
        resp = response_from("search_a.htm")
        results = to_test.parse_agencies_links(resp)

        def should_return_only_one_item():
            # parse results should hold only one item (sometimes parsers have to return a mix!)
            assert count_requests_in_parse_result(results) == 242
            assert count_items_in_parse_result(results) == 0

    def describe_data_extraction():
        resp = response_from("agency.htm")
        results = to_test.parse_profile(resp)

        def should_return_only_one_item():
            # parse results should hold only one item (sometimes parsers have to return a mix!)
            assert count_requests_in_parse_result(results) == 0
            assert count_items_in_parse_result(results) == 1

        def should_work_with_example():
            item = results
            print(item)

            assert item["contact_name"] == u'Andrew Hudson Contact'
            assert item["email"] == u'andrew@formeprojex.com.au'
            assert item["fax"] == u'08 8203 1499'
            assert item["phone"] == u'08 8203 1400'

    def describe_another_data_extraction():
        resp = response_from("agency2.htm")
        results = to_test.parse_profile(resp)

        def should_return_only_one_item():
            # parse results should hold only one item (sometimes parsers have to return a mix!)
            assert count_requests_in_parse_result(results) == 0
            assert count_items_in_parse_result(results) == 1

        def should_work_with_example():
            item = results
            print(item)

            assert item["company"] == u'@realty'
            assert item["contact_name"] == u'Andrew Giles Contact'
            assert item["email"] == u'gilesproperty@atrealty.com.au'
            assert item["fax"] == u'0755 920 900'
            assert item["phone"] == u'0414 696 936'
            assert item["website"] == u'http://www.atrealty.com.au'