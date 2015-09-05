"""
plos_spider.py crawls search results on the PLOS One website, and scrapes
article details like title, PDF url and text url

Author: Kathleen Kusworo
"""
import scrapy
import re
from crawl_plos.items import PlosSpiderItem
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import exceptions

class PlosSpider(CrawlSpider):
    name = "plos"

    #this start URL is the archives section of PLOS One.
    #There are only 44 articles so it's good for testing
    start_urls = \
    ['http://www.plosone.org/browse/Archives?startPage=0&filterAuthors=&\
     filterSubjectsDisjunction=&filterArticleTypes=&pageSize=13&filterKeyword=\
     &filterJournals=PLoSONE&query=&ELocationId=&id=&resultView=list&sortValue=&\
     unformattedQuery=*%3A*&sortKey=&filterSubjects=Archives&volume=&']

    count = 1       #article count
    #page_num = 2    #page number count - mainly for testing

    def parse_start_url(self, response):
        #call parse_page for start url
        yield Request(response.url, callback = self.parse_page)

    def parse_page(self,response):
        #grab article url
        urls = response.xpath('//ul[@id="search-results"]//h2/a/@href').extract()

        #add domain to url and call parse_item on each article url
        for url in urls:
            url = 'http://www.plosone.org' + url
            yield Request(url,callback = self.parse_item)

        #grab link for the next page in search results
        next_page = response.xpath('//div[@class="pagination"]//a[@class="next"]/@href').extract()

        #if there is a next page, follow the link and call parse_page on it
        if len(next_page) is not 0:
            next_page_url = 'http://www.plosone.org' + next_page[0].strip()
            yield Request(next_page_url,callback = self.parse_page)
           
    def parse_item(self,response):
        item = PlosSpiderItem()
        item['pdf_url'] = (response.xpath('//div[@class = "dload-pdf"]/a/@href').extract())[0]
        item['text_url'] = response.url
        item['title'] = (response.xpath('//meta[@name = "citation_title"]/@content').extract())[0]
        item['count'] = self.count
        self.count += 1

        #get article's abstract
        abstract = (response.xpath('//div[contains(@class,"abstract")]//p').extract())
        if len(abstract) == 0:
            abstract = (response.xpath('//div[@id = "section1"]//a[not(contains(@id,"disp-quote1"))]/following-sibling::p').extract())
        item['abstract'] = abstract[0]

        #clean up text
        for key in item.keys():        
            if key == 'count' or key == 'text_url':
                continue 
            
            #remove tags, dangling whitespace, and citations
            #fix ampersand characters and spaces before periods
            item[key] = re.sub('<[^>]*>', '', item[key])
            item[key] = item[key].strip()
            item[key] = item[key].replace('&amp;', '&')
            item[key] = re.sub('\[.*\]','',item[key])
            item[key] = re.sub(' \.', '.', item[key])
        
        return item
