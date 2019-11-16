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


class spider1(scrapy.Spider):
    name = 'google_site_operator3_spider'
    # handle_httpstatus_list = [404, 302]

    # start_urls = ['https://www.google.com/search?q=us+veteran+disabilities+sites+and+blogs']
    # start_urls = ['https://www.google.com/search?q=veteran+disabilities+sites+and+blogs']
    # start_urls = ['https://www.google.com/search?q=us+military+disabilities+sites+and+blogs']
    # start_urls = ['https://www.google.com/search?q=military+disabilities+sites+and+blogs']
    ##start_urls = ['https://www.google.com/search?q=us+internships+sites&start=100']
    # start_urls = ['https://www.google.com/search?q=site%3Achaliklaw.com']
    # start_urls = ['https://www.google.com/search?q=car+accident+inurl%3A%22write-for-us%22&client=ubuntu&hs=ZUL&channel=fs&source=lnt&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2018%2Ccd_max%3A6%2F19%2F2019&tbm=']
    start_urls = [
        'https://www.google.com/search?client=ubuntu&hs=jZ4&channel=fs&ei=vpQKXYfJJsbRwQLKj7qYBA&q=car+accident+%28inurl%3A%22write-for-us%22+and+-site%3Asupermaxlawsuit.com%29']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["keyword", "search_operator", "link"],
    }

    def start_requests(self):
        for url in self.start_urls:
            ##yield scrapy.Request(url,self.parse,
            ##  headers={'X-Crawlera-Profile':'desktop'})
            # df=pd.read_csv('~/Desktop/lawyers_sites2.csv')
            ##df=pd.read_csv('~/Downloads/excluded_domains_1000 - excluded_domains_1000.csv')
            #####last df=pd.read_csv('~/Desktop/all_justia_search_terms.csv')
            ###keywords=['slip and fall']
            # df = pd.read_csv('/home/hronis/Desktop/marcela_outreach/new/outreach_keywords.csv')
            # df2 = df.dmillerlaw.dropna().reset_index(drop=True)
            keywords = ['can be contributing factors that cause collisions',
                        'can be contributing factors that can cause collisions',
                        'can be contributing factors that can cause collisions.',
                        'approximately what percent of crashes are caused by driver error?',
                        'what can be contributing factors that cause collisions',
                        'a lack of is a major factor in traffic crashes',
                        'major contributing factors to traffic accidents',
                        'equipment failure road design and driving behavior',
                        'contributing factors that can cause collisions', 'what are the factors that cause accidents',
                        'a lack of__________is a major factor in traffic crashes',
                        'a lack of blank is a major factor in traffic crashes',
                        'most injury crashes in florida happen in _________ conditions.',
                        'describe three driver errors that could cause a collision',
                        'most injury crashes in florida happen in _________ conditions',
                        'approximately what percent of crashes are caused by driver error?',
                        'what are the two common factors in accidents?',
                        'the behind a vehicle is one of the most common causes of collisions while',
                        'describe three driver errors that could cause a collision.',
                        'which factor was involved in the highest percentage of traffic fatalities',
                        'which of the following is not a leading cause of collisions?',
                        'what causes most car accidents', 'traffic accidents florida',
                        'major causes of traffic accidents', 'most traffic crashes occur',
                        'speeding is one of the most prevalent factors in motor vehicle crashes.',
                        'who causes the most car accidents', 'florida traffic accidents', 'fl traffic accidents',
                        'major cause of traffic accidents', 'what causes the most car accidents',
                        'florida traffic incidents',
                        'nhtsa estimates that aggressive driving accounts for about of all crashes',
                        'a lack of__________is a major factor in traffic crashes',
                        'only 1 of collisions are caused by driver error', 'highway accidents occur most frequently',
                        'what causes most accidents', 'what is contributing factors', 'reasons for accidents',
                        'what is the leading cause of traffic collisions',
                        'what is the most common cause of collisions', 'major car accidents today',
                        'major car accident today', 'what are contributing factors', 'contributing cause',
                        'leading cause of traffic accidents', 'causes of motor vehicle accidents',
                        'most common cause of collisions', 'nhtsa estimates that aggressive driving accounts for about',
                        'automotive accidents', 'main causes of accidents', 'most accidents occur',
                        'number one cause of accidents', 'what is the number one cause of car accidents',
                        'a lack of blank is a major factor in traffic crashes', 'primary collision factor',
                        'is one of the top three factors associated with fatal crashes',
                        'distracted driving contributes to what percent of vehicle collisions',
                        'motor vehicle accidents today']

            operator_keywords = ['guest post', 'guest blogger', 'guest article', 'become a contributor',
                                 'write for us', 'write for me', 'guest Column', 'top 10 blog', 'recommended articles',
                                 'suggested articles', 'favorite articles', 'guest blog', 'contribute to this site',
                                 'contributors', 'add article', 'submit article', 'suggest article', 'post article',
                                 'recommend article', 'guest blogger wanted', 'Guest bloggers wanted', 'add guest post',
                                 'become a guest blogger', 'become a guest writer', 'become an author',
                                 'bloggers wanted',
                                 'blogs that accept guest bloggers', 'blogs that accept guest posts',
                                 'contribute to our site',
                                 'group writing project', 'guest blogging spot', 'guest contributor', 'guest post by',
                                 'guest post guidelines', 'my guest posts', 'now accepting guest posts',
                                 'submission guidelines',
                                 'submit a guest article', 'submit a guest post', 'submit guest post',
                                 'suggest a guest post',
                                 'the following guest post', 'this guest post was written', 'this is a guest article',
                                 'accepting guest posts', 'guest blogging', 'guest posting', 'submit an article',
                                 'submit post',
                                 'submit your post', 'submit content', 'pitch article']

            search_operators = ['intitle:guest post', 'intitle:guest blogger',
                                'intitle:guest article', 'intext:guest post', 'intext:guest blogger',
                                'intext:guest article', 'intitle:blog', 'inurl:blog', 'intext:guest posts',
                                'intext:suggested articles', 'intitle:suggested articles', 'intitle:guest author',
                                'intitle:guest Column', 'inurl:guest Column', 'intext:guest Column',
                                'intitle:recommend article',
                                'intext:recommend article', 'inanchor:guest post', 'inanchor:write for us',
                                'inanchor:write for me',
                                'inanchor:guest author', 'intext:guest author', 'intitle:guest author',
                                'allintext:guest author',
                                'inurl:category/guest', 'inurl:contributors', 'intext:contributors',
                                'intitle:add article',
                                'intitle:suggest article', 'intitle:submit article', 'intitle:post article',
                                'intext:sponsored post',
                                'intitle:“submit” + inurl:blog', 'inpostauthor:guest', 'inpostauthor:“guest blog”',
                                'inpostauthor:guest post', 'intitle:submit post', 'inurl:guest-post-guidelines',
                                'inurl:guest-posts', 'inurl:write-for-us', 'intext:guest-post-guidelines',
                                'intext:guest-posts', 'intext:write-for-us', 'intitle:guest blogger wanted',
                                'intitle:Guest bloggers wanted', 'intitle:add guest post',
                                'intitle:become a guest blogger',
                                'intitle:become a guest writer', 'intitle:become an author', 'intitle:bloggers wanted',
                                'intitle:blogs that accept guest bloggers', 'intext:blogs that accept guest bloggers',
                                'intitle:blogs that accept guest posts', 'intext:blogs that accept guest posts',
                                'intitle:contribute to our site', 'intitle:group writing project',
                                'intitle:guest blogging spot',
                                'intitle:guest contributor', 'intitle:guest post by', 'intitle:guest post guidelines',
                                'intitle:my guest posts', 'intitle:now accepting guest posts',
                                'intitle:submission guidelines',
                                'intitle:submit a guest article', 'intitle:submit a guest post',
                                'intitle:submit guest post',
                                'intitle:suggest a guest post', 'intitle:accepting guest posts',
                                'intitle:guest blogging',
                                'intitle:guest posting', 'intitle:submit an article', 'intitle:submit post',
                                'intitle:submit your post', 'intitle:submit content', 'intext:submit content',
                                'inblogtitle:guest posts', 'inblogtitle:guest blogger', 'inblogtitle:guest Column',
                                'inblogtitle:recommend article', 'inblogtitle:add article',
                                'inblogtitle:suggest article',
                                'inblogtitle:submit article', 'inblogtitle:post article',
                                'inblogtitle:guest blogger wanted',
                                'inblogtitle:Guest bloggers wanted', 'inblogtitle:become a guest writer',
                                'inblogtitle:become an author', 'inblogtitle:bloggers wanted',
                                'inblogtitle:blogs that accept guest bloggers',
                                'inblogtitle:blogs that accept guest posts',
                                'inblogtitle:my guest posts', 'inblogtitle:submission guidelines',
                                'inblogtitle:guest blogging',
                                'inblogtitle:guest posting', 'inblogtitle:submit an article', 'inblogtitle:submit post',
                                'inblogtitle:submit your post', 'inblogtitle:submit content']

            for i in keywords:  # df.search_term:
                for j in search_operators:
                    ##link='https://www.google.com/search?q=inurl%3A'+j.replace(' ','-')+'+'+i.replace(' ','+')
                    ###link='https://www.google.com/search?q='+i.replace(' ','+')+'+'+j.replace(' ','+')+'+%28inurl:'+k.replace(' ','+')+'+and+-site:johnfoy.com+and+-site:sinklaw.com+and+-site:cck-law.com+and+-site:dmillerlaw.com+and+-site:medicalmalpracticehelp.com+and+-site:www.birthinjurylawyer.com+and+-site:losangelesduiattorney.com+and+-site:sevenishlaw.com+and+-site:lilawyer.com+and+-site:zaneslaw.com+and+-site:bergerandgreen.com+and+-site:anidjarlevine.com+-site:ambientedge.com+and+-site:chaliklaw.com+and+-site:disabledvets.com+and+-site:brainandspinalcord.org+and+-site:dallascaraccidentlawyers.net+and+-site:houston-accidentattorney.com+and+-site:rbisenberg.com+and+-site:simmrinlawgroup.com+and+-site:shouselaw.com+and+-site:texasdwilawfirm.com+and+-site:pmhplaw.com+and+-site:friedmansimon.com+and+-site:topclassactions.com+and+-site:miamicaraccidentlawyers.net&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2018%2Ccd_max%3A6%2F19%2F2019'
                    link = 'https://www.google.com/search?q=' + i.replace(' ', '+') + '+' + j.replace(' ',
                                                                                                      '+') + '+and+-site:johnfoy.com+and+-site:sinklaw.com+and+-site:cck-law.com+and+-site:dmillerlaw.com+and+-site:medicalmalpracticehelp.com+and+-site:www.birthinjurylawyer.com+and+-site:losangelesduiattorney.com+and+-site:sevenishlaw.com+and+-site:lilawyer.com+and+-site:zaneslaw.com+and+-site:bergerandgreen.com+and+-site:anidjarlevine.com+-site:ambientedge.com+and+-site:chaliklaw.com+and+-site:disabledvets.com+and+-site:brainandspinalcord.org+and+-site:dallascaraccidentlawyers.net+and+-site:houston-accidentattorney.com+and+-site:rbisenberg.com+and+-site:simmrinlawgroup.com+and+-site:shouselaw.com+and+-site:texasdwilawfirm.com+and+-site:pmhplaw.com+and+-site:friedmansimon.com+and+-site:topclassactions.com+and+-site:miamicaraccidentlawyers.net&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2018%2Ccd_max%3A6%2F19%2F2019&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2018%2Ccd_max%3A6%2F19%2F2019'
                    link2 = 'https://www.google.com/search?q=' + i.replace(' ', '+') + '+' + j.replace(' ',
                                                                                                       '+') + '&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2018%2Ccd_max%3A6%2F19%2F2019&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2018%2Ccd_max%3A6%2F19%2F2019'

                    yield scrapy.Request(link2, self.parse, meta={'keyword': i, 'search_operator': j, 'count': 0},
                                         headers={'X-Crawlera-Profile': 'desktop'})  # ,download_timeout=600)

    def parse(self, response):
        item = lefta()
        for i in response.css('.r'):
            url = i.css('a::attr(href)').extract_first()
            try:
                item['link'] = url.split('/url?q=')[1].split('&')[0]
            except:
                item['link'] = url
            item['keyword'] = response.meta['keyword']
            item['search_operator'] = response.meta['search_operator']
            # item['intitle']=response.meta['intitle']
            ##item['state']=response.meta['state']
            yield item
        ##item['link']=response.xpath('//a[span[text()="Next"]]/@href').extract()
        ##yield item
        # item['number_of_results']=response.css('#resultStats::text').extract_first()
        # item['site']=response.meta['site']

        # yield item
        count = response.meta['count']
        if count < 5:
            count += 1
            next_link = response.urljoin(response.xpath('//a[span[text()="Next"]]/@href').extract_first())
            if next_link:
                yield scrapy.Request(next_link, self.parse,
                                     headers={'X-Crawlera-Profile': 'desktop'},
                                     meta={'keyword': response.meta['keyword'],
                                           'search_operator': response.meta['search_operator'],
                                           'count': count})
                ##count=response.meta['count']+10
        ##if count<1000:
        ##yield scrapy.Request('https://www.google.com/search?q=inurl%3A'+response.meta['inurl'].replace(' ','-')+'+'+response.meta['query'].replace(' ','+')+'&start='+str(count),self.parse,
        ##headers={'X-Crawlera-Profile':'desktop'}, meta={'count':count, 'query':response.meta['query'],
        ##'inurl':response.meta['inurl']})


class lefta(scrapy.Item):
    link = scrapy.Field()
    keyword = scrapy.Field()
    search_operator = scrapy.Field()
    # intitle = scrapy.Field()
    ##state = scrapy.Field()
    # mail = scrapy.Field()
    # practice_url = scrapy.Field()
    # practice_url2 = scrapy.Field()
    # site = scrapy.Field()
    # number_of_results = scrapy.Field()

# df[(df['WebSite of practice'].isna()==True) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('DDS')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('DMD')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('D.D.S')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('D.m.d')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('DR ')==False) & (df['Practice/Clinic/ Business/ Office Name'].str.contains('MD')==False)]['Practice/Clinic/ Business/ Office Name']
# bkWMgd
