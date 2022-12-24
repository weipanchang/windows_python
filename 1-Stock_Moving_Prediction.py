#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import sys
import shutil
from path import Path
import os
import re
import pandas as pd
import time
import statsmodels.api as sm
import datetime
import shutil
import string
import logging
import argparse
# import pickle

from dateutil.relativedelta import relativedelta
from datetime import date
#from cachetools import cached

pd.set_option('mode.use_inf_as_na', True)

logging.basicConfig(level=logging.INFO)
Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()

downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Prediction"
# downloadPath_pickle = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Pickle"
stock = ""
cutoff =0.50
class Logger(object):

    def __init__(self):

        today = date.today()
#        d1 = today.strftime("%m%d%Y")
        try:
            shutil.rmtree(downloadPath)
            # shutil.rmtree(downloadPath_pickle)
        except:
            pass
        time.sleep(2)

        try:
            os.mkdir(downloadPath)
            # os.mkdir(downloadPath_pickle)
        except:
            pass
        # time.sleep(2)
        self.terminal = sys.stdout
        i =0
        delay = 0
        while i < 2:
            # i += 1
            # time.sleep(delay * 10 + 1)
            try:
                self.log = open(downloadPath + "\\Individual_Stock_Report_" + stock.upper() + '_' + today.strftime("%m%d%Y") + ".txt" , "a+")
                break
            except:
                continue
        else:
            print ("Log file permission denied, aborted!")
            sys.exit()
            

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

def rsi(df1, period):
    
    for i in range(len(df1)):
        if df1.iloc[i,9] <= 0:
            df1.iloc[i,24] = 0
            df1.iloc[i,25] = df1.iloc[i,9]
        else:
            df1.iloc[i,25] = 0
            df1.iloc[i,24] = df1.iloc[i,9]

    AVG_Gain = df1.Up.ewm(span=period, adjust=False).mean()
    AVG_Loss = df1.Down.ewm(span=period, adjust=False).mean().abs()


    RS = AVG_Gain /AVG_Loss
    RSI = 100.0 - (100.0 / (1.0 + RS))
    df1['RSI'] = RSI
    df1['RSI_Lag'] = df1['RSI'].shift(1)

def confusion_matrix(act,pred, cutoff):
    predtrans = ['Up' if i > cutoff else 'Down' for i in pred]
    actuals = ['Up' if i > 0 else 'Down' for i in act]
    confusion_matrix = pd.crosstab(pd.Series(actuals),
                                   pd.Series(predtrans),
                                   rownames = ["Actual"],
                                   colnames = ["Predict"]
                                  )
    return confusion_matrix


def buy_sell(open_price, sell_price,prediction, money, share):
    if prediction == 1 and money != 0:
        share =  money / open_price
        money = 0
    elif prediction == 0 and share != 0:
        money = share * sell_price
        share = 0
    else: pass
    return [money, share]


def read_in_line():
#    stocks = input("Enter the stock symbol: (Ctr-C to Exit, RETURN for batch process from Stock.txt)  ")
    parser = argparse.ArgumentParser(description='Process Stock Price Predication')

    parser.add_argument(
        '-l ',   # either of this switches
        nargs='*',       # one or more parameters to this switch
        type=str,        # /parameters/ are str
        dest='stock_lst',      # store in 'lst'.
        default=None,      # since we're not specifying required.
        help='Manual Input Stock Symbol List, or RETURN for batch process from Stock.txt'
    )
#    args = parser.parse_args()

    return parser.parse_args()

def main():

    short_moving_average_span = 20
    long_moving_average_span = 50
    global cutoff
