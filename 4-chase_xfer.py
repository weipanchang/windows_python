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


dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Chase\\"
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
cHase_file_name = "Markets - Watchlists - chase.com"
cHase_pdf_file = cHase_file_name + ".pdf"
cHase_data_file = cHase_file_name + ".txt"
source = downloadPath + cHase_data_file

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
        self.log = open(dataPath +"\\Summary_Report_From_Chase_"+ today.strftime("%m%d%Y") + ".txt" , "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
     
def main():
    pdf_to_text(downloadPath + cHase_pdf_file, downloadPath + cHase_data_file)
    
    def extract_price(s, sub1):
        idx1 = s.index(sub1)
        return(s[(idx1 + 1):])
    
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

    sys.stdout = Logger()

    for stock in stock_Dictionary.keys():

        print ("")
        with open(dataPath + cHase_data_file) as Chase:
            while True:
                line_from_Chase =  Chase.readline()
                if "("+stock+")" in line_from_Chase:
                    print("\n")
                    print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
                    print ("Processing " + stock_Dictionary[stock][0] +" data")
                    print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")

                    while True:
                        line_from_Chase = Chase.readline()
                        if "Trade" in line_from_Chase:
                            line_from_Chase = Chase.readline()
                            line_from_Chase = line_from_Chase.replace("Â","")
                            print ("\nUpside/downside %s\n" % (line_from_Chase))
                        if "Morgan price target" in line_from_Chase:
                            line_from_Chase = Chase.readline()
                            line_from_Chase = extract_price(line_from_Chase, '$').replace(",","")
                            
                            try: 
                                float(line_from_Chase) 
                                pass 
                            except ValueError: 
                                line_from_Chase = "0.00"
                    
                            print ("\n1y Target Est = %s\n" % (line_from_Chase))

                            break
                    break


if __name__ == '__main__':
    
    main()