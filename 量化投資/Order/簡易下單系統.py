#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install shioaji


# In[1]:


import pandas as pd
import shioaji as sj
api = sj.Shioaji(simulation=True) 
api.login(
    person_id="PAPIUSER05", 
    passwd="2222", 
    contracts_cb=lambda security_type: print(f"{repr(security_type)} fetch done.")
)


# # 生成下單單據

# In[138]:


import pandas as pd
a=pd.DataFrame(columns=('id','買賣','買價','股數','股本','日期','return rate' ,'收益'))
#a.loc[0]=['1630','1',0,'2',1,1]
a


# In[101]:


def stock(self,money=10,time='日期'):
        self=str(self)
        contracts = [api.Contracts.Stocks[self]]
        snapshots = api.snapshots(contracts)
        df = pd.DataFrame(snapshots)
        df.ts = pd.to_datetime(df.ts)
        price=df.open[0]#當天價格
        price=float(price)
        amount=int((money/price))
        money=price*amount
        a.loc[a.shape[0]]=[self,'買',price,amount,money,time,0,0]
        return(a)


# # 下當日單

# In[27]:


#下單 按照格式輸入代碼 股本 日期
stock(2332,100000,1)


# # 下歷史單

# In[139]:


#日資料(最多過往五年)
from haohaninfo import GOrder
def gorderdata(times,code,date):
    # = GOrder.GetHistoryKBar('25','6239','Stock','1')
    times=str(times)
    code=str(code)
    date=str(date)
    KBar = GOrder.GetHistoryKBar(times,code,'Stock','1')
    for i in KBar: #日期 代碼 開盤 最高 最低 收盤 量       
        if (date in i): 
            i=i.split(',')
            return((i[2])) #抓開盤
#print(KBar) 


# In[140]:


#輸入股本
def stock2(self,money=10,time='日期'): #最多過往五年
    pri=gorderdata(25,self,time) #times code date
    self=str(self)
    price=float(pri) #價格
    amount=int((money/price))
    money=price*amount
    a.loc[a.shape[0]]=[self,'買',price,amount,money,time,0,0]
    return(a)


# In[141]:


#輸入股數
def stock3(self,amount,time='日期'): #最多過往五年
    pri=gorderdata(25,self,time) #times code date
    self=str(self)
    price=float(pri) #價格
    money=price*amount
    a.loc[a.shape[0]]=[self,'買',price,amount,money,time,0,0]
    return(a)


# In[84]:


#下單 按照格式輸入代碼 股本 日期
#輸入股本
#買輸入+ 賣輸入-
stock2(1455,71123,20210503)
#賣出 要計算扣除股數而非股本  並求出收益


# In[147]:


#輸入股數
#買輸入+ 賣輸入-
stock3(1455,4064,20210503)


# # 刪單(擇一)

# In[70]:


#刪單 輸入id
repeated=a[a['id']=='2330'].index
a.drop(repeated,axis=0,inplace=True)
a=a.reset_index(drop=True)


# In[151]:


#刪單 輸入index
a.drop(a.index[1],axis=0,inplace=True)


# In[121]:


a


# # 存本次下單紀錄

# In[122]:


#存本次下單紀錄
#改成存檔路徑 windows用/
i='2021_05_13' #修改日期
file=open('stock/stock%s.txt' %i,'a')
a.to_csv('stock/stock%s.txt' %i,sep='\t',index=False)
file.close()


# # 算本次花費

# In[174]:


i='2021_05_13'


# In[175]:


funds=pd.DataFrame(columns=('日期','資金收入'))


# In[176]:


funds.loc[funds.shape[0]]=[i,-sum(b['股本'])]


# In[177]:


funds


# In[178]:


file2=open('funds/funds%s.txt' %i,'w+')
funds.to_csv('funds/funds%s.txt' %i,sep='\t',index=False)
file2.close()


# # 寫入庫存 

# In[149]:


#寫入庫存 續寫
c.to_csv('Bank_statement.csv',encoding='utf_8_sig', mode='a+',)#header=False utf_8_sig


# # 以下為整理庫存 算報酬率

# In[153]:


#讀取庫存
b=pd.read_csv('Bank_statement.csv') # index_col="id"
b=b.reset_index(drop=True)
b=b.drop(columns=['Unnamed: 0'])

b.drop(b[b['id']=='id'].index,axis=0,inplace=True)
b=b.reset_index(drop=True)
#a=a.drop(a.index[1],axis=0,inplace=True)
b


# # 統整相同ID股票

# In[154]:


#整理相同ID股票  重複使用
for i in range(0,100,1):
    for j in range(i+1,100,1):
        if j > b.index[-1]:
            break
        if b.iloc[i]['id'] == b.iloc[j]['id']:
            b.loc[i,'買價']=float(b.loc[i,'買價'])
            b.loc[i,'股數']=int(b.loc[i,'股數'])
            b.loc[j,'買價']=float(b.loc[j,'買價'])
            b.loc[j,'股數']=int(b.loc[j,'股數'])
            
            buy=b.loc[i,'買價']*b.loc[i,'股數']+b.loc[j,'買價']*b.loc[j,'股數']
            
            b.loc[i,'買價']=(abs(b.loc[i,'買價']*b.loc[i,'股數'])+abs(b.loc[j,'買價']*b.loc[j,'股數']))/(abs(b.loc[i,'股數'])+abs(b.loc[j,'股數'])) ##獲得平均買價
            b.loc[i,'股數']=b.loc[i,'股數']+b.loc[j,'股數'] ##獲得總股數
            b.loc[i,'日期']=b.loc[j,'日期']
            b.loc[i,'股本']=buy
            b.drop(b.index[j],axis=0,inplace=True)
             
        b=b.reset_index(drop=True)

b


# In[166]:


for i in range(0,len(b),1):
    b.iloc[i]['股本'] = float(b.iloc[i]['股本'])         
b


# In[165]:


len(b)


# # 計算報酬 

# In[155]:


#計算報酬
for i in range(0,100,1):
    if i > b.index[-1]:
        break
    b.loc[i,'id']=str(b.loc[i,'id'])
    contracts = [api.Contracts.Stocks[b.iloc[i]['id']]]  ##查詢最新價格
    snapshots = api.snapshots(contracts)
    df = pd.DataFrame(snapshots)
    df.ts = pd.to_datetime(df.ts)
    price = df.open[0]
    price = float(price)
    b.loc[i,'股數']=float(b.loc[i,'股數'])
    b.loc[i,'買價']=float(b.loc[i,'買價'])
    b.loc[i,'return rate'] = price/b.loc[i,'買價']
    b.loc[i,'收益'] = (price - b.loc[i,'買價'])*b.loc[i,'股數']
    
b


# # 更改庫存資料

# In[156]:


#寫入庫存 覆蓋
b.to_csv('Bank_statement.csv',encoding='utf_8_sig', mode='w+',)


# In[ ]:


#5/13 開盤 除了華碩全砍
#我們這禮拜的調整是
停損：
GIS-KY
中興電
亞力
耀華

加新標的：
華碩
集盛


# In[ ]:


#讀取庫存
b=pd.read_csv('0421.csv') # index_col="id"
b=b.reset_index(drop=True)

b.drop(b[b['id']=='id'].index,axis=0,inplace=True)
b=b.reset_index(drop=True)
#a=a.drop(a.index[1],axis=0,inplace=True)
b

