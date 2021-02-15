# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IndexItem(scrapy.Item):
    # define the fields for your item here like:
    stime = scrapy.Field()
    ucode = scrapy.Field()
    last = scrapy.Field()
    chng = scrapy.Field()
    pchng = scrapy.Field()
    turnover = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    pass
