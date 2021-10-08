# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:41:47 2021

@author: gtxnn
"""
#disable python warnings

#import warnings
#warnings.filterwarnings("ignore")
#ARIMA SALES PREDICTION
#save to db
import mysql.connector
import base64
import io
#import dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#import testing dependencies
from statsmodels.tsa.stattools import adfuller

#AUTO REGRESSIVE MODEL DEPENDENCIES
from pandas.plotting import autocorrelation_plot
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
from pandas.tseries.offsets import DateOffset




#DATASET IS SALES FROM 2015 - 2021
df = pd.read_csv("arima_sales.csv")

#convert month into datetime format
#df['MONTH']= datetime(df['Month'])
df['Month']= pd.to_datetime(df.Month)
print("1st 5 rows")
print(df.head())
print("last 5 rows")
print(df.tail())

#convert Month into DateTime
print("convert Month into DateTime")
#df['Month']=pd.to_datetime(df['Month'])
#print(df.head())
df.set_index('Month', inplace=True)
print(df.head())
#descirbe
print("describe")
print(df.describe())

#VISUALIZE DATA
print("VISUALIZE DATA")
df.plot()
plt.show()


#TESTING
#ADFULLER TEST OR AUGMENTED DICKEY-FULLER IS USED TO CHECK IF TIME SERIES DATA IS STATIONARY OR NOT
print("TESTING")
test_result=adfuller(df['Sales'])
#WHY THE 1ST LINEAR PREDICTION MODEL FAILED? 
#To obtain useful results you can't use nonstationary data with OLS and time series.There are other more advanced methods where nonstationarity is a non issue. With OLS you have to difference real GDP and indices, and also apply log transform in many cases.
#https://stats.stackexchange.com/questions/94723/using-non-stationary-time-series-data-in-ols-regression
#HYPOTHESIS
#Ho: It is non stationary
#H1: It is stationary
def adfuller_test(sales):
    result=adfuller(sales)
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
    for value,label in zip(result,labels):
        print(label+' : '+str(value) )
    if result[1] <= 0.05:
        print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
    else:
        print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")
#test value of sales
adfuller_test(df['Sales'])
#THE DATA IS STATIONARY
#stationary vs non stationary
#https://www.investopedia.com/articles/trading/07/stationary.asp

#DIFFERENCING
print("Sales First Difference")
df['Sales First Difference'] = df['Sales'] - df['Sales'].shift(1)
df['Sales'].shift(1)
print(df.head())

print("Seasonal Difference")
df['Seasonal First Difference'] = df['Sales'] - df['Sales'].shift(12)
print(df.head(14))



#kumbaga GROWTH RATE kng pila nag taas or pila nag nubo
#test adfuller
print("Seasonal First Difference")
adfuller_test(df['Seasonal First Difference'].dropna())
print("Seasonal First Difference Plot")
df['Seasonal First Difference'].plot()
plt.show()


#Auto Regressive Model
#this shows kung kapila mag fluctuate or called lags and can be done only sa autocorrelation plot
autocorrelation_plot(df['Sales'])
plt.show()

#FOR NON SEASONAL DATA
#ARIMA
#print("ARIMA MODEL")
#model=ARIMA(df['Sales'],order=(1,1,1))
#model_fit=model.fit()
#model_fit.summary()
#df['forecast']=model_fit.predict(start=90,end=103,dynamic=True)
#df[['Sales','forecast']].plot(figsize=(12,8))
#SINCE IT IS SEASONAL DATA ARIMA WILL NOT WORK WELL
# #SEASONL ARIMAX
print("SARIMAX MODEL")
model=sm.tsa.statespace.SARIMAX(df['Sales'],order=(1, 1, 1),seasonal_order=(1,1,1,12))
results=model.fit()
#PREDICT
df['forecast']=results.predict(start=60,end=85,dynamic=True)#GIN PREDICT ANG INDEX 60 T O 85
df[['Sales','forecast']].plot(figsize=(12,8))
plt.show()
#FORECASTING
print("FORECASTING")
future_dates=[df.index[-1]+ DateOffset(months=x)for x in range(0,24)]
future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)
future_datest_df.tail()
future_df=pd.concat([df,future_datest_df])
future_df['forecast'] = results.predict(start = 83, end = 120, dynamic= True)  #GIN PREDICT ANG INDEX 83 TO FUTURE
future_df[['Sales', 'forecast']].plot(figsize=(12, 8))
plt.show()

 
