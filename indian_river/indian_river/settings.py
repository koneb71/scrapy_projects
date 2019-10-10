# -*- coding: utf-8 -*-

# Scrapy settings for indian_river project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'indian_river'

SPIDER_MODULES = ['indian_river.spiders']
NEWSPIDER_MODULE = 'indian_river.spiders'

# COOKIES_ENABLED = False
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30