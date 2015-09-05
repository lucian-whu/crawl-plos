# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PlosSpiderItem(Item):
    # define the fields for your item here like:
    # name = Field()

    pdf_url = Field()
    text_url = Field()
    title = Field()
    count = Field()
    abstract = Field()
    
    pass
