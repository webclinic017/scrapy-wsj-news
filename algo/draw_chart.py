import sys
import os
from pathlib import Path
#
path_root = Path(os.path.abspath(''))
sys.path.insert(1, os.path.join(path_root))
#
path_root2 = Path(os.path.abspath('')).parent
sys.path.insert(1, os.path.join(path_root2))
import talib
import sqlite3 as sqlite3
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.font_manager as fm
from mplfinance.original_flavor import candlestick_ohlc
from util.util import get_ucodes

path_sqlite = os.path.join(path_root, 'data', 'aastock', 'sqlite', 'hk-marketwatch.db')
if not os.path.exists(path_sqlite):
    path_sqlite = os.path.join(path_root2, 'data', 'aastock', 'sqlite', 'hk-marketwatch.db')
print(path_sqlite)
conn = sqlite3.connect(path_sqlite)
cursor = conn.cursor()
conn.row_factory = lambda cursor, row: row[0]
no_days = 60

ucodes = []
for k, v in get_ucodes().items():
    for v1 in v:
        if '.HK' in v1:
            ucodes.append(v1.replace('.HK', '').zfill(5))
        elif ('.SS' in v1  and not v1 == '.SSEC') or ('.SZ' in v1 and not v1 == '.SZI'):
            ucodes.append(v1.replace('.SS', '').replace('.SZ', '').zfill(6))
        else:
            ucodes.append(v1.lower().replace('.', ''))

data1 = {}
for ucode in ucodes:
    sql = """SELECT t.code, t.lot, t.nmll, t.stime, t.high, t.low, t.open, t.close, t.volume
                FROM (SELECT n.code, n.lot, n.nmll, c.stime, c.high, c.low, c.open, c.close, c.volume 
                    FROM s_{} AS c INNER JOIN name AS n 
                        ON c.code=n.code ORDER BY c.stime DESC LIMIT 365*20) AS t 
                            ORDER BY t.stime """.format(ucode)
    cursor.execute(sql)
    columns = ['code', 'lot', 'nmll', 'sdate', 'high', 'low', 'open', 'last', 'vol']
    data1[ucode] = pd.DataFrame(cursor.fetchall(), columns=columns)
conn.close()

for k, _df in data1.items():
    df = _df.copy(deep=True)
    if df.shape[0] < no_days:
        df = df.iloc[1:]
    df.fillna(0, inplace=True)
    df.columns = ['code', 'lot', 'nmll', 'sdate', 'High', 'Low', 'Open', 'Close', 'Volume']
    df["Volume"] = pd.to_numeric(df["Volume"])
    df.index = pd.to_datetime(df.sdate)
    df = df.tail(no_days)
    prop = fm.FontProperties(fname='D:/PycharmProjects/scrapy-001/algo/msjh.ttf')
    style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size':12, 'font.family' : 'SimSun'}, gridaxis='both')

    if _df['sdate'].shape[0] > 0:
        stime = _df['sdate'].iloc[-1]
    else:
        stime = ''

    if _df['nmll'].shape[0] > 0:
        title = _df['nmll'].iloc[1]+' '+stime
    else:
        title = k+' '+stime

    path_img = os.path.join(path_root, 'data', 'img')
    if os.path.exists(path_img):
        path_save = os.path.join(path_img, k+'.png')
    else:
        path_img2 = os.path.join(path_root2, 'data', 'img')
        path_save = os.path.join(path_img2, k+'.png')

    if os.path.exists(path_save):
        os.remove(path_save)
        print('del: '+path_save)

    try:
        fig, axs = mpf.plot(df, type='candle', addplot=[], style=style, ylabel='', ylabel_lower='', title=title,
                            volume=True, figratio=(18,10), figscale=1, xrotation=0, datetime_format="%Y-%m-%d", show_nontrading=False,
                            tight_layout=True, scale_width_adjustment=dict(volume=0.6,candle=1), returnfig=True, savefig=path_save)
        print('draw: '+k+' '+path_save)
    except:
        print('err: '+k)

path_git = os.path.join(path_root, 'run-git.bat')
if not os.path.exists(path_git):
    path_git = os.path.join(path_root2, 'run-git.bat')
print(path_git)
os.system(path_git)
