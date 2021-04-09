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
from wsj.items import WsjItem
from util.util import get_random_header, remove_line, remove_first_end_spaces


class WsjSpider(scrapy.Spider):
    name = 'wsj'

    def start_requests(self):
        start_urls = ['https://www.wsj.com/news/markets',
                      'https://www.wsj.com/news/economy',
                      'https://www.wsj.com/news/technology',
                      'https://www.wsj.com/news/business',
                      'https://www.wsj.com/news/world',
                      'https://www.wsj.com/news',
                      'https://www.wsj.com/news/politics',
                      'https://www.wsj.com/news/opinion',
                      'https://www.wsj.com/news/life-arts']
        for url in start_urls:
            yield scrapy.Request(url=url, headers=get_random_header(), callback=self.parse)

    def parse(self, response):
        item = WsjItem()
        html = bs4.BeautifulSoup(response.body, 'lxml')

        # 父頁
        regex = re.compile('.*WSJTheme--headline--.*')
        for v in html.find_all('div', {'class': regex}):
            url = v.find_all('a', href=True)[0]['href']
            # title = v.getText()
            yield scrapy.Request(url=url, headers=get_random_header(), callback=self.parse)

        # 子頁
        # 網址
        item['url_original'] = response.url
        # 網頁名
        item['url'] = urlparse(response.url).path.replace('/articles/', '')

        regex2 = re.compile('.*wsj-article-headline-wrap.*')
        for v2 in html.find_all('div', {'class': regex2}):
            # 標題
            title2 = v2.find_all('h1', class_='wsj-article-headline')[0].getText()
            item['title'] = remove_line(title2)
            # 副標題
            sub_head2 = v2.find_all('h2', class_='sub-head')
            if sub_head2:
                item['sub_head'] = remove_line(sub_head2[0].getText())
            else:
                item['sub_head'] = ''

        # 新聞分類
        regex3 = re.compile('.*article-breadCrumb-wrapper.*')
        for v3 in html.find_all('span', {'class': regex3}):
            category = v3.find_all('a')
            # 主分類
            if len(category) >= 1:
                item['category_1'] = remove_line(category[0].getText())
            # 次分類
            if len(category) >= 2:
                item['category_2'] = remove_line(category[1].getText())

        # 圖片
        regex4 = re.compile('.*article__inset__image__image.*')
        for v4 in html.find_all('div', {'class': regex4}):
            # 圖片網址
            item['image_1_url'] = v4.find_all('img')[0]['src']
            # 圖片名
            item['image_1'] = urlparse(item['image_1_url']).path.replace('/', '')
            if '.jpg' not in item['image_1']:
                item['image_1'] = item['image_1']+'.jpg'

        # 時間
        regex5 = re.compile('.*timestamp.*')
        for v5 in html.find_all('time', {'class': regex5}):
            time5 = remove_line(v5.getText())
            # 日
            day5 = re.sub('\D', '', time5.split(',')[0])
            # 月
            month5 = re.sub(r'\d+', '', time5.split(',')[0].lower()).replace('.', '').replace('updated', '')
            month5 = "".join(month5.split())
            month6 = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
                      'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
            month7 = None
            if month5 in month6:
                month7 = month6[month5]
            # 年
            year5 = re.sub('\D', '', time5.split(',')[1])[:4]
            # 時 $ 分 & 早/晚
            ms5 = time5.split(',')[1].split(' ')
            hour5 = ms5[2].split(':')[0]
            min5 = ms5[2].split(':')[1]
            ms6 = ms5[3].lower()
            if ms6 == 'pm' and int(hour5) < 12:
                hour5 = int(hour5) + 12
            time5_1 = datetime.datetime(int(year5), int(month7), int(day5), int(hour5), int(min5), 0)
            item['time'] = time5_1.strftime('%Y-%m-%d %H:%M:%S')

        # 正文
        regex6 = re.compile('.*wsj-snippet-body.*')
        for v6 in html.find_all('div', {'class': regex6}):
            body6 = [remove_first_end_spaces(v6_1.get_text().replace('\n', '')) for v6_1 in v6.find_all('p')]
            item['body'] = '<br />'.join(body6)

        yield item
