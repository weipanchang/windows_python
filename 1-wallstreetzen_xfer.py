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

# wallStreetZen_data_file = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen\\Best Stock Screener App In 2025 - #1 Top Free Stock Scanner _ WallStreetZen.txt"
# Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
# downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen"

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen\\"                                     
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
WallStreetZen_data_file_name = "Best Stock Screener App In 2025 - #1 Top Free Stock Scanner _ WallStreetZen"
#WallStreetZen_pdf_file = WallStreetZen_data_file_name + ".pdf"
WallStreetZen_data_file = WallStreetZen_data_file_name + ".txt"
source = downloadPath + WallStreetZen_data_file

class Logger(object):

    def __init__(self):
        global downloadPath
        today = date.today()

        self.terminal = sys.stdout
        self.log = open(dataPath +"\\Summary_Report_From_WallStreetZen_"+ today.strftime("%m%d%Y") + ".txt" , "w")

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
        key_list = []
        value_list = []
        WallStreetZen_readlines =  [stock_line for stock_line in open(dataPath + WallStreetZen_data_file, "r")]
#        print(WallStreetZen_readlines[2::2])
        for line in WallStreetZen_readlines[2::2]:
            stock_line= line
            if "Strong" in stock_line:
                stock_line = stock_line.replace("Strong","")
            key_list.append(stock_line.split()[0])
            value_list.append(stock_line.split()[1:])
        data_list = { k:v for (k,v) in zip(key_list, value_list)}
        return data_list
    
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
        shutil.rmtree(dataPath)
    except:
         pass
    time.sleep(2)
    try:
        os.mkdir(dataPath)
    except:
        pass
    
    #source = "C:\\Users\\William Chang\\Downloads\\Best Stock Screener App In 2025 - #1 Top Free Stock Scanner _ WallStreetZen.txt"

    shutil.move(source, dataPath)
    
    fetch_Stock_Name(stock_Dictionary:={})
    data_list = extract_data(data_list:={})
    data_list["GOOG"] = data_list.pop("GOOGL")
    sys.stdout = Logger()
#    os.system("pause")    

    for stock in stock_Dictionary.keys():

        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")

        target_price = data_list[stock][-4].replace("$","").replace(",","")

        try: 
            float(target_price) 
            pass 
        except ValueError: 
            target_price = "0.00"
    
        print ("\n1y Target Est = %s\n" % (target_price))                
        print ("\nPrice Target Upside Percent = %s\n" % (data_list[stock][-3]))


if __name__ == '__main__':
    
    main()