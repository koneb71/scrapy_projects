# -*- coding: utf-8 -*-

# Scrapy settings for smythstoys project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'smythstoys'

SPIDER_MODULES = ['smythstoys.spiders']
NEWSPIDER_MODULE = 'smythstoys.spiders'

CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_TIMEOUT = 30

DOWNLOAD_DELAY = .1 # Autothrottle never goes below this value and so we have to set it to low
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1

ITEM_PIPELINES = {
    'smythstoys.mysql_pipeline.MySQLStorePipeline': 300,
}

MYSQL_HOST = 'awsftfba1.cuaruwiziqum.eu-west-2.rds.amazonaws.com'
MYSQL_PORT = '3306'
MYSQL_DB = 'aws_ftfba1'
MYSQL_USERNAME = 'scrapinghub'
MYSQL_PASSWORD = '{nPb!7g3c_V)WNwM'