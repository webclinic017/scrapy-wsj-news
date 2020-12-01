# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WsjItem(scrapy.Item):
    # define the fields for your item here like:
    url_original = scrapy.Field()   # 網址
    url = scrapy.Field()            # 網頁名

    title = scrapy.Field()          # 標題
    sub_head = scrapy.Field()       # 副標題

    category_1 = scrapy.Field()     # 主分類
    category_2 = scrapy.Field()     # 次分類

    image_1 = scrapy.Field()        # 圖片名
    image_1_url = scrapy.Field()    # 圖片網址

    time = scrapy.Field()           # 時間
    body = scrapy.Field()           # 正文
