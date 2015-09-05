# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os

class CrawlPlosPipeline(object):
    def __init__(self):
        corpus_dir = 'C:\\Users\\Kathleen\\repo\\crawl_plos\\data\\'
        self.filehandle = codecs.open(corpus_dir + 'results.json','w', encoding = 'utf-8')
        self.filehandle.write('[')
        self.is_first_item = True
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        if not self.is_first_item:
            line = ",\n" + line
        self.filehandle.write(line)
        self.is_first_item = False
        return item

    def close_spider(self,spider):
        self.filehandle.write(']')
        self.filehandle.close()
