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

#database 
connection  = mysql.connector.connect(
    host = "#",
    user = "#",
    password = "#",
    database = "#"    
    )
#if connected to the database print <mysql.connector.connection.MySQLConnection object at 0x000001CC6743CFA0>
print(connection)
#for query
cursor = connection.cursor()




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
current_prediction = df[['Sales','forecast']].plot(figsize=(12,8))
plt.show()
#FORECASTING
print("FORECASTING")
future_dates=[df.index[-1]+ DateOffset(months=x)for x in range(0,24)]
future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)
future_datest_df.tail()
future_df=pd.concat([df,future_datest_df])
future_df['forecast'] = results.predict(start = 83, end = 120, dynamic= True)  #GIN PREDICT ANG INDEX 83 TO FUTURE
future_prediction = future_df[['Sales', 'forecast']].plot(figsize=(12, 8))
plt.show()

 

#upload
try: 
    print("image uploaded")
    query1 = "INSERT INTO currentprediction(image)VALUES('%s')" 
    query2 = "INSERT INTO futureprediction(image)VALUES('%s')"
    result1 = cursor.execute(query1, current_prediction)
    result2 = cursor.execute(query2, future_prediction)
    connection.commit()
 
# Print error if occured
except mysql.connector.Error as error:
    print(format(error))
finally:   
    # Closing all resources
    if connection.is_connected():
       
        cursor.close()
        connection.close()
        print("MySQL connection is closed")    


# def write_file(data, filename):
#     with open(filename, 'wb') as f:
#         f.write(data)
        
# def read_blob(author_id, filename):
#     # select photo column of a specific author
#     query = "SELECT image FROM futureprediction WHERE id = %s"  
    
   

#     try:
#         # query blob data form the authors table
    
#         cursor = connection.cursor()
#         cursor.execute(query, (author_id,))
#         photo = cursor.fetchone()[0]
#         # write blob data into a file
#         write_file(photo, filename)
     
   
#     finally:
#         cursor.close()
#         connection.close()
# def main():
#     read_blob(1,"futureprediction.png")
# if __name__ == '__main__':
#     main()

# import sys

# def showFile(blob):
#     print( "Content-Type: image/jpeg\r\n")
#     sys.stdout.flush()
#     print (sys.stdout.buffer.write(image))
   

# def getFile():
#     id = 1
#     sql = "SELECT image FROM futureprediction WHERE id = %s"  
#     cursor.execute(id, sql)
#     data = cursor.fetchone()
#     blob = data[0]

#     return blob

# image = getFile()
# showFile(image)

import mysql.connector

db = mysql.connector.connect(
     host = "#",
    user = "#",
    password = "#",
    database = "#"     
    )
cursor = db.cursor()


def InsertBlob(FilePath):
    with open(FilePath, "rb") as File:
        BinaryData = File.read()
    SQLStatement = "INSERT INTO furrentprediction(image)VALUES('%s')" 
    cursor.execute(SQLStatement, BinaryData, )
    db.commit()

def RetrieveBlob(id):
     SQLStatement2 = "SELECT * FROM futureprediction WHERE id = '{0}'"
     cursor.execute(SQLStatement2.format(str(id)))
     MyResult = cursor.fetchone()[1]
     StoreFilePath = "static/uploads/img{0}.jpg".format(str(id))
     print(MyResult)
     with open(StoreFilePath, "wb") as File:
         File.write(MyResult)
         File.close()


# current_filepath = current_prediction
# future_filepath = future_prediction
# #uploading
# InsertBlob(current_filepath)
# InsertBlob(future_filepath)

