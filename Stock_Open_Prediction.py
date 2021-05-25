#!/usr/bin/env python
# coding: utf-8
import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.api as sm
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date

def main():
    stock = input("Enter the stock symbol:  ")

    years_of_data_to_process = 17
    
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    start_year =  int(year) - years_of_data_to_process
    start = datetime.datetime(start_year, 1, 1)
    
    print('\n'*3)
    data =  yf.download(stock, start=start)
    data.drop(data.loc[data['Open']==0].index, inplace=True)
    data.drop(data.loc[data['Volume']==0].index, inplace=True)
    
    print('\n'*1,data)
    
    df = data["Close"].pct_change() * 100

    df = df.rename("Today_Change_%")
    df = df.reset_index()
    #print(df)
    
    df1 = pd.merge(data,df, on="Date")
    
    df1['Volume_Lag'] = data.Volume.shift(1).values/1000000000
    df1['Volume'] = df1['Volume']/1000000000
    #df1.rename(columns={'Volume_Lag': 'Volume'}, inplace=True)
    
    df1["Up_Down"] = [1 if (i > 0) else 0 for i in df1["Today_Change_%"]]
    
    #print(df1)
    
    df1["Trend"] =  (df1["Close"] - df1["Low"])/ ((df1["High"] - df1["Low"]))
    
    df1["Trend_Lag1"] = df1["Trend"].shift(1)
    
    df1 = sm.add_constant(df1)
    
    df1.dropna(inplace= True)
    #print(df1)
    
    X = df1[['const','Trend_Lag1','Volume_Lag']]
    
    y = df1["Up_Down"].values
    
    cutoff=0.50
    
    model = sm.Logit(y,X)
    
    result =  model.fit()
    
    result.summary()
    
    prediction = result.predict(X)
    
    
    df1['Prediction_Caculated'] = pd.array(prediction)
    df1['Prediction_indicator'] = pd.array([1 if i > cutoff else 0 for i in prediction])
    #print(df1.tail(10))
    
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
#    print(confusion_matrix(y,prediction))
    z = confusion_matrix(y,prediction)

    # try:
    #      print ("\nPredication effectiveness: %.4f \n"  %((z.iloc[0,0] + z.iloc[1,1]) / len(df1)))
    # except:
    #      print ("\nPredication effectiveness is not avairable \n" )
    
    x_tran= df1[df1.Date.dt.year < 2020][['const','Trend_Lag1','Volume_Lag']]
    y_train=df1[df1.Date.dt.year < 2020]["Up_Down"]
    x_test= df1[df1.Date.dt.year >= 2020][['const','Trend_Lag1','Volume_Lag']]
    y_test= df1[df1.Date.dt.year >= 2020]["Up_Down"]
    
    result=model.fit()
    
    confusion_matrix(y_test, prediction)
    
    #len(x_test)
   
    z = confusion_matrix(y_test,prediction)
    
    try:
        print ("\n=========> Predication effectiveness: %.4f <=========\n"  %((z.iloc[0,0]+ z.iloc[1,1]) / (z.iloc[0,0] + z.iloc[1,1] + z.iloc[0,1])))
    except:
        print ("\n=========> Predication effectiveness is not avairable <=========\n" )

    df1 = df1.assign(share=np.nan,money=np.nan)
    
    #Simulate Investment transaction buy on opening at 1 and sell average at 0
    diff_years = round((df1.iloc[-1,1] - df1.iloc[0,1])/np.timedelta64(1,'Y') + 0.5)
    def buy_sell(open_price, sell_price,prediction, money, share):
        if prediction == 1 and money != 0:
            share =  money / open_price
            money = 0
        elif prediction == 0 and share != 0:
            money = share * sell_price
            share = 0
        else: pass
        return [money, share]
    money = 1000000
    share = 0
    diff_years = round((df1.iloc[-1,1] - df1.iloc[0,1])/np.timedelta64(1,'Y'))    
  
    for i in range(len(df1)):
        [money, share] = buy_sell(df1.iloc[i,2],(df1.iloc[i,3]+df1.iloc[i,4])/2,df1.iloc[i,14], money, share)
        df1.iloc[i,15] = share
        df1.iloc[i,16] = money
        
    print("\nIf $1,000,000 was invested in [ {} ], and Just Hold and Not Trade  for {:,} years, the ROI = ${:,.2f} <=========".format( stock.upper(), diff_years, 1000000/data.iloc[0, 0] * data.iloc[-1,0]))
    print ("\nIf $1,000,000 was invested {:2d} years ago, buy and sell according this script\'s recommandation, the ROI = ${:,.2f} <=========".format(diff_years, (money + (share * df1.iloc[-1,6]))))
    print ('\n')
    print ('=' * 30)
    print ("Last 15 Day\'s Predication")
    print ('=' * 30)
    print ('\n')
    
    df1_summary=df1[['Date', 'Up_Down','Prediction_indicator']].copy()
    df1_summary['Stock Market Performance'] = df1_summary['Up_Down'].apply(lambda x: 'Up' if x > 0 else 'Down')
    df1_summary['Scribe Predection'] = df1_summary['Prediction_indicator'].apply(lambda x: 'Up' if x > 0 else 'Down')
    print (df1_summary[['Date','Stock Market Performance','Scribe Predection']].tail(15))
    print('\n')       
    
    print ("\nToday [ %s ] actually went up," %stock.upper(), end = ' ') if (df1.iloc[-1,10] == 1) else print ("\nToday [ %s ] actually went down," %stock.upper(), end = " ")
    print ("--- base on yesterday\'s data, ", end = '')
    print ("We Predication [ %s ] should be going up." %stock.upper()) if (df1.iloc[-1,14] == 1) else print ("We Predicae [ %s ] should be going down." %stock.upper())
    print ("\n=========> Actual and Predication MATCH <=========") if (df1.iloc[-1,14] == df1.iloc[-1,10]) else print("\n=========> Actual and Predication DO NOT match <=========")
       
    # Base on today's data to  predicate tomorrow trend
    prediction = result.predict(x_test)
    tomorrow_up_down = result.predict([1.0,df1.iloc[-1,11],df1.iloc[-1,7]])
    print ("\n=========> Current trend = %.4f,  " %tomorrow_up_down, end=' ')
    print ("[ %s ] will go up! <=========" %stock.upper()) if tomorrow_up_down > 0.5 else print ("[ %s ] will go down! <=========" %stock.upper()) 
    
    #df1.to_csv('fb.csv', index = False)

if __name__ == "__main__":
    main()
 
