import sys
import os
from pathlib import Path
path_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(1, os.path.join(path_root))

import scrapy
import bs4
import re
import datetime
from urllib.parse import urlparse
from eastmoney.items import EastmoneyItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class WsjSpider(scrapy.Spider):
    name = 'eastmoney'

    def start_requests(self):
        # 1.0
        start_urls = []
        for k, v in get_ucodes().items():
            for v1 in v:
                if '.HK' in v1:
                    ucode = v1.replace('.HK', '').zfill(5)
                    # start_urls.append('http://quote.eastmoney.com/hk/'+v2+'.html')
                    url = 'http://www.aastocks.com/tc/stocks/analysis/moneyflow.aspx?symbol='+ucode
                    start_urls.append({'url': url, 'ucode': ucode})
        # 2.0
        for data in start_urls:
            yield scrapy.Request(url=data['url'], headers=get_random_header(), callback=self.parse, meta={'ucode': data['ucode']})

    def parse(self, response):
        item = EastmoneyItem()
        html = bs4.BeautifulSoup(response.body, 'lxml')
        item['ucode'] = response.meta.get('ucode')

        regex1 = re.compile('.*tblLatest.*')
        for v1 in html.find_all('table', {'class': regex1}):
            v2 = v1.find_all('td')
            if len(v2) >= 31:
                for i in range(len(v2)):
                    v3 = re.sub(r",", '', v2[i].getText()).replace('+', '').replace('$', '')
                    if i == 12:
                        item['retail_inflow_vol'] = float(v3)
                    elif i == 13:
                        item['retail_inflow_turnover'] = float(v3)
                    elif i == 14:
                        item['major_inflow_vol'] = float(v3)
                    elif i == 15:
                        item['major_inflow_turnover'] = float(v3)
                    elif i == 16:
                        item['overall_inflow_vol'] = float(v3)
                    elif i == 17:
                        item['overall_inflow_turnover'] = float(v3)

                    elif i == 19:
                        item['retail_outflow_vol'] = float(v3)
                    elif i == 20:
                        item['retail_outflow_turnover'] = float(v3)
                    elif i == 21:
                        item['major_outflow_vol'] = float(v3)
                    elif i == 22:
                        item['major_outflow_turnover'] = float(v3)
                    elif i == 23:
                        item['overall_outflow_vol'] = float(v3)
                    elif i == 24:
                        item['overall_outflow_turnover'] = float(v3)

                    elif i == 26:
                        item['retail_net_money_flow_vol'] = float(v3)
                    elif i == 27:
                        item['retail_net_money_flow_turnover'] = float(v3)
                    elif i == 28:
                        item['major_net_money_flow_vol'] = float(v3)
                    elif i == 29:
                        item['major_net_money_flow_turnover'] = float(v3)
                    elif i == 30:
                        item['overall_net_money_flow_vol'] = float(v3)
                    elif i == 31:
                        item['overall_net_money_flow_turnover'] = float(v3)

        v4 = html.find('select', {'id': 'cp_ddlDate'})
        item['stime'] = v4.find_all('option', {'selected': 'selected'})[0].getText()
        return item
