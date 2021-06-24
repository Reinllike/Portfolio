#!/usr/bin/env python
# coding: utf-8

# 1.逐筆資料
# 2.對帳單(成交資訊)
# 3.買賣下單功能(可開關)

# In[3]:


#查詢當前(訂閱)
from haohaninfo import GOrder
a = GOrder.GOCommand()
a.AddQuote('Simulator_Stock', '0050')


# # 當前即時報價

# In[ ]:


#逐筆即時報價
from haohaninfo import GOrder
a = GOrder.GOQuote()
for i in a.Subscribe('Simulator_Stock', 'match', '0050'):
    print(i)
    
#一次抓多筆?


# In[ ]:


#停止上述迴圈
from haohaninfo import GOrder
a = GOrder.GOQuote()
for i in a.Subscribe('Simulator_Stock', 'match', '0050'):
    a.EndSubscribe()
#無法暫停


# In[4]:


#最近一筆即時報價
from haohaninfo import GOrder
a = GOrder.GOQuote()
print(a.SubscribeLast('Simulator_Stock', 'match', '0050'))


# # 下單功能

# In[2]:


#下單
from haohaninfo import GOrder
a = GOrder.GOCommand()
b = a.Order('Simulator_Stock', '0050', 'B', '138.1', '1', '1', '0')
#(券商代碼 ,股票代碼 ,B:買入 S:賣出 ,價錢 ,張數 ,0:一般 1:零股 2:定價  ,0:現貨 1:融資 2:融券 3:無券)
print(b)


# In[13]:


#市價單
a = GOrder.GOQuote()
price =(a.SubscribeLast('Simulator_Stock', 'match', '0050')[2]) #當前價格
c = GOrder.GOCommand()
b = c.Order('Simulator_Stock', '0050', 'B', price, '1', '1', '0')
#(券商代碼 ,股票代碼 ,B:買入 S:賣出 ,價錢 ,張數 ,0:一般 1:零股 2:定價  ,0:現貨 1:融資 2:融券 3:無券)
print(b)


# In[ ]:


#限價單
from haohaninfo import GOrder
a = GOrder.GOCommand()
b = a.Order('Simulator_Stock', '0050', 'B', '140', '1', '1', '0')
#(券商代碼 ,股票代碼 ,B:買入 S:賣出 ,價錢 ,張數 ,0:一般 1:零股 2:定價  ,0:現貨 1:融資 2:融券 3:無券)
print(b)


# In[6]:


#刪單
from haohaninfo import GOrder
a = GOrder.GOCommand()
c = a.Delete('Simulator_Stock', 'S2021041600012')
print(c)


# # 對帳單

# In[53]:


#下單紀錄
from haohaninfo import GOrder
a = GOrder.GOCommand()
for i in a. GetAccount('Simulator_Stock', 'All'):
    print(i)
    f = open("stock.txt",'a+')
    f.write(i)
    f.write('\n')
    f.close()

    


# In[14]:


#成交紀錄
from haohaninfo import GOrder
a = GOrder.GOCommand()
for i in a.MatchAccount('Simulator_Stock', 'All'):
    print(i)
    f = open("deal_order.txt",'a+')
    f.write(i)
    f.write('\n')
    f.close()


# In[8]:


#庫存紀錄
from haohaninfo import GOrder
a = GOrder.GOCommand()
for i in a.GetInStock('Simulator_Stock'):
    print(i)
    f = open("Bank_statement.txt",'a+')
    f.write(i)
    f.write('\n')    
    f.close()


# # 歷史日資料

# In[40]:


#日資料(最多過往五年)
from haohaninfo import GOrder
KBar = GOrder.GetHistoryKBar('25','2330','Stock','1')
for i in KBar:
    print(i)#日期 代碼 開盤 最高 最低 收盤 量
    


# In[38]:


a='20210510,6239,105.5,106.0,103.5,105.0,1732'
a=a.split(',')
a[2]


# In[51]:


#下單
from haohaninfo import GOrder
a = GOrder.GOCommand()
symbol=str(2367)
price=23.2
money=33871
amount=str(int((money/price)))
price=str(price)
b = a.Order('Simulator_Stock', symbol, 'B', price, amount, '1', '0')
#(券商代碼 ,股票代碼 ,B:買入 S:賣出 ,價錢 ,張數 ,0:一般 1:零股 2:定價  ,0:現貨 1:融資 2:融券 3:無券)
print(b)


# In[ ]:





# In[ ]:


1.對帳單轉txt
2.限價單 市價單功能
3.限時購買(幾點到幾點購買)


# In[ ]:


1.部位/股價 決定買入股數 無條件捨去
2.買今天開盤 賣開盤
3.


# In[ ]:


永豐金
模擬單 抓價錢
可以算每日資產價格 報酬率

