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


class EastmoneyPipeline:
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
        conn = sqlite3.connect(self.path_sqlite)
        # 1.0 创建表
        tb_name = 's_' + item['ucode'] + '_moneyflow'
        stmt = "CREATE TABLE IF NOT EXISTS " + tb_name + " (stime TEXT NOT NULL, ucode TEXT NOT NULL, type TEXT NOT NULL, inflow_vol REAL, inflow_turnover REAL, outflow_vol REAL, outflow_turnover REAL, net_money_flow_vol REAL, net_money_flow_turnover REAL, PRIMARY KEY (stime, ucode, type))"
        conn.execute(stmt)

        # 2.0 散戶
        data = [item['stime'], item['ucode'], 'retail', item['retail_inflow_vol'], item['retail_inflow_turnover'], item['retail_outflow_vol'], item['retail_outflow_turnover'], item['retail_net_money_flow_vol'], item['retail_net_money_flow_turnover']]
        stmt = "REPLACE INTO "+tb_name+" (stime, ucode, type, inflow_vol, inflow_turnover, outflow_vol, outflow_turnover, net_money_flow_vol, net_money_flow_turnover) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        conn.execute(stmt, data)

        # 3.0 大戶
        data = [item['stime'], item['ucode'], 'major', item['major_inflow_vol'], item['major_inflow_turnover'], item['major_outflow_vol'], item['major_outflow_turnover'], item['major_net_money_flow_vol'], item['major_net_money_flow_turnover']]
        stmt = "REPLACE INTO "+tb_name+" (stime, ucode, type, inflow_vol, inflow_turnover, outflow_vol, outflow_turnover, net_money_flow_vol, net_money_flow_turnover) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        conn.execute(stmt, data)

        # 4.0 所有
        data = [item['stime'], item['ucode'], 'overall', item['overall_inflow_vol'], item['overall_inflow_turnover'], item['overall_outflow_vol'], item['overall_outflow_turnover'], item['overall_net_money_flow_vol'], item['overall_net_money_flow_turnover']]
        stmt = "REPLACE INTO "+tb_name+" (stime, ucode, type, inflow_vol, inflow_turnover, outflow_vol, outflow_turnover, net_money_flow_vol, net_money_flow_turnover) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        conn.execute(stmt, data)

        conn.commit()
        conn.close()
        return item