#    cutoff=0.51
    invest = 100
    years_of_data_to_process = 25
    period = 5

    time = datetime.datetime.now().time()
    date = datetime.datetime.now().date()

    # try:
    #     shutil.rmtree(downloadPath + '\\Individual_Stock_Report_' + stock.upper())
    #
    # except:
    #     pass
    try:
        os.mkdir(downloadPath + '\\' + stock.upper())
    except:
        pass
    year = date.strftime("%Y")
    start_year =  int(year) - years_of_data_to_process
    start = datetime.datetime(start_year, 1, 1)

    print("\n\n*************************************************")
    print("             Stock Ticket: = %s" %stock.upper())
    data =  yf.download(stock, start=start)
    if data.empty:
        return
    print("\n", data.tail())
    df = data["Close"].pct_change() * 100

    df = df.rename("Today_Change_%")
    df = df.reset_index()

    df1 = pd.merge(data,df, on="Date")

    df1.insert(7,'Volume_Lag', None)
    df1.Volume = df1.Volume.pct_change()
    df1['Volume_Lag'] = df1.Volume.shift(1).values

    df1["Trend"] =  (df1["Close"] - df1["Low"])/ ((df1["High"] - df1["Low"]))
    df1["Trend_Lag"] = df1["Trend"].shift(1)

    df1['High-Low_Change_%'] = (df1['High'].pct_change() + df1['Low'].pct_change()).shift(1)

    df1 = sm.add_constant(df1)
    df1["Up_Down"] = [1 if (i > 0) else 0 for i in df1["Today_Change_%"]]

    df1.dropna(inplace= True)

    df1['Short_MV_Avg_Span'] = df1['Close'].ewm(span=short_moving_average_span, adjust=False).mean()
    df1.dropna(inplace= True)

    df1['Long_MV_Avg_Span'] = df1['Close'].ewm(span=long_moving_average_span, adjust=False).mean()
    df1.dropna(inplace= True)

    df1['Short_MV_Avg_Span-Long_MV_Avg_Span'] = df1.Short_MV_Avg_Span - df1.Long_MV_Avg_Span
    df1['Short_MV_Avg_Span-Long_MV_Avg_Span_Lag'] = df1['Short_MV_Avg_Span-Long_MV_Avg_Span'].shift(1)
    df1.dropna(inplace= True)

    df1.index = pd.RangeIndex(start=0,stop = len(df1), step = 1)
    df1.reindex()

    fig, ax1 = plt.subplots()
    ax2 =  ax1.twinx()
    df1['Close'][-150:].plot(x = 'Index', color='tab:blue', figsize=(16,6), label = 'Close Price USA ($)', fontsize = 12, ax = ax1)
    df1['Short_MV_Avg_Span'][-150:].plot(x = 'Index', color='tab:red', figsize=(16,6), label = str(short_moving_average_span) + ' Days Moving Average', fontsize = 12, ax = ax1)
    df1['Long_MV_Avg_Span'][-150:].plot(x = 'Index', color='tab:green', figsize=(16,6), label = str(long_moving_average_span) + ' days Moving Average', fontsize = 12, ax = ax1)
    df1['Short_MV_Avg_Span-Long_MV_Avg_Span_Lag'][-150:].plot(x = 'Index', color='tab:brown', figsize=(16,6), label = 'Signal_line', fontsize = 12, ax = ax2)
    plt.xlim([len(df1)-120, len(df1)])
    ax1.set_ylabel('Close Price USD ($)', fontsize = 18)
    ax2.set_ylabel('Signal_line', fontsize = 18)

    ax2.grid(color='tab:brown')
    ax1.set_title("Moving Average & Signal Line for " + stock.upper(), fontsize = 16)
    ax1.legend(loc=2, fontsize = 16)
    ax2.legend(loc=4,fontsize = 16)
    # plt.show
    # plt.close()

    today = date.today()
    plt.savefig(downloadPath + '\\' + stock.upper() +'\\Individual_Stock__MV_Average_ &_Signal_Line_Report_' +stock.upper()+ '_' +today.strftime("%m%d%Y") +'.png')
    plt.close()

    df1['Signal_Line'] = df1['Short_MV_Avg_Span-Long_MV_Avg_Span_Lag'].ewm(span = period, adjust=False ).mean()
    df1['Signal_Line_Lag'] =  df1['Signal_Line'].shift(1)
    df1.dropna(inplace= True)

    X = df1[['const','Trend_Lag','High-Low_Change_%','Signal_Line_Lag','Volume_Lag']]

    y = df1["Up_Down"].values

    model = sm.Logit(y,X)

    result =  model.fit()
    result.summary()

    prediction = result.predict(X)

    df1['Prediction_Caculated'] = pd.array(prediction)
    df1['Prediction_indicator'] = pd.array([1 if i > cutoff else 0 for i in prediction])

    y = df1["Up_Down"].values

    confusion_matrix(y, prediction, cutoff)
    
