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
from tabula import read_pdf
from tabula import convert_into

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stock_Analysis\\"                                     
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
Stock_Analysis_data_file_name = "Stock Watchlist & Portfolio Tracker"
Stock_Analysis_pdf_file = Stock_Analysis_data_file_name + ".pdf"
Stock_Analysis_data_file = Stock_Analysis_data_file_name + ".txt"
source = downloadPath + Stock_Analysis_data_file

def pdf_table_to_text(pdf_file_name, text_file_name):
    # # extract all the tables in the PDF file
#    abc = camelot.read_pdf(pdf_file_name)   #address of file location
    df = read_pdf(pdf_file_name, pages='all') 
    # print the first table as Pandas DataFrame
    convert_into(pdf_file_name, text_file_name, output_format="csv", pages='all')

class Logger(object):

    def __init__(self):
        global dataPath
        today = date.today()

        self.terminal = sys.stdout
        self.log = open(dataPath +"\\Summary_Report_From_Stock_Analysis_"+ today.strftime("%m%d%Y") + ".txt" , "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
     
def main():
    pdf_table_to_text(downloadPath + Stock_Analysis_pdf_file, downloadPath + Stock_Analysis_data_file)
    
    def extract_data(data_list):
        key_list = []
        value_list = []
        Stock_Analysis_readlines =  [stock_line for stock_line in open(dataPath + Stock_Analysis_data_file, "r")]
        for stock_line in Stock_Analysis_readlines[5:]:
            key_list.append((stock_line.split(",")[0]).split()[0])
            value_list.append(stock_line.split(",")[2:])
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

    shutil.move(source, dataPath)            
    fetch_Stock_Name(stock_Dictionary:={})
    data_list = extract_data(data_list:={})
    sys.stdout = Logger()
    for stock in stock_Dictionary.keys():
        
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        
        print ("\n1y Target Est = %s\n" % (data_list[stock][0].split()[2]))
        print ("\nPrice Target Upside Percent = %s\n" % (data_list[stock][1]))
 
if __name__ == '__main__':
    
    main()