# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import Join, MapCompose, Compose, TakeFirst
import re

def remove_duplicates(in_list):
    already_seen = set()
    ret_list = []
    for elem in in_list:
        if not elem in already_seen:
            ret_list.append(elem)
        already_seen.add(elem)
    return ret_list

def strip_strings(in_list):
    return [ re.sub('\s+',' ',s).strip() for s in in_list]

def remove_emptys(in_list):
    return filter(len, filter(None, in_list))


class Remove(object):
    def __init__(self, removal_string):
        self.removal_string = removal_string

    def __call__(self, value):
        if len(value) == 0: return value
        return value.replace(self.removal_string, "").strip()

def extract_from(text):
    text_splits = text.split('To')
    if text_splits:
        return re.sub('\s+',' ',text_splits[0]).replace('From', "").replace(':', "").replace(" ", "").strip()

DEFAULT = scrapy.Field(
        output_processor=Compose(
            strip_strings, remove_emptys, remove_duplicates, Join(' ')),
    )


class IndianRiverItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parcel_id = DEFAULT
    owner = DEFAULT
    site_address = DEFAULT
    mailing_address = scrapy.Field(
        output_processor=Compose(
            strip_strings, remove_emptys, remove_duplicates, Join(' '), Remove("Address:"), Remove(" Address Line 2:"), Remove("City, State Zip:")),
    )
    dor = DEFAULT
    appraisal_date = DEFAULT
    short_legal_description = DEFAULT
    sales_date1 = DEFAULT
    sales_amount1 = DEFAULT
    sales_description1 = DEFAULT
    sales_link1 = DEFAULT
    sales_date2 = DEFAULT
    sales_amount2 = DEFAULT
    sales_description2 = DEFAULT
    sales_link2 = DEFAULT
    actual_year_built = DEFAULT
    effective_year_built = DEFAULT
    case_number = DEFAULT
    party_type = DEFAULT
    status = DEFAULT
    decedent_dob = DEFAULT
    decedent_last = DEFAULT
    decedent_first = DEFAULT

