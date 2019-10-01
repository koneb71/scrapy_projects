# -*- coding: utf-8 -*-

# Scrapy settings for manatee_com project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'manatee_com'

SPIDER_MODULES = ['manatee_com.spiders']
NEWSPIDER_MODULE = 'manatee_com.spiders'

# COOKIES_ENABLED = False
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30

# Autothrottle makes the scraper go es fast as possible (by measuring how fast the target site allows us to go)
# ============
# activate it once the scraper is working well for faster testing and faster results

# DOWNLOAD_DELAY = .2 # Autothrottle never goes below this value and so we have to set it to low
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_DEBUG = True
# AUTOTHROTTLE_MAX_DELAY = 10.0
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1