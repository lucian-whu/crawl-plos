# Scrapy settings for crawl_plos project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawl_plos'

SPIDER_MODULES = ['crawl_plos.spiders']
NEWSPIDER_MODULE = 'crawl_plos.spiders'
ITEM_PIPELINES= ['crawl_plos.pipelines.CrawlPlosPipeline']
LOG_LEVEL = 'INFO'
#DOWNLOAD_DELAY = 30
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_plos (+http://www.yourdomain.com)'
