# -*- coding: utf-8 -*-

# Scrapy settings for chartered project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chartered'

SPIDER_MODULES = ['chartered.spiders']
NEWSPIDER_MODULE = 'chartered.spiders'


COOKIES_ENABLED = False
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30