#!/usr/bin/env python
# coding: utf-8

# In[ ]:



"""
主觀交易（策略 ATR平均真實波幅指標策略）
日資料策略，下降時ATR峰值較高

因為是做多策略，以下只用作多邏輯

TR:MAX(abs(high-low),(ABS(close(1)-high),(ABS(close(1)-low)))

ATR:MA(TR,N)
N=14

通道:21EMA+-2*ATR

止損:看前低or price-n*ATR
n為2

開倉:1.突破通道邊緣close<21ema-2*ATR 2.回調and不破中線 3.K線型態確認(陽線)

目前暫時設定：
#無風險設定
盈虧比 1.5:1
本金設定 100000
"""
import os
os.chdir('D:\PAP\大腦')#更改路径，''里面为更改的路径
import 資金管理
import backtrader as bt
import pandas as pd
class 策略020(bt.Strategy):
    def __init__(self):
        資金管理.初始設定(self,商品單位=1000)
        for i,d in enumerate(self.datas):
            self.inds[d]['high_20'] = bt.indicators.Highest(d.high,period=20)
            
            self.inds[d]['low_10'] = bt.indicators.Lowest(d.low,period=10)
            
            self.inds[d]['average_hl'] = (self.inds[d]['high_20']+self.inds[d]['low_10'])/2         

            self.inds[d]['EMA55'] = bt.indicators.MovingAverageExponential(d,period=55)

            
    def next(self):
        #print(self.data.datetime.date(0))
        for i,d in enumerate(self.datas):
            if self.開盤前檢查(d):return            

            
            if self.pos:#手中持有部位
            
                #停損
                虧錢倉位=self.inds[d]['倉位存取'].價錢 > d.close[0]#計算所有虧錢的倉位
                if 虧錢倉位.sum():#如果有虧錢的倉位
                    停損的倉位 = d.low[0] <= self.inds[d]['low_10']
                    self.多單停損(停損的倉位) 
                    
                        
                
                
                #停利
                賺錢倉位=self.inds[d]['倉位存取'].價錢 < d.close[0]#計算所有賺錢的倉位
                if 賺錢倉位.sum():#如果有虧錢的倉位
                    停利的倉位 = d.low[0] <= self.inds[d]['low_10']
                    self.多單停利(停利的倉位)
                    
           # Not yet ... we MIGHT BUY if ...
            #入場條件
            if all([d.low[0]>= self.inds[d]['average_hl'],#在黃線上
                    d.low[0]> self.inds[d]['EMA55'],#>EMA55
                    d.high[0]>= self.inds[d]['high_20'],#突破20日K線
                    ]) :
                    self.多單買入(額外添加項={'範例':None})


if __name__ == '__main__':
    import bt系統
    回測=bt系統.系統()
    
    策略名稱=os.path.basename(__file__).split('.')[0]#會載入當前策略
    
    回測回傳字典=回測.運行bt系統(
        策略名稱=策略名稱,
        額外參數={
            #'是否回傳圖片':True,
            #'股票名稱':'2330',
            '標的單位':1000,
            '起始資金':1000000,
            #'添加額外資料':('流通在外股數(千股)',),
            #'添加分析項':True,
            '產業名稱':['建設','PC系統'],
            'startdate':pd.to_datetime('2015-01-01').strftime(format="%Y-%m-%d %H:%M:%S"),
            'enddate':pd.to_datetime('2020-12-31').strftime(format="%Y-%m-%d %H:%M:%S"),
            })
    
    回測.回測完成後的檢查與輸出(存檔=True)


# In[ ]:




