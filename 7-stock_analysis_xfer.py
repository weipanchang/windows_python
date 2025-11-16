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
sTock_Analysis_data_file_name = "Stock Watchlist & Portfolio Tracker"
sTock_Analysis_pdf_file = sTock_Analysis_data_file_name + ".pdf"
sTock_Analysis_data_file = sTock_Analysis_data_file_name + ".txt"
source = downloadPath + sTock_Analysis_data_file

def pdf_table_to_text(pdf_file_name, text_file_name):
    # # extract all the tables in the PDF file
#    abc = camelot.read_pdf(pdf_file_name)   #address of file location
    df = read_pdf(pdf_file_name, pages='all') 
    # print the first table as Pandas DataFrame
    convert_into(pdf_file_name, text_file_name, output_format="csv", pages=1)

class Logger(object):

    def __init__(self):
        global downloadPath
        today = date.today()

        self.terminal = sys.stdout
        self.log = open(dataPath +"\\Summary_Report_From_Stock_Analysis_"+ today.strftime("%m%d%Y") + ".txt" , "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(str(message))

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
     
def main():
    time.sleep(5)
    pdf_table_to_text(downloadPath + sTock_Analysis_pdf_file, downloadPath + sTock_Analysis_data_file)
    def extract_data(data_list):
        line_from_Stock_Analysis =""
        with open(dataPath+sTock_Analysis_data_file) as Stock_Analysis:
             Stock_Analysis.readline()
             # Stock_Analysis.readline()
             # Stock_Analysis.readline()
             # Stock_Analysis.readline()

             while True:
    #                line_from_Stock_Analysis = Stock_Analysis.readline()
    #                if "Watchlist Averages" not in line_from_Stock_Analysis:
                line_from_Stock_Analysis = Stock_Analysis.readline()
    #            for line_from_Stock_Analysis in Stock_Analysis.readline():
                if not line_from_Stock_Analysis:
                    break
                elements = line_from_Stock_Analysis.split(",")
                print(elements)
                element_data = elements
                # element_data = elements[2].split(",")
                # print(element_data)
                 #    if len(elements)  > 5:
                 # if float(element_data[0]) == 0  or str(element_data[0])[0]== "+" or str(element_data[0])[0]== "-":
                 #     data_list[elements[0]] = element_data[1]
                 # else:
                 #     data_list[elements[0]] = element_data[0]
                data_list[elements[0].split()[0]] = element_data[3]
#                data_list[elements[0] = element_data[4]   
        return(data_list)
    
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

    shutil.move(source, dataPath)            
    fetch_Stock_Name(stock_Dictionary:={})

#    print(stock_Dictionary)
    sys.stdout = Logger()
#    os.system("pause")    

    extract_data(data_list:={})
    for stock in stock_Dictionary.keys():
        
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        
        print ("\n1y Target Est = %s\n" % (data_list[stock]))
#        print ("\nPrice Target Upside Percent = %s%%\n" % (data_list[stock][1]))
 
if __name__ == '__main__':
    
    main()