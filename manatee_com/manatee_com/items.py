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

def extract_to(text):
    text_splits = text.split('To')
    if text_splits and len(text_splits) > 0:
        return re.sub('\s+',' ',text_splits[1]).replace(':', "").replace(" ", "").strip()

def remove_all_empty_spaces(text):
    return text.replace(" ", "").strip()

DEFAULT = scrapy.Field(
        output_processor=Compose(
            strip_strings, remove_emptys, remove_duplicates, Join(' ')),
    )

class ManateeComItem(scrapy.Item):
    src = DEFAULT
    par_id = scrapy.Field(
        output_processor=Compose(
            strip_strings, remove_emptys, remove_duplicates, Join(' '), Remove('PARID: ')),
    )
    name = DEFAULT
    primary_address = DEFAULT
    dor_use_code = DEFAULT
    dor_description = DEFAULT
    owner = DEFAULT
    owner_address = DEFAULT
    owner_city = DEFAULT
    owner_state = DEFAULT
    owner_zip = DEFAULT
    just_land_value = DEFAULT
    just_improvement_value = DEFAULT
    total_just_value = DEFAULT
    account_number = DEFAULT
    sales_date = DEFAULT
    sales_amount = DEFAULT
    year_built = DEFAULT
    case_number = DEFAULT
    party_name = DEFAULT
    party_type = DEFAULT
    case_type = DEFAULT
    case_status = DEFAULT
    case_file_date = DEFAULT
    dob = DEFAULT
    tags = DEFAULT
    is_multiple = DEFAULT

class AppraiserItem(scrapy.Item):
    src = DEFAULT
    party_name = DEFAULT
    case_number = DEFAULT
    party_type = DEFAULT
    case_type = DEFAULT
    case_status = DEFAULT
    file_date = DEFAULT
    dob = DEFAULT
    tags = DEFAULT