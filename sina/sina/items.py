# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    stime = scrapy.Field()
    ucode = scrapy.Field()
    price = scrapy.Field()
    volume = scrapy.Field()
    pct = scrapy.Field()
    type = scrapy.Field()
    pass
