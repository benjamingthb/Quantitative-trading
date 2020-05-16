import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import jqdatasdk
jqdatasdk.auth('user','password')#需要去聚宽注册免费账号使用jqdata，输入用户名和密码
stk_name = '000895.XSHE'
df=jqdatasdk.get_price(stk_name, start_date='2019-12-01', end_date='2020-04-30', frequency='daily')#, fields=['open', 'close'])
#print(df.head())
close = df.close
low = df.low
high = df.high

date = close.index.to_series()
ndate = len(date)
#print(ndate)

prhigh = pd.Series(np.zeros(ndate-8+1),index=date.index[8-1:])
prlow = pd.Series(np.zeros(ndate-8+1),index=date.index[8-1:])

RSV = pd.Series(np.zeros(ndate-8+1),index=date.index[8-1:])

#print(RSV)

for j in range(8-1,ndate):
#    period = date[j-8,j-1]
    i = date[j]
    prhigh[i] = high.iloc[j+1-8:j+1].max() #iloc[a,b] is from a to b-1.
    prlow[i] = low.iloc[j+1-8:j+1].min()
    RSV[i] = 100*(close[i]-prlow[i])/(prhigh[i]-prlow[i])

RSV.name = 'RSV'
#print(RSV.describe())

#plt.rcParams['font.sans-serif'] = ['SimHei']

#close1 = close['2020']
#RSV1 = RSV['2020']
C1_RSV = pd.DataFrame([close,RSV]).transpose()
C1_RSV.plot(subplots=True, title='RSV', figsize=(12,8))
#plt.show()

RSV1 = pd.Series([50,50],index=date[5:7]).append(RSV)
RSV1.name = 'RSV1'
#RSV1.head()
KValue = pd.Series(0.0,index=RSV1.index)
KValue[0] = 50
for i in range(1,len(RSV1)):
    KValue[i] = 2/3*KValue[i-1]+RSV1[i]/3
KValue.name = 'KValue'
#KValue.head()

DValue = pd.Series(0.0,index=RSV1.index)
DValue[0] = 50
for i in range(1,len(RSV1)):
    DValue[i] = 2/3*DValue[i-1]+KValue[i]/3
KValue = KValue[1:]
DValue.name = 'DValue'
DValue = DValue[1:]
#DValue.head()

plt.figure(figsize=(12,8))
plt.subplot(211)
plt.title(stk_name+' close price in 2020')
#plt.plot(close)
plt.plot(close['2020'])
plt.subplot(212)
plt.title(stk_name+' RSV and KD line')
plt.plot(RSV['2020'])
plt.plot(KValue['2020'], linestyle='dashed', label='K')
plt.plot(DValue['2020'], linestyle='-.', label='D')
plt.legend(loc='best')
#plt.show()
plt.savefig('KD')

JValue = 3*KValue - 2*DValue
JValue.name = 'JValue'

plt.figure(figsize=(12,8))
plt.subplot(211)
plt.title(stk_name+' close price in 2020')
#plt.plot(close)
plt.plot(close['2020'])
plt.subplot(212)
plt.title(stk_name+' RSV and KD line')
plt.plot(RSV['2020'])
plt.plot(KValue['2020'], linestyle='dashed', label='K')
plt.plot(DValue['2020'], linestyle='-.', label='D')
plt.plot(JValue['2020'], linestyle='--', label='J')
#plt.legend(loc='upper left')
plt.legend(loc='best')
#plt.show()
plt.savefig('KDJ')