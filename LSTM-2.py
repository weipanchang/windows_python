#!/usr/bin/env python
# coding: utf-8

import math
import sys
import os
import shutil
import yfinance as yf
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import datetime
from cachetools import cached
from datetime import date
downloadPath = "C:\\Users\\William Chang\\Documents\\Python Scripts\\LSTM"

class Logger(object):
    
    def __init__(self):
        today = date.today()
        global downloadPath
        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\LSTM_Report_"+ today.strftime("%m%d%Y") + ".txt" , "a+")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass   

@cached(cache = {})
def main():
    stock = input("Enter the stock symbol:  ")
    global downloadPath
    os.mkdir(downloadPath + '\\' + stock.upper())
    
    time = datetime.datetime.now().time()

    plt.style.use('fivethirtyeight')

    years_of_data_to_process = 25
    
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    
    start_year =  int(year) - years_of_data_to_process
    start = datetime.datetime(start_year, 1, 1)
    
    df = web.DataReader(stock, data_source='yahoo', start = start, end = date)
#    df =  yf.download(stock, start=start)
    df.dropna(inplace= True)
    #df
    
    #df.shape
    
    # plt.figure(figsize=(16,8))
    # 
    # plt.title(stock.upper())
    # #plt.title( plt.title(str(stock)))
    # plt.plot(df['Close'])
    # plt.xlabel('Date', fontsize=18)
    # plt.ylabel('Close Price USD ($)', fontsize =18)
    # plt.show()
    
    data =df.filter(['Close'])
    dataset = data.values
    training_data_len = math.ceil(len(dataset) *.8)
    #training_data_len
    
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    
    #scaled_data
    
    train_data = scaled_data[0:training_data_len, :]
    x_train = []
    y_train = []
    
    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
        # if i <= 60:
        #     print (x_train)
        #     print (y_train)
        #     print
        
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    x_train = np.reshape(x_train,(x_train.shape[0], x_train.shape[1],1))
    #x_train.shape
    
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
        
    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])
    
#    model.fit(x_train, y_train, batch_size=128, epochs=200)
    model.fit(x_train, y_train, batch_size=128, epochs=200, verbose=2)
#    model.fit(x_train, y_train, batch_size=128, epochs=200, verbose=2)
    
    test_data = scaled_data[training_data_len - 60:, :]
    x_test = []
    y_test =  dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])
    
    x_test = np.array(x_test)
    x_test =  np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    predictions = model.predict(x_test)
    predictions =  scaler.inverse_transform(predictions)
    
    rmse = np.sqrt(np.mean(predictions -y_test) **2)
    
    sys.stdout = Logger()
    
    print("\n\n***************************************************")
    print("  Time:", time)
    print("  Stock Ticket: = %s" %stock.upper(), end = " ")
    print ("    RMSE = %f.4" %rmse)
    print("***************************************************")

    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    plt.figure(figsize=(16,8))
    plt.title(stock.upper())
    plt.xlabel('Data Index', fontsize = 18)
    plt.ylabel('Close Price USD ($)', fontsize = 18)
    plt.plot()
    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right')
#    plt.show()
    today = date.today()
    plt.savefig(downloadPath  + '\\' + stock.upper() + '\\LSTM_' +stock.upper()+ '_' +today.strftime("%m%d%Y") +'.png')
    
    print("\n", valid.tail(15))
    
#    stock_quote = web.DataReader(stock, data_source =  'yahoo', start = start , end = date)
    stock_quote = yf.download(stock, start=start)
    new_df = stock_quote.filter(['Close'])
    last_60_days = new_df[-60:].values
    last_60_days_scaled = scaler.transform(last_60_days)
    X_test = []
    X_test.append(last_60_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test,(X_test.shape[0], X_test.shape[1],1))
    pred_price = model.predict(X_test)
    pred_price = scaler.inverse_transform(pred_price)
    print("\nPrediction Close Price for Tomorrow =  %f.4" %pred_price)
    print ("\n ============> Close Price differs from Predicate Price \n ============> %.4f....%.4f....%.4f....%.4f....%.4f....<=============" %((valid.iloc[-5,0] - valid.iloc[-5,1]), (valid.iloc[-4,0] - valid.iloc[-4,1]),(valid.iloc[-3,0] - valid.iloc[-3,1]),(valid.iloc[-2,0] - valid.iloc[-2,1]),(valid.iloc[-1,0] - valid.iloc[-1,1])))
    
    #stock_quote2 = web.DataReader(stock, data_source =  'yahoo', start = date , end = date)
    #print (stock_quote2['Close'])


if __name__ == "__main__":
    main()

