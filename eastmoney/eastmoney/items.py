# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EastmoneyItem(scrapy.Item):
    # define the fields for your item here like:
    stime = scrapy.Field()
    ucode = scrapy.Field()

    retail_inflow_vol = scrapy.Field()
    retail_inflow_turnover = scrapy.Field()
    retail_outflow_vol = scrapy.Field()
    retail_outflow_turnover = scrapy.Field()
    retail_net_money_flow_vol = scrapy.Field()
    retail_net_money_flow_turnover = scrapy.Field()

    major_inflow_vol = scrapy.Field()
    major_inflow_turnover = scrapy.Field()
    major_outflow_vol = scrapy.Field()
    major_outflow_turnover = scrapy.Field()
    major_net_money_flow_vol = scrapy.Field()
    major_net_money_flow_turnover = scrapy.Field()

    overall_inflow_vol = scrapy.Field()
    overall_inflow_turnover = scrapy.Field()
    overall_outflow_vol = scrapy.Field()
    overall_outflow_turnover = scrapy.Field()
    overall_net_money_flow_vol = scrapy.Field()
    overall_net_money_flow_turnover = scrapy.Field()

    pass
