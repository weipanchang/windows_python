#!/usr/bin/env python
import requests
import time
import datetime
from datetime import date
from datetime import timedelta
from path import Path
import os
import sys
import shutil
import re
import logging

sTock_Analysis_data_file = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stock_Analysis\\Stock Watchlist & Portfolio Tracker.txt"
Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stock_Analysis"

class Logger(object):

    def __init__(self):
        global downloadPath
        today = date.today()

        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report_From_Stock_Analysis_"+ today.strftime("%m%d%Y") + ".txt" , "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
     
def main():
    
    def extract_data(data_list):
        line_from_Stock_Analysis =""
        with open(sTock_Analysis_data_file) as Stock_Analysis:
            try:
                line_from_Stock_Analysis = Stock_Analysis.readline()
            except:
                pass
            while "Next Year" not in line_from_Stock_Analysis:

                line_from_Stock_Analysis = Stock_Analysis.readline()

                # print(line_from_Stock_Analysis)
                # os.system("pause")
#                    continue
            # os.system("pause")
            
            while True:
#                line_from_Stock_Analysis = Stock_Analysis.readline()
#                if "Watchlist Averages" not in line_from_Stock_Analysis:
                # try:
                line_from_Stock_Analysis = Stock_Analysis.readline()
                # except:
                #     pass
                if "Watchlist Averages" not in line_from_Stock_Analysis:
                    if len(line_from_Stock_Analysis)  != 0:
                        elements = line_from_Stock_Analysis.split()
                        if len(elements)  > 5:
#                            print(elements)
                            data_list[elements[0]] = [elements[3].replace(",", "")]
                            data_list[elements[0]].append(elements[4])
                else:
                    break
    
    def fetch_Stock_Name(stock_Dictionary):
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
    
            stock = stock.group().rstrip().rstrip(')').lstrip('(')
            msft_ticket = msft_ticket.group().rstrip().rstrip(']').lstrip('[')
            stock_Dictionary[stock] = [stock_fund_name.rstrip()[:-9]]
            
            stock_Dictionary[stock].append(stock_or_fund)
            stock_Dictionary[stock].append(msft_ticket)
            
    try:
        shutil.rmtree(downloadPath)
    except:
         pass
    time.sleep(2)
    try:
        os.mkdir(downloadPath)
    except:
        pass            
    source = "C:\\Users\\William Chang\\Downloads\\Stock Watchlist & Portfolio Tracker.txt"
#    destination = "D:\Pycharm projects\gfg\Test\A"
    shutil.move(source, downloadPath)            
    fetch_Stock_Name(stock_Dictionary:={})

 #  print(stock_Dictionary)
    sys.stdout = Logger()
#    os.system("pause")    

    extract_data(data_list:={})
#   print (data_list)
#    os.system("pause")
    for stock in stock_Dictionary.keys():
        
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        
        print ("\n1y Target Est = %s\n" % (data_list[stock][0]))
        print ("\nPrice Target Upside Percent = %s\n" % (data_list[stock][1]))
 
if __name__ == '__main__':
    
    main()