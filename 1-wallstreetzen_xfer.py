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

wallStreetZen_data_file = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen\\WallStreetZen.txt"
Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen"

class Logger(object):

    def __init__(self):
        global downloadPath
        today = date.today()

        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report_From_WallStreetZen_"+ today.strftime("%m%d%Y") + ".txt" , "w")

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
    
    source = "C:\\Users\\William Chang\\Downloads\\WallStreetZen.txt"

    shutil.move(source, downloadPath)
    
    fetch_Stock_Name(stock_Dictionary:={})

#    print(stock_Dictionary)
    sys.stdout = Logger()
#    os.system("pause")    

    with open(wallStreetZen_data_file) as WallStreetZen:
#            reading_line_list = list() 
        reading_line_list = WallStreetZen.readlines()
        for i in range(len(reading_line_list)):
            if len(reading_line_list[i]) >1:
                reading_line_list[i] = reading_line_list[i][:-1]
            if  reading_line_list[i] == "GOOGL":
                reading_line_list[i] = "GOOG"
#        print (reading_line_list)               


    for stock in stock_Dictionary.keys():
#            os.system("PAUSE")
   
            # while True:
            #     read_in = WallStreetZen.readline()
            #     if read_in != None:
            #         reading_line_list.append(read_in)
            #     if len(reading_line_list) > 3:
            #         del  reading_line_list[0]
            #     print(reading_line_list)
        for i in range(len(reading_line_list)):
            
            if stock == reading_line_list[i]:
                    print("\n")
                    print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
                    print ("Processing " + stock_Dictionary[stock][0] +" data")
                    print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
                    # for i in range(8):
                    #     line_from_WallStreetZen = WallStreetZen.readline()
                    target_price = reading_line_list[i-2].split()[-3].replace("$","").replace(",","")
                    # while True:
                    #     line_from_WallStreetZen = WallStreetZen.readline()
                    #     if "Morgan price target" in line_from_WallStreetZen:
                    #         line_from_WallStreetZen = WallStreetZen.readline().replace("$","").replace(",","")
                    try: 
                        float(target_price) 
                        pass 
                    except ValueError: 
                        target_price = "0.00"
            
                    print ("\n1y Target Est = %s\n" % (target_price))
                            
                        # WallStreetZen.readline()
                        # WallStreetZen.readline()
                        # line_from_WallStreetZen = WallStreetZen.readline()
                        # print ("\nUpside/downside %s\n" % (line_from_WallStreetZen))
                            # break


if __name__ == '__main__':
    
    main()