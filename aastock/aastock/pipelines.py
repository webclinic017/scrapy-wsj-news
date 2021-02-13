# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
import sqlite3 as sqlite3
import os
import datetime


class AastockPipeline:
    def __init__(self):
        # 0.0 環境參數
        self.path_root = Path(__file__).parent.parent.parent
        self.path_sqlite = os.path.join(self.path_root, 'data', 'aastock', 'sqlite', 'aastock.db')
        # 2.0
        self.weekday = datetime.datetime.today().weekday()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if self.weekday in [0, 1, 2, 3, 4]:
            conn = sqlite3.connect(self.path_sqlite)
            # 1.0 创建表
            tb_name = 's_'+item['ucode']+'_transaction'
            conn.execute("CREATE TABLE IF NOT EXISTS "+tb_name+" (stime TEXT NOT NULL, ucode TEXT NOT NULL, wtype TEXT NOT NULL, avg REAL, volume REAL, turnover REAL, pct REAL, pct_raw REAL, PRIMARY KEY (stime, ucode, wtype))")

            # 2.0 插值
            data = [item['stime'], item['ucode'], item['wtype'], item['avg'], item['volume'], item['turnover'], item['pct'], item['pct_raw']]
            stmt = "REPLACE INTO "+tb_name+" (stime, ucode, wtype, avg, volume, turnover, pct, pct_raw) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            print(stmt)
            conn.execute(stmt, data)

            conn.commit()
            conn.close()
        return item
