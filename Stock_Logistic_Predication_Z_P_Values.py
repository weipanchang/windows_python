#!/usr/bin/env python
# coding: utf-8
import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.api as sm
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date

from cachetools import cached

@cached(cache = {})
def main():
#    stock = input("Enter the stock symbol:  ")

    short_moving_average_span = 20
    long_moving_average_span = 50
    cutoff=0.50
    invest = 100
    years_of_data_to_process = 25
    
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    start_year =  int(year) - years_of_data_to_process
    start = datetime.datetime(start_year, 1, 1)

    with open("STOCK.txt","r") as stock_input_file:
        stock_fund_names = stock_input_file.readlines()
    print(stock_fund_names)

    for stock in stock_fund_names:
        print("\n\n[************************************************]")
        print ("      Stock Ticket = %s" %stock, end=' ')
        data =  yf.download(stock, start=start)

#        print (data)
        df = data["Close"].pct_change() * 100
        
        df = df.rename("Today_Change_%")
        df = df.reset_index()
        
        df1 = pd.merge(data,df, on="Date")
        
        df1.insert(7,'Volume_Lag', None)
        df1['Volume_Lag'] = df1.Volume.shift(1).values/1000000000
        df1.Volume = df1.Volume/1000000000
        
        df1["Trend"] =  (df1["Close"] - df1["Low"])/ ((df1["High"] - df1["Low"]))
        
        df1["Trend_Lag"] = df1["Trend"].shift(1)
        
        df1['Close-Open'] =  df1['Close'] - df1['Open']
        df1['Close-Open_Lag'] = df1['Close-Open'].shift(1)
        
        df1['High-Low'] =  df1['High'] - df1['Low']
        df1['High-Low_Lag'] = df1['High-Low'].shift(1)
        
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
        
        X = df1[['const','Trend_Lag','Short_MV_Avg_Span-Long_MV_Avg_Span_Lag','Close-Open_Lag','High-Low_Lag','Volume_Lag']]
        y = df1["Up_Down"].values
        
        model = sm.Logit(y,X)
        result =  model.fit()
        
        #result.summary()
        prediction = result.predict(X)
        
        df1['Prediction_Caculated'] = pd.array(prediction)
        df1['Prediction_indicator'] = pd.array([1 if i > cutoff else 0 for i in prediction])
        
        y = df1["Up_Down"].values
        
        def confusion_matrix(act,pred):
            predtrans = ['Up' if i > cutoff else 'Down' for i in pred]
            actuals = ['Up' if i > 0 else 'Down' for i in act]
            confusion_matrix = pd.crosstab(pd.Series(actuals),
                                           pd.Series(predtrans),
                                           rownames = ["Actual"],
                                           colnames = ["Predict"]
                                          )
            return confusion_matrix
        
        confusion_matrix(y,prediction)
        
        # z = confusion_matrix(y,prediction)
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
        
        #Simulate Investment transaction buy on opening when predict UP and sell daily average when predict DOWN
        
        def buy_sell(open_price, sell_price,prediction, money, share):
            if prediction == 1 and money != 0:
                share =  money / open_price
                money = 0
            elif prediction == 0 and share != 0:
                money = share * sell_price
                share = 0
            else: pass
            return [money, share]
        money = invest
        share = 0
        for i in range(len(df1)):
            [money, share] = buy_sell(df1.iloc[i,2],(df1.iloc[i,3]+df1.iloc[i,4])/2,df1.iloc[i,22], money, share)
            df1.iloc[i,23] = share
            df1.iloc[i,24] = money
        
        #print("\nIf ${:,.2f} was invested in [ {} ], and Just Hold and Not Trade for {:,} years, the ROI = ${:,.2f}".format( invest, stock.upper(), diff_years, invest/data.iloc[0, 0] * data.iloc[-1,0]))
        
        #print ("\nIf ${:,.2f} was invested {:2d} years ago, buy and sell according this script\'s recommandation, the ROI = ${:,.2f}".format(invest, diff_years, (money + (share * df1.iloc[-1,6]))))
        
        # df1_summary=df1[['Date', 'Up_Down','Prediction_indicator']].copy()
        # df1_summary['Stock Market Performance'] = df1_summary['Up_Down'].apply(lambda x: 'Up' if x > 0 else 'Down')
        # df1_summary['Scribe Predection'] = df1_summary['Prediction_indicator'].apply(lambda x: 'Up' if x > 0 else 'Down')
        # print (df1_summary[['Date','Stock Market Performance','Scribe Predection']].tail(15))
        
        # print ("\nToday [ %s ] actually went up," %stock.upper(), end = ' ') if (df1.iloc[-1,16] == 1) else print ("\nToday [ %s ] actually went down," %stock.upper(), end = " ")
        # print ("--- base on yesterday\'s data, ", end = '')
        # print ("We Predication [ %s ] should be going up." %stock.upper()) if (df1.iloc[-1,22] == 1) else print ("We Predicae [ %s ] should be going down." %stock.upper())
        # print ("\n=========> Actual and Predication MATCH <=========") if (df1.iloc[-1,16] == df1.iloc[-1,22]) else print("\n=========> Actual and Predication DO NOT match <=========")
        
        x_tran= df1[df1.Date.dt.year < 2021][['const','Trend_Lag','Short_MV_Avg_Span-Long_MV_Avg_Span_Lag','Close-Open_Lag','High-Low_Lag','Volume_Lag']]
        y_train=df1[df1.Date.dt.year < 2021]["Up_Down"]
        x_test= df1[df1.Date.dt.year >= 2021][['const','Trend_Lag','Short_MV_Avg_Span-Long_MV_Avg_Span_Lag','Close-Open_Lag','High-Low_Lag','Volume_Lag']]
        y_test= df1[df1.Date.dt.year >= 2021]["Up_Down"]
        # print("\n" *3)
        model = sm.Logit(y_train,x_tran)
        result=model.fit()
        
