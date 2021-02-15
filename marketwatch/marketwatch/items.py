# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MarketwatchItem(scrapy.Item):
    # define the fields for your item here like:
    ucode = scrapy.Field()
    stime = scrapy.Field()
    last = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    open = scrapy.Field()
    vol = scrapy.Field()
    pass
