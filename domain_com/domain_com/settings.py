# -*- coding: utf-8 -*-

# Scrapy settings for domain_com project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'domain_com'

SPIDER_MODULES = ['domain_com.spiders']
NEWSPIDER_MODULE = 'domain_com.spiders'



COOKIES_ENABLED = False
DOWNLOAD_DELAY = .5
CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30

# DOWNLOAD_DELAY = .1 # Autothrottle never goes below this value and so we have to set it to low
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_DEBUG = True
# AUTOTHROTTLE_MAX_DELAY = 10.0
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
}
# FEED_URI="/home/domain.csv"
#
# FEED_EXPORTERS = {
# 'csv': 'scrapy.contrib.exporter.CsvItemExporter',
# }
FEED_FORMAT = 'csv'