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
from pprint import pprint 
import logging

cHase_data_file = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stanley\\Morgan Stanley Online.txt"
Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stanley"

class Logger(object):

    def __init__(self):
        global downloadPath
        today = date.today()

        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report_From_Stanley_"+ today.strftime("%m%d%Y") + ".txt" , "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
     
def main():
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
    source = "C:\\Users\\William Chang\\Downloads\\Morgan Stanley Online.txt"
#    destination = "D:\Pycharm projects\gfg\Test\A"
    shutil.move(source, downloadPath)        
    fetch_Stock_Name(stock_Dictionary:={})

#    pprint(stock_Dictionary)
    print('\n\n')
    sys.stdout = Logger()
    with open(cHase_data_file) as Stanley:
        Stanley_readlines = Stanley.readlines()
#   print (Stanley_readlines)
#    os.system("pause")
    for stock in stock_Dictionary.keys():
        for Stanley_readline in Stanley_readlines:
            if len(Stanley_readline) < 3:
                continue
#            print(Stanley_readline.split()[0])
            if Stanley_readline.split()[0].upper() in stock_Dictionary[stock][0].upper():
                print("\n")
                print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
                print ("Processing " + stock_Dictionary[stock][0] +" data")
                print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
#                print(Stanley_readline.split()[-1])
                target_price = Stanley_readline.split()[-1].replace("$","").replace(",","")
    
                try: 
                    float(target_price) 
                    pass 
                except ValueError: 
                    target_price = "0.00"
    
                print ("\n1y Target Est = %s\n" % (target_price))

if __name__ == '__main__':
    
    main()