import sys
import os
from pathlib import Path
path_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(1, os.path.join(path_root))

import json
import scrapy
import bs4
import re
import datetime
from index.items import IndexItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class YahooSpiderSpider(scrapy.Spider):
    name = 'reuters_spider'

    def start_requests(self):
        start_urls = ['https://www.reuters.com/companies/api/getFetchQuotes/.DJI,.SPX,.IXIC,.HSI,.HSCE,.SSEC,.CSI300']
        for url in start_urls:
            yield scrapy.Request(url=url, headers=get_random_header(), callback=self.parse)

    def parse(self, response):
        item = IndexItem()
        data = json.loads(response.body)
        for v in data['market_data']['indices']:
            print(v)
