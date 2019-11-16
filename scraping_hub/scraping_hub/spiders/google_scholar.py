import logging
# logging.getLogger('scrapy').setLevel(logging.WARNING)
import time
import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import urllib.parse
from scrapy.item import Item, Field
from scrapy_splash import SplashRequest
import pandas as pd
import numpy as np
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re


class spider1(scrapy.Spider):
    name = 'google_scholar_spider'
    # handle_httpstatus_list = [404, 302]

    # start_urls = ['https://www.google.com/search?q=Dr.+Gregory+Jovanelly']
    start_urls = ['https://blog.feedspot.com/military_wife_blogs/']
    # start_urls = ['https://www.usnews.com/best-colleges/ok?_mode=table&_page=2&format=json']#,'https://www.usnews.com/best-colleges/ga?_mode=table&_page=2&format=json']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["keyword", "search_operator", "link", "email"],
    }

    def start_requests(self):
        for url in self.start_urls:
            # lista=['al','ak','az','ar','ca','co','ct','dc','de','fl','ga','hi','id',
            # 'il','in','ia','ks','ky','la','me','md','ma','mi','mn','ms','mo','mt',
            # 'ne','nv','nh','nj','nm','ny','nc','nd','oh','ok','or','pa','ri','sc',
            # 'sd','tn','tx','ut','vt','va','wa','wv','wi','wy']
            #  for i in lista:
            #   link='https://www.usnews.com/best-colleges/'+i+'?_mode=table&_page=1&format=json'
            #  yield scrapy.Request(link,self.parse, headers={'X-Crawlera-Profile':'desktop'})

            # df=pd.read_csv('~/scrapy_projects/peirama_splash/us_unis.csv')
            # df=pd.read_csv('~/scrapy_projects/scraping_hub/interships_non_edu_companies.csv')
            ##df=pd.read_csv('~/Desktop/alexa_military_wives/alexa_military_relevant_sites.csv')
            ###df=pd.read_csv('~/scrapy_projects/scraping_hub/google_site_operator_justia_terms.csv')
            ###df2=df.drop_duplicates(subset=['link'])
            # df=pd.read_csv('~/Desktop/anna_outreach/new/resource_page_outreach/google_site_operator_outreach_data_deduplicated.csv')
            # df=pd.read_csv('~/Desktop/anna_outreach/new/sponsors/google_sponsors.csv')
            # df=pd.read_csv('/home/hronis/Desktop/anna_outreach/new/blog_outreach/blog_outreach.csv')
            # df=pd.read_csv('/home/hronis/Desktop/anna_outreach/new/info_video/info_video_outreach.csv')
            # df=pd.read_csv('/home/hronis/Desktop/anna_outreach/new/podcasts/google_site_operator_podcasts.csv')
            ##df=pd.read_csv('~/scrapy_projects/scraping_hub/winary_listing_with_website_fixed.csv')
            # df = pd.read_csv('/home/hronis/scrapy_projects/scraping_hub/google_search_operators_for_link_building_outreach2_all3.csv')
            df = pd.read_csv('/home/hronis/Desktop/marcela_outreach/new/sites/outreach_sites_for_cck_law.csv')
            df2 = df.drop_duplicates(subset='link').reset_index(drop=True)
            df3 = df2.dropna(subset=['link'])
            for keyword, search_operator, link in df3[27240:].itertuples(index=False):
                # link2='https://www.google.com/search?q='+i.replace(' ','+')+'+contact'#'financial+aid'
                '''try:
                  url=i.split('/')[0]+'//'+i.split('/')[2]+'/contact-us'
                  yield scrapy.Request(url, self.parse3, meta={'site':i},
                headers={'X-Crawlera-Profile':'desktop'})#,download_timeout=600)
                except:
                  pass'''
                if link != '#':
                    if link.endswith('/'):
                        ii = link
                    else:
                        ii = link + '/'
                    yield scrapy.Request(link, self.parse3, meta={'link': link, 'keyword': keyword,
                                                                  'search_operator': search_operator})
                else:
                    pass

    def parse(self, response):
        item = lefta()
        # data=json.loads(response.text)
        for i in response.css('.ext'):
            item['link'] = i.css('::attr(href)').extract_first()
            yield item
        # item['university']=i['institution']['displayName']
        # yield item
        # next_link=data['data']['next_link']
        # if next_link:
        # yield scrapy.Request(next_link+'&format=json',self.parse,
        # headers={'X-Crawlera-Profile':'desktop'})

    def parse2(self, response):
        url = response.css('.r a::attr(href)').extract_first()
        try:
            url2 = url.split('/url?q=')[1].split('&')[0]
        except:
            url2 = url
        yield scrapy.Request(url2, self.parse3, meta={'site': response.meta['site']})
        # urls=response.css('.r a::attr(href)').extract()
        # urls2=[]
        # for url in urls:
        # try:
        #   urls2.append(url.split('/url?q=')[1].split('&')[0])
        # except:
        #  urls2.append(url)
        # for i in urls2:
        # if 'intern' or 'stud' in i:
        #  yield scrapy.Request(i, self.parse3,
        # meta={'university':response.meta['university']},
        # headers={'X-Crawlera-Profile':'desktop'})
        # break
        # lse:
        # pass

    def parse3(self, response):
        item = lefta()
        # item['university']=response.meta['university'],
        item['link'] = response.meta['link']  # response.url,
        # item['email']=response.xpath('//*[contains(text(),"@")]/text()').extract()
        item['email'] = re.findall('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', response.text)
        item['keyword'] = response.meta['keyword']
        item['search_operator'] = response.meta['search_operator']
        ###item['site']=response.meta['site']
        ###coded_email=response.css('.__cf_email__::attr(data-cfemail)').extract_first()
        # item['email2']=self.decodeEmail(coded_email)
        yield item
        # link=response.meta['site'].split('/')[0]+'/'+response.meta['site'].split('/')[2]+'/contact'
        # yield scrapy.Request(link, self.parse4, meta={'site':response.meta['site']})

    def parse4(self, response):
        item = lefta()
        # item['university']=response.meta['university'],
        item['contact_link'] = response.url,
        item['email'] = response.xpath('//*[contains(text(),"@")]/text()').extract()
        item['site'] = response.meta['site']
        coded_email = response.css('.__cf_email__::attr(data-cfemail)').extract_first()
        # item['email2']=self.decodeEmail(coded_email)
        yield item
        link = link.split('/')[0] + '/' + response.meta['site'].split('/')[2] + '/contact-us'
        yield scrapy.Request(link, self.parse5, meta={'site': response.meta['site']})

    def parse5(self, response):
        item = lefta()
        # item['university']=response.meta['university'],
        item['contact_link'] = response.url,
        item['email'] = response.xpath('//*[contains(text(),"@")]/text()').extract()
        item['site'] = response.meta['site']
        coded_email = response.css('.__cf_email__::attr(data-cfemail)').extract_first()
        # item['email2']=self.decodeEmail(coded_email)
        yield item

    def decodeEmail(e):
        de = ""
        k = int(e[:2], 16)

        for i in range(2, len(e) - 1, 2):
            de += chr(int(e[i:i + 2], 16) ^ k)

        return de


class lefta(scrapy.Item):
    # university = scrapy.Field()
    link = scrapy.Field()
    email = scrapy.Field()
    keyword = scrapy.Field()
    search_operator = scrapy.Field()
    # site = scrapy.Field()
    # email2 = scrapy.Field()
    # practice_url = scrapy.Field()
    # practice_url2 = scrapy.Field()
    # link = scrapy.Field()

# df[(df['WebSite of practice'].isna()==True) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('DDS')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('DMD')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('D.D.S')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('D.m.d')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('DR ')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('MD')==False)]['Practice/Clinic/ Business/ Office Name']
# bkWMgd