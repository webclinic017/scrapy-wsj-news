import requests
import os
import camelot
import json
import datetime as dt
import numpy as np
import pandas as pd
from io import StringIO
from datetime import datetime
from pathlib import Path
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from lxml import etree
from bs4 import BeautifulSoup


# 1.0 环境设置
url = 'https://www.yieldbook.com/x/ixFactSheet/factsheet_daily_usd.pdf'
path_root = Path(__file__).parent.parent
path1 = os.path.join(path_root, 'data', 'yieldbook', 'factsheet_daily_usd')

# 2.0 下载pdf
path2 = os.path.join(path1, 'tmp')
file2 = os.path.join(path2, 'tmp.pdf')
Path(path2).mkdir(parents=True, exist_ok=True)
if os.path.exists(file2):
    os.remove(file2)
with open(file2, 'wb') as fd:
    r = requests.get(url, stream=True)
    for chunk in r.iter_content(2000):
        fd.write(chunk)


# 3.0 转换html
output = StringIO()
html3 = os.path.join(path2, 'tmp.html')
if os.path.exists(html3):
    os.remove(html3)
with open(file2, 'rb') as pdf_file:
    extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec=None, page_numbers=[1])
with open(html3, 'a') as html_file:
    html_file.write(output.getvalue())


# 4.0 解析1
raw_html = output.getvalue()
parser = etree.HTMLParser()
tree = etree.parse(StringIO(raw_html), parser)
divs = tree.xpath('.//div')
for div in divs:
    ctx = etree.tostring(div)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html")


# 5.0 解析2
soup = BeautifulSoup(raw_html, 'html.parser')
ctx5 = [v.get_text().strip() for v in soup.find_all('div')]
date5 = ctx5[1].split(' ')
years = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
         'november', 'december']
month = int(years.index(date5[4].lower()))+1
day = int(date5[5].replace(',', ''))
year = int(date5[6])
date5_1 = dt.date(year, month, day)


# 6.0 解析3
tables = camelot.read_pdf(file2, pages='1,2', compress=False)
df6_5 = pd.DataFrame()
for df6 in tables:
    df6 = df6.df
    path6 = os.path.join(path2, 'tmp2.html')
    if os.path.exists(path6):
        os.remove(path6)
    df6.to_html(path6)
    # 6.1
    for i, r in df6.iterrows():
        # Local Currency Terms, USD Terms Unhedged, USD Terms Hedged
        if i == 0:
            terms = r.values.tolist()
            del terms[0]
        # Index, Daily, MTD
        elif i == 1:
            types = r[1].split('\n')
        # content
        elif i == 2:
            names = r[0].replace('\n-', '').replace('- \n', '').replace('\n(', '').replace('\nIndex', '').split('\n')
            len6_1, len6_2 = len(r[1].split('\n')), len(types)
            shape6 = (int(len6_1/len6_2), len6_2)
            data6_1 = np.reshape(r[1].split('\n'), shape6)
            data6_2 = np.reshape(r[2].split('\n'), shape6)
            data6_3 = np.reshape(r[3].split('\n'), shape6)
    # 6.2 合并
    df6_1 = pd.DataFrame(data=data6_1, columns=types, index=names)
    df6_2 = pd.DataFrame(data=data6_2, columns=types, index=names)
    df6_3 = pd.DataFrame(data=data6_3, columns=types, index=names)
    df6_4 = pd.concat([df6_1, df6_2, df6_3], axis=1, keys=terms)
    df6_5 = pd.concat([df6_5, df6_4], axis=0)

# 7.0 储存csv
path7_1 = datetime.strftime(date5_1, '%Y-%m')
file7_1 = datetime.strftime(date5_1, '%Y-%m-%d')
path7_2 = os.path.join(path1, path7_1)
Path(path7_2).mkdir(parents=True, exist_ok=True)
file7_2 = os.path.join(path7_2, file7_1+'.csv')
if os.path.exists(file7_2):
    os.remove(file7_2)
df6_5.to_csv(file7_2)


# 8.0 log
file8 = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
path_log = os.path.join(path_root, 'yieldbook', 'log', file8 + '.log')
with open(path_log, 'w', encoding='utf-8') as f:
    json.dump({'time': file8}, f, ensure_ascii=False, indent=4)

# 8.0 git
path_git = os.path.join(path_root, 'run-git.bat')
os.system(path_git)
