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
import pymupdf

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stanley\\"
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
sTanley_file_name = "Morgan Stanley Online"
sTanley_pdf_file = sTanley_file_name + ".pdf"
sTanley_data_file = sTanley_file_name + ".txt"
source = downloadPath + sTanley_data_file

def pdf_to_text(pdf_file_name, text_file_name):
    doc = pymupdf.open(pdf_file_name) # open a document
    out = open(text_file_name, "wb") # create a text output
    for page in doc: # iterate the document pages
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
        out.write(text) # write text of page
        out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    out.close()

class Logger(object):

    def __init__(self):
        global dataPath
        today = date.today()

        self.terminal = sys.stdout
        self.log = open(dataPath +"\\Summary_Report_From_Stanley_"+ today.strftime("%m%d%Y") + ".txt" , "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
     
def main():
    pdf_to_text(downloadPath + sTanley_pdf_file, downloadPath + sTanley_data_file)
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

    print('\n\n')
    sys.stdout = Logger()
    with open(dataPath + sTanley_data_file) as Stanley:
        Stanley_readlines = Stanley.readlines()

    for stock in stock_Dictionary.keys():
        for i in range(len(Stanley_readlines)):
            if Stanley_readlines[i][:-1] == stock:
                print("\n")
                print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
                print ("Processing " + stock_Dictionary[stock][0] +" data")
                print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
                target_price = (Stanley_readlines[i+1])
                target_price = target_price.replace("$","").replace(",","")
    
                try: 
                    float(target_price) 
                    pass 
                except ValueError: 
                    target_price = "0.00"
    
                print ("\n1y Target Est = %s\n" % (target_price))
                break
if __name__ == '__main__':
    
    main()