#    z = confusion_matrix(y,prediction)

    # try:
    #     print((z.loc['Down','Down'] + z.loc['Up','Up']) / len(df1))
    # except:
    #     pass
    #
    # try:
    #     print( (z.loc['Down', 'Down']+ z.loc['Up','Up']) / (z.loc['Down', 'Down']+ z.loc['Up','Up'] + z.loc['Down','Up']) )
    # except:
    #     pass

    df1 = df1.assign(share=np.nan,money=np.nan)

    diff_years = round((df1.iloc[-1,1] - df1.iloc[0,1])/np.timedelta64(1,'Y') + 0.5)

    df1['Signal_Line_Lag'] = df1['Signal_Line'].shift(1)
    df1=df1[['const', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Volume_Lag', 'Today_Change_%', 'Trend', 'Trend_Lag', 'High-Low_Change_%', 'Up_Down', 'Short_MV_Avg_Span', 'Long_MV_Avg_Span', 'Short_MV_Avg_Span-Long_MV_Avg_Span', 'Short_MV_Avg_Span-Long_MV_Avg_Span_Lag', 'Prediction_Caculated', 'Prediction_indicator', 'share', 'money', 'Signal_Line', 'Signal_Line_Lag']]

    money = invest
    share = 0

    for i in range(len(df1)):
        [money, share] = buy_sell(df1.iloc[i,2],(df1.iloc[i,3]+df1.iloc[i,4])/2,df1.iloc[i,19], money, share)
        df1.iloc[i,20] = share
        df1.iloc[i,21] = money

    df1 = df1.assign(Up=np.nan,Down=np.nan)

    rsi(df1, period)

    fig, ax1 = plt.subplots()
    ax2 =  ax1.twinx()
    df1['RSI'][-150:].plot(x = 'Index', color='tab:red', figsize=(16,6), label = 'Relative Strength Index', fontsize = 12,ax = ax2)
    df1['Close'][-150:].plot(x = 'Index',color = 'tab:blue', figsize=(16,6),  label = 'Close Price',fontsize = 12,ax = ax1)
    plt.xlim([len(df1)-100, len(df1)])
    ax2.set_ylabel('Relative Strength Index', fontsize = 18)
    ax1.set_ylabel('Close Price USD ($)', fontsize = 18)
    #df1.xlabel('Index', fontsize=18)
    #df1.ylabel('Relative Strength Index', fontsize =18)
    ax2.grid(color='tab:red')
    ax1.set_title("Relative Strength Index for " + stock.upper(), fontsize = 16)
    ax2.legend(loc=3, fontsize = 16)
    ax1.legend(loc=2,fontsize = 16)
    # plt.show
    # plt.close()

    plt.savefig(downloadPath + '\\' + stock.upper() + '\\Individual_Stock__RSI_Report_' +stock.upper()+ '_' +today.strftime("%m%d%Y") +'.png')
    plt.close()

    fig, ax1 = plt.subplots()
    ax2 =  ax1.twinx()
#    ax3 =  ax1.twinx()
    #ax3.spines.right.set_position(("axes", 1.2))
    df1['Trend_Lag'][-150:].ewm(span = period, adjust=False ).mean().plot(x = 'Index', color='tab:red', figsize=(16,6), label = 'Buying Trend', fontsize = 12,ax = ax2)
#    df1['High-Low_Change_%'][-150:].ewm(span = period, adjust=False ).mean().plot(x = 'Index', color='tab:green', figsize=(16,6), label = 'High-Low_Change', fontsize = 12, ax = ax3)
    df1['Close'][-150:].plot(x = 'Index',color = 'tab:blue', figsize=(16,6),  label = 'Close Price',fontsize = 12,ax = ax1)
    ax2.set_ylabel('Buying Trend', fontsize = 18)
#    ax3.set_ylabel('High-Low_Change', fontsize = 18)
    ax1.set_ylabel('Close Price USD ($)', fontsize = 18)
    plt.xlim([len(df1)-100, len(df1)])
    ax2.grid(color='tab:red')
    ax1.set_title("Buying Trend for " + stock.upper(), fontsize = 16)
    ax2.legend(loc=3, fontsize = 16)
#    ax3.legend(loc=4, fontsize = 16)
    ax1.legend(loc=2,fontsize = 16)
#    plt.show

    plt.savefig(downloadPath + '\\' + stock.upper() + '\\Individual_Stock__Buying_Trend_Report_' +stock.upper()+ '_' + today.strftime("%m%d%Y") +'.png')
    plt.close()

    df1.dropna(inplace= True)
    X = df1[['const','Trend_Lag', 'RSI_Lag', 'Signal_Line_Lag','Volume_Lag']]
    y = df1["Up_Down"].values
    model = sm.Logit(y,X)
    result =  model.fit()

    print(result.summary())
    print("\nIf ${:,.0f} was invested in [ {} ], and Just Hold and Not Trade for {:2d} years, the ROI = ${:,.0f}".format( invest, stock.upper(), diff_years, invest/data.iloc[0, 0] * data.iloc[-1,0]))
    print ("\nIf ${:,.0f} was invested {:2d} years ago, buy and sell according this script\'s recommandation, the ROI = ${:,.0f}".format(invest, diff_years, (money + (share * df1.iloc[-1,5]))))


    df1_summary=df1[['Date', 'Up_Down','Prediction_indicator']].copy()
    df1_summary['Stock Market Performance'] = df1_summary['Up_Down'].apply(lambda x: 'Up' if x > 0 else 'Down')
    df1_summary['Predection'] = df1_summary['Prediction_indicator'].apply(lambda x: 'Up' if x > 0 else 'Down')


    print ("\nToday [ %s ] actually went up," %stock.upper(), end = ' ') if (df1.iloc[-1,13] == 1) else print ("\nToday [ %s ] actually went down," %stock.upper(), end = " ")
    print ("--- base on yesterday\'s data, ", end = '')
    print ("We Predication [ %s ] should be going up." %stock.upper()) if (df1.iloc[-1,19] == 1) else print ("We Predicae [ %s ] should be going down." %stock.upper())
    print ("\n=========> Actual and Predication MATCH <=========\n") if (df1.iloc[-1,13] == df1.iloc[-1,19]) else print("\n=========> Actual and Predication DO NOT match <=========\n")

    x_tran= df1[df1.Date.dt.year < 2021][['const','Trend_Lag','High-Low_Change_%', 'RSI_Lag','Signal_Line_Lag','Volume_Lag']]
    y_train=df1[df1.Date.dt.year < 2021]["Up_Down"]
    x_test= df1[df1.Date.dt.year >= 2021][['const','Trend_Lag','High-Low_Change_%', 'RSI_Lag','Signal_Line_Lag','Volume_Lag']]
    y_test= df1[df1.Date.dt.year >= 2021]["Up_Down"]

    model = sm.Logit(y_train,x_tran)
    result = model.fit()
    # with open(downloadPath_pickle + '\\' + stock.upper()+'.result.pickle', 'wb') as pickle_file:
    #     pickle.dump(result,pickle_file)

    print("\n",result.summary())

    prediction = result.predict(x_test)
#    confusion_matrix(y_test, prediction, cutoff)

    z = confusion_matrix(y_test,prediction, cutoff)

    try:
        print ("\n=========> Prediction Accuracy Rate: %.4f <=========\n"  %((z.loc['Down','Down'] + z.loc['Up','Up']) / len(x_test)))
    except:
        print ("\n=========> Predication effectiveness is not avairable <=========\n" )

    High_Low=((df1.iloc[-1,3]-df1.iloc[-2,3])/df1.iloc[-1,3] + (df1.iloc[-1,4]-df1.iloc[-2,4])/df1.iloc[-1,4])
#    print(df1.info())
    print(df1[['Date','Open','Close','High','Low','Trend']].tail(15))
    print ('\n' *2 )
    print (df1_summary[['Date','Stock Market Performance','Predection']].tail(15))

    # fig, ax1 = plt.subplots()
    # ax2 =  ax1.twinx()
    # df1['Close'][-150:].plot(x = 'Index', color='tab:blue', figsize=(16,6), label = 'Close Price USA ($)', fontsize = 12, ax = ax1)
    # df1['Trend'][-150:].plot(x = 'Index', color='tab:red', figsize=(16,6), label = 'Prediction Trend', fontsize = 12, ax = ax2)
    #
    # plt.xlim([len(df1)-120, len(df1)])
    # ax1.set_ylabel('Close Price USD ($)', fontsize = 18)
    # ax2.set_ylabel('Prediction Trend', fontsize = 18)
    #
    # ax2.grid(color='tab:brown')
    # ax1.set_title('Prediction Trend ' + stock.upper(), fontsize = 16)
    # ax1.legend(loc=2, fontsize = 16)
    # ax2.legend(loc=4,fontsize = 16)
    # # plt.show
    # plt.savefig(downloadPath + '\\' + stock.upper() + '\\Prediction Trend ' +stock.upper()+ '_' + today.strftime("%m%d%Y") +'.png')
    # plt.close()

#    prediction = result.predict(x_test)
    now_up_down  = result.predict([1.0, df1.iloc[-1, 10], High_Low, df1.iloc[-1, 26] ,df1.iloc[-1, 22], df1.iloc[-1, 7]])
    print ("\n=========> Current trend = %.4f,  " %now_up_down, end=' ')
    print ("[ %s ] will go up! <=========" %stock.upper()) if now_up_down > cutoff else print ("[ %s ] will go down! <=========" %stock.upper())

    print ("\n ============> %s Days over %s Days Moving Average Indicator \n ============> %.4f....%.4f....%.4f....%.4f....%.4f....<=============" %(short_moving_average_span, long_moving_average_span, df1.iloc[-5,16], df1.iloc[-4,16], df1.iloc[-3,16], df1.iloc[-2,16],df1.iloc[-1,16]))
    if df1.iloc[-1,16] * df1.iloc[-2,16] < 0:
        print ("\n ============> Warning, It Is the Time to Sell [ %s ] <=========" %stock.upper()) if df1.iloc[-1,16] < 0 else print ("\n ============> It Is the Time to Buy [ %s ] ! <=========" %stock.upper())
    else:
        print ("\n ============> No Trading Waring at this time! <=============")
        
    print('\n' * 3)
    return

if __name__ == "__main__":
#    global cutoff
    print ("\nCutoff is set as %f" %cutoff)
    stocks = read_in_line().stock_lst

    if stocks != None:
        sys.stdout = Logger()
        logging.log(logging.INFO, "In Line Variable")
        for stock in stocks:
            # logging.log(logging.INFO, "stock = %s" %stock)
            main()

    else:
        logging.log(logging.INFO, "Batch Process")
        sys.stdout = Logger()
        stock_fund_names =  [line for line in open("STOCK.txt", "r")]
        for stock_fund_name in stock_fund_names:
            if len(stock_fund_name) < 2 or "IGNOR" in stock_fund_name :
                # logging.log(logging.INFO, "stock_fund_name = %s" %stock_fund_name)
                continue
            logging.log(logging.INFO, "stock_fund_name = %s" %stock_fund_name)
            stock = re.search(('\(\w+\)'), stock_fund_name)
            stock = stock.group().rstrip().rstrip(')').lstrip('(')
            main()