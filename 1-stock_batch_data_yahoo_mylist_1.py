#!/usr/bin/env python
"""
Firefox version: 73.0 (64-bit)
"""
#import xml.etree.ElementTree as ET
#import urllib2
import requests, urllib3, sys
#import requests, sys
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from path import Path
import os
import holidays
import shutil
#from yahoo_fin import stock_info as si
import yahoo_fin.stock_info as si
import yfinance as yf
import pandas as pd
from openpyxl import load_workbook, Workbook

# from bs4 import BeautifulSoup
# import unittest

import time
import datetime
from datetime import date
# import sys
# from bs4 import BeautifulSoup as bs
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\data"
Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
eXCEL_File = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Watch_List.xlsx"
        
#short_cut_url = "https://finance.yahoo.com/quote/AVGO/history?period1=1249516800&period2=1626307200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
stock = ""
#home_dir = os.path.expanduser( '~' )

class Logger(object):

    def __init__(self):
#        global downloadPath
        global stock
        today = date.today()
        #d1 = today.strftime("%m%d%Y")
        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report__From_Yahoo_"+ today.strftime("%m%d%Y") + ".txt" , "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

class get_data():

    #def __init__(self, stock_name, startDate, endDate, downloadPath):
    sys.stdout = Logger()
    def __init__(self, stock_or_fund):
#        global downloadPath
        global stock
#        stock_name = stock
        print ("")
#        print ("Processing " + self.stock_name.upper() +" stock data")
        self.stock_or_fund = stock_or_fund
        self.delay = 0
        self.currentDateTime = datetime.datetime.now()
        self.date = self.currentDateTime.date()

        self.ts = datetime.datetime.strptime(str(self.date),"%Y-%m-%d")
#        tuple = element.timetuple()
        self.timestamp = str(int(time.mktime(self.ts.timetuple())))

        
        weekno = datetime.datetime.today().weekday()
        north_america = holidays.US()

        Day_of_today = self.date.strftime("%m-%d-%Y")

        if weekno < 5 and (Day_of_today not in north_america):
#            print("Saving current stock price.")
            current_time = datetime.datetime.now()
            open_time = current_time.replace(hour=6, minute=20, second=0, microsecond=0)

        
    def lines_that_contain(string, fp):
        return [line for line in fp if string in line]
    
    def stock_summary():
        today = date.today()

        quote_table = si.get_quote_table(stock)
        print("Current Price:\t%s\n" % quote_table["Quote Price"])
        print("Previous Close:\t%s\n" % quote_table["Previous Close"])
        print("Open:\t%s\n" % quote_table["Open"])
        Low, High  = quote_table["Day's Range"].split(' - ')[0], quote_table["Day's Range"].split(' - ')[1]
        print ("LOW = %s, HIGH = %s\n" %(Low, High))
        print("Beta (5Y Monthly):\t%s\n" % quote_table["Beta (5Y Monthly)"])
        print("=====> 1y Target Est\t%s\n" % quote_table["1y Target Est"])
        print("EPS ( > 1 is better ):\t%s\n" % quote_table["EPS (TTM)"])
        try:
            print("Earning Date:\t%s\n" % quote_table["'Earnings Date': "])
        except:
            pass
        print("PE_Ratio ( Smaller is better ):\t%s\n" % quote_table["PE Ratio (TTM)"])
        print("Volume over Average:\t{:.{}f}".format( (quote_table["Volume"])/quote_table["Avg. Volume"], 2 ))

        

                
    def get_Current_Stock_Price(self, stock, Stock_Fund):
        if Stock_Fund != 'Fund':
            return(float(si.get_live_price(stock)))
        else:
            ticket = yf.Ticker(stock)
            return ticket.info['regularMarketPrice']


def main():
#    global downloadPath
    global stock
    try:
        shutil.rmtree(downloadPath)
    except:
         pass
    time.sleep(2)
    try:
        os.mkdir(downloadPath)
    except:
        pass

    now_time = datetime.datetime.now().time()
    print("\nTime: ", now_time, "\n")


    def fetch_Stock_Name(stock_Dictionary):
        
        __slots__ = stock_Dictionary
        stock_fund_names =  [line for line in open("STOCK.txt", "r")]
        for stock_fund_name in stock_fund_names:
            if len(stock_fund_name) < 2 or "IGNOR" in stock_fund_name :
                continue

            stock = re.search(r'(\(\^\w+\))', stock_fund_name)
            if stock is None:
                stock = re.search('\(\w+\)', stock_fund_name)
                msft_ticket = re.search('\[\w+\]', stock_fund_name)

            is_stock =  re.search("ETF|Fund",stock_fund_name)
#            print is_stock
            if is_stock:
                if 'ETF' in stock_fund_name:
                    stock_or_fund =  'ETF'
                else:
                    stock_or_fund = 'Fund'
            else:
                stock_or_fund ='STOCK'
            # print(stock_or_fund)
            stock = stock.group().rstrip().rstrip(')').lstrip('(')
            msft_ticket = msft_ticket.group().rstrip().rstrip(']').lstrip('[')
            stock_Dictionary[stock] = [stock_fund_name.rstrip()[:-9]]
            stock_Dictionary[stock].append(stock_or_fund)
            stock_Dictionary[stock].append(msft_ticket)

    # def option1():
    #     get_history_data.get_historical_data()
    # 
    # def option2():
    #     get_history_data.get_Summary_data()
    # 
    # def option3():
    #     get_history_data.get_historical_data()
    #     get_history_data.get_Summary_data()

    def option4(): 
#        get_history_data = get_data('STOCK')
        get_data.stock_summary()
        

    sys.stdout = Logger()
    fetch_Stock_Name(stock_Dictionary:={})

    for stock in stock_Dictionary.keys():
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
 #       get_data(stock_Dictionary[stock][1])
        
        option4()

if __name__ == "__main__":
    main()