#        print (result.summary())
        summary_list=result.summary().as_csv().split(",")
        print("\nz-value = %s,   p-value = %s" %(summary_list[37], summary_list[38]))
        
        prediction = result.predict(x_test)
        confusion_matrix(y_test, prediction)
        
        # z = confusion_matrix(y_test,prediction)
        # 
        # try:
        #     print ("\n=========> Prediction Accuracy Rate: %.4f <=========\n"  %((z.loc['Down','Down'] + z.loc['Up','Up']) / len(x_test)))
        # except:
        #     print ("\n=========> Predication effectiveness is not avairable <=========\n" )
        # 
        prediction = result.predict(x_test)
        # now_up_down  = result.predict([1.0, df1.iloc[-1, 10], df1.iloc[-1, 19], df1.iloc[-1, 12], df1.iloc[-1, 14], df1.iloc[-1, 7]])
        # print ("\n=========> Current trend = %.4f,  " %now_up_down, end=' ')
        # print ("[ %s ] will go up! <=========" %stock.upper()) if now_up_down > cutoff else print ("[ %s ] will go down! <=========" %stock.upper()) 
        # 
        # print ("\n ============> %s Days over %s Days Moving Average Indicator<=============" %(short_moving_average_span, long_moving_average_span))
        # if df1.iloc[-1,19] * df1.iloc[-2,19] < 0:
        #     print ("\n ============> Warning, It Is the Time to Sell [ %s ]! <=========" %stock.upper()) if df1.iloc[-1,19] < 0 else print ("\n ============> It Is the Time to Buy [ %s ] ! <=========" %stock.upper())
        # else:
        #     print ("\n ============> No Trading Waring at this time! <=============")
        # 
        #df1.to_csv('fb.csv', index = False)
        
if __name__ == "__main__":
    main()

