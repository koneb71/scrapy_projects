# -*- coding: utf-8 -*-

# Scrapy settings for gamecollection_com project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'gamecollection_com'

SPIDER_MODULES = ['gamecollection_com.spiders']
NEWSPIDER_MODULE = 'gamecollection_com.spiders'

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30

CRAWLERA_PRESERVE_DELAY = True

DOWNLOADER_MIDDLEWARES = {'scrapy_crawlera.CrawleraMiddleware': 300}
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '3b5be7c7836c469c9bd265d079deb921'

ITEM_PIPELINES = {
    'gamecollection_com.mysql_pipeline.MySQLStorePipeline': 300,
}

MYSQL_HOST = 'testdb.cuaruwiziqum.eu-west-2.rds.amazonaws.com'
MYSQL_PORT = '3306'
MYSQL_DB = 'testdb'
MYSQL_USERNAME = 'test_asda'
MYSQL_PASSWORD = 'Testasda123'