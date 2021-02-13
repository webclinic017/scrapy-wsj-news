# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AastockItem(scrapy.Item):
    # define the fields for your item here like:
    stime = scrapy.Field()
    ucode = scrapy.Field()
    wtype = scrapy.Field()
    avg = scrapy.Field()
    volume = scrapy.Field()
    turnover = scrapy.Field()
    pct = scrapy.Field()
    pct_raw = scrapy.Field()
    pass
