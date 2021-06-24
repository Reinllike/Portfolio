#!/usr/bin/env python
# coding: utf-8

# In[7]:


pip install SQLAlchemy


# In[10]:


import backtrader


# In[1]:


"""
主觀交易（編號006，布林帶策略作多）

策略敘述：只在"價格在144EMA之上and金叉"做多，"價格在144EMA之下and死叉"做空
    

因為是做多策略，以下只用作多邏輯
目前暫時設定：
風險承受 1%
盈虧比 1.5:1
本金設定 100000
"""

import backtrader as bt
import pandas as pd
import 資金管理

class 無延遲MACD(bt.Strategy):

    def __init__(self):

        self.inds=dict()

        for i,d in enumerate(self.datas):

            self.inds[d]=dict()

            self.inds[d]['倉位存取']=pd.DataFrame(columns=['時間','部位','價錢','購買兩日內最低價'])
            
            self.inds[d]['EMA12'] = bt.indicators.MovingAverageExponential(d,period=12)
            
            self.inds[d]['EMA26'] = bt.indicators.MovingAverageExponential(d,period=26)
            
            self.inds[d]['EMA144'] = bt.indicators.MovingAverageExponential(d,period=144)
            
            self.inds[d]['ZLMACD'] = (2*self.inds[d]['EMA12']-bt.indicators.MovingAverageExponential(self.inds[d]['EMA12'],period=12))-(2*self.inds[d]['EMA26']-bt.indicators.MovingAverageExponential(self.inds[d]['EMA26'],period=26))
            
            self.inds[d]['DEA'] = bt.indicators.MovingAverageExponential(self.inds[d]['ZLMACD'],period=9)
            
            self.inds[d]['ZLMACDS'] = (2*self.inds[d]['DEA']-
                                      bt.indicators.MovingAverageExponential(self.inds[d]['DEA'],period=9))
            
            self.inds[d]['MACD_crossover']= bt.indicators.CrossOver(self.inds[d]['ZLMACD'], self.inds[d]['ZLMACDS'],plot=False)
            
            self.inds[d]['order'] = None
            
            
            
    def 多單買入(self,張數=None):
        d=self.d
        pos=self.pos
        cash=self.cash
        if not 張數:
            張數=資金管理.固定分數法(剩餘本金=cash,
                               現價=d.close[0],
                               #止損點=d.close[0]-self.inds[d]['ATR'][0],
                               止損點=d.close[0]-0.1,
                               N=0.01)
            張數=(cash/10) / (d.close[0]*1000)
        try:
            self.inds[d]['倉位存取']=self.inds[d]['倉位存取'].append(
                pd.DataFrame([[d.datetime.date(0),'B',d.open[1],張數,min(d.low[0],d.low[-1],d.low[1])]],
                             columns=['時間','部位','價錢','數量','購買兩日內最低價'],
                             index=[d.datetime.date(0)]))#將隔天開盤價存入倉位
            self.對帳單=self.對帳單.append(
                pd.DataFrame([[d._name,d.open[1],張數,'B',cash-(d.open[1]*張數*self.商品單位),float('nan'),float('nan')]],
                             columns=['Symbol','Price','Amount','Sid','Cash','Profit','Return'],
                             index=[d.datetime.date(0)]))
            self.inds[d]['order'] = self.buy(data=d,
                                             size=張數*self.商品單位,
                                             )#購買隔天開盤的股票
        except Exception as e:print(e)
        #print('買入',d._name,'持倉數量:',len(self.inds[d]['倉位存取'].index))
    
    
    def 多單停利(self,賺錢判定,張數=None):
        d=self.d
        pos=self.pos
        cash=self.cash
        if 賺錢判定.sum():
            try:
                for _ in self.inds[d]['倉位存取'][賺錢判定].index:
                    if not 張數:張數=self.inds[d]['倉位存取'][賺錢判定].loc[_].數量
                    損益=(d.open[1]-self.inds[d]['倉位存取'][賺錢判定].loc[_].價錢)*張數*self.商品單位
                    Return=損益/(self.inds[d]['倉位存取'][賺錢判定].loc[_].價錢*張數*self.商品單位)
                    self.inds[d]['order'] = self.sell(data=d,size=張數*self.商品單位)
                    self.對帳單=self.對帳單.append(
                        pd.DataFrame([[d._name,d.open[1],-張數,'Cp',cash+(d.open[1]*張數*self.商品單位),損益,Return]],
                                     columns=['Symbol','Price','Amount','Sid','Cash','Profit','Return'],
                                     index=[d.datetime.date(0)]))
                self.inds[d]['倉位存取']=self.inds[d]['倉位存取'][~賺錢判定]#清空"虧錢倉位"，這個要小心會不會過
            except Exception as e:print(e)
            #print('停利 ',d._name,'持倉數量:',len(self.inds[d]['倉位存取'].index))
            
    
    def 多單停損(self,虧錢判定,張數=None):
        d=self.d
        pos=self.pos
        cash=self.cash
        if 虧錢判定.sum():#如果有"虧錢判定"
            try:
                for _ in self.inds[d]['倉位存取'][虧錢判定].index:#遍歷所有虧錢倉位
                    if not 張數:張數=self.inds[d]['倉位存取'][虧錢判定].loc[_].數量
                    損益=(d.open[1]-self.inds[d]['倉位存取'][虧錢判定].loc[_].價錢)*張數*self.商品單位
                    Return=損益/(self.inds[d]['倉位存取'][虧錢判定].loc[_].價錢*張數*self.商品單位)
                    self.inds[d]['order'] = self.sell(data=d,size=張數*self.商品單位)
                    self.對帳單=self.對帳單.append(
                        pd.DataFrame([[d._name,d.open[1],-張數,'Cl',cash+(d.open[1]*張數*self.商品單位),損益,Return]],
                                     columns=['Symbol','Price','Amount','Sid','Cash','Profit','Return'],
                                     index=[d.datetime.date(0)]))
                self.inds[d]['倉位存取']=self.inds[d]['倉位存取'][~虧錢判定]#清空"收盤小於訊號購買兩日內最低價者"，這個要小心會不會過
            except Exception as e:print(e)
            #print('止損',d._name,'持倉數量:',len(self.inds[d]['倉位存取'].index))
    
    def 開盤前檢查(self,d):
        try :
            d.datetime.date(1)
        except:#如果這是最後一天，那代表你啥都不能做了
            print(d._name,'到期',d.datetime.date(0))
            return 1
        #目前所在的策略物件
        self.d=d
        #pos為目前擁有的股票張數
        self.pos = self.getposition(d).size
        #當前現金
        self.cash=self.broker.getcash()

            
            
    def next(self):

        #print(self.data.datetime.date(0))

        for i,d in enumerate(self.datas):
            
            try :

                d.datetime.date(1)

            except:#如果這是最後一天，那代表你啥都不能做了

                print(d._name,'到期',d.datetime.date(0))

                return


            #pos為目前擁有的股票張數
            pos = self.getposition(d).size



            # Not yet ... we MIGHT BUY if ...
            #入場條件
            if all([
                    self.datas[0].close < self.inds[d]['EMA144'][0],#只在144EMA之下做多
                    #金叉
                    self.inds[d]['MACD_crossover'][0]>0,#MACD金叉
                    #self.inds[d]['ZLMACD'][0]=0,
                    #self.inds[d]['ZLMACD'][-1]<self.inds[d]['DEA'][-1]
                    ]) :
                    self.多單買入(d)
                            

            if pos:#手中持有部位
            
                #停損
                虧錢倉位=self.inds[d]['倉位存取'].價錢 > d.close[0]#計算所有虧錢的倉位
                if 虧錢倉位.sum():#如果有虧錢的倉位
                    虧100元的倉位=self.inds[d]['倉位存取'].價錢-0.1 > d.close[0]#計算所有虧100元的倉位
                    self.多單停損(d,虧100元的倉位)
                    
                        
                
                
                #停利
                賺錢倉位=self.inds[d]['倉位存取'].價錢 < d.close[0]#計算所有賺錢的倉位
                if 虧錢倉位.sum():#如果有虧錢的倉位
                    虧100元的倉位=self.inds[d]['倉位存取'].價錢+0.15 < d.close[0]#計算所有賺150元的倉位
                    self.多單停利(d,賺錢倉位)
                


# In[ ]:




