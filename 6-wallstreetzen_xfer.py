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

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen\\"                                     
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
WallStreetZen_data_file_name = "Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen"
WallStreetZen_pdf_file = WallStreetZen_data_file_name + ".txt"
WallStreetZen_data_file = WallStreetZen_data_file_name + ".txt"
source = downloadPath + WallStreetZen_data_file

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
    #pdf_table_to_text(downloadPath + WallStreetZen_pdf_file, downloadPath + WallStreetZen_data_file)
    
    def extract_data(data_list):
        key_list = []
        value_list = []
        WallStreetZen_readlines =  [stock_line for stock_line in open(dataPath + WallStreetZen_data_file, "r")]
        
        for stock_line in WallStreetZen_readlines[2:]:
            if len(stock_line) > 2:
                key_list.append(stock_line.split()[0])
                if "Strong" in stock_line:
                    value_list.append(stock_line.split()[-9])
                else:
                    value_list.append(stock_line.split()[-8])
        
        data_list = { k:v for (k,v) in zip(key_list, value_list)}
        print(data_list)
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
    #print (data_list)

    for stock in stock_Dictionary.keys():

        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")

        print ("\n1y Target Est = %s\n" % (str(float(data_list[stock].replace("$","").replace(",","")))))
        # if target_price[-1] == 'k':
        #     print ("\n1y Target Est = %s\n" % (str(float(target_price.replace("k", "")) * 1000)))  
        # else:
        #     print ("\n1y Target Est = %s\n" % (target_price))                
        
        # if data_list[stock].split()[3][0] == '"':
        #     print ("\nPrice Target Upside Percent = %s\n" % (data_list[stock].split()[6]))
        # else:
        #     print ("\nPrice Target Upside Percent = %s\n" % (data_list[stock].split()[5]))
 
if __name__ == '__main__':
    
    main()