# -*- coding: utf-8 -*-

# Scrapy settings for asda project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'asda'

SPIDER_MODULES = ['asda.spiders']
NEWSPIDER_MODULE = 'asda.spiders'

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30

# DOWNLOAD_DELAY = .1 # Autothrottle never goes below this value and so we have to set it to low
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_DEBUG = True
# AUTOTHROTTLE_MAX_DELAY = 10.0
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    'asda.middlewares.AsdaDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'asda.mysql_pipeline.MySQLStorePipeline': 300,
}

MYSQL_HOST = 'testdb.cuaruwiziqum.eu-west-2.rds.amazonaws.com'
MYSQL_PORT = '3306'
MYSQL_DB = 'testdb'
MYSQL_USERNAME = 'test_asda'
MYSQL_PASSWORD = 'Testasda123'