# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YahooItem(scrapy.Item):
    # define the fields for your item here like:
    ucode = scrapy.Field()
    last = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    chng = scrapy.Field()
    pchng = scrapy.Field()
    vol = scrapy.Field()
    pe = scrapy.Field()
    eps = scrapy.Field()
