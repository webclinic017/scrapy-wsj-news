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
from urllib.parse import urlparse
from tencent.items import TencentItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class TencentSpiderSpider(scrapy.Spider):
    name = 'tencent_spider'
    
    def start_requests(self):
        start_urls = []
        for k, v in get_ucodes().items():
            for v1 in v:
                if '.HK' in v1:
                    ucode = v1.replace('.HK', '').zfill(5)
                    url = 'https://qt.gtimg.cn/q=s_hk'+ucode
                    start_urls.append({'url': url, 'ucode': v1})
                elif '.SS' in v1:
                    ucode = v1.replace('.SS', '').replace('.SZ', '').zfill(6)
                    url = 'https://qt.gtimg.cn/q=s_sh'+ucode
                    start_urls.append({'url': url, 'ucode': v1})
                elif '.SZ' in v1:
                    ucode = v1.replace('.SS', '').replace('.SZ', '').zfill(6)
                    url = 'https://qt.gtimg.cn/q=s_sz'+ucode
                    start_urls.append({'url': url, 'ucode': v1})

        for data in start_urls:
            yield scrapy.Request(url=data['url'], headers=get_random_header(), callback=self.parse, meta=data)

    def parse(self, response):
        item = TencentItem()
        item['ucode'] = response.meta.get('ucode')

        data = response.text
        if 'v_pv_none_match' not in data:
            item['nmll'] = data.split('~')[1]
            return item
