from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import yfinance as yf
import datetime
import os.path
import sys


import backtrader as bt


class MyStochastic1(bt.Indicator):

    lines = ('k', 'd', )  # プロットに表示するlinesオブジェクト
    params = (
        ('k_period', 14), # パラメーターをタプルのタプルで指定する
        ('d_period', 3),  # タプルの最後にもコンマ(、)をいれる
    )

    #省略
    #plotinfo = dict()

    def __init__(self):
        # 正確にはself.datas[0]と書くが省略可能
        # self.params.k_periodを省略してself.p.k_period
        highest = bt.ind.Highest(self.data, period=self.p.k_period)
        lowest = bt.ind.Lowest(self.data, period=self.p.k_period)

        self.lines.k = k = (self.data - lowest) / (highest - lowest)
        self.lines.d = bt.ind.SMA(k, period=self.p.d_period)



class TestStrategy(bt.Strategy):
    def __init__(self):
        #インスタンス名myind1の部分は任意の名前でいい
        self.myind1 = MyStochastic1(self.data)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    data = bt.feeds.PandasData(dataname=yf.download('2800.HK', '2020-01-01', '2022-06-08', auto_adjust=False))

    cerebro.adddata(data)
    cerebro.run(stdstats=False)
    cerebro.plot(style='candle')