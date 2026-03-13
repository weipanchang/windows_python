#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read a CSV file, skip the first four lines, build a dict mapping Ticker -> Price Target,
and print the resulting variable `data_list`.

As a Python developer, develope a python script to read the file
"Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.tickers_price_targets.csv",
skip the first four line, create a dictionary type variable data_list,
the key is first element in each line,  the value is second element  in each line, print out the variable data_list


"""
import time
import datetime
from datetime import date
import shutil
import re
import logging
import csv
import os
import argparse
import sys
from pprint import pprint
from typing import Dict, Any

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen\\"                                     
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
WallStreetZen_data_file_name = "Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen"
WallStreetZen_csv_file = WallStreetZen_data_file_name + ".csv"
WallStreetZen_data_file = WallStreetZen_data_file_name + ".txt"
source = downloadPath + WallStreetZen_csv_file
#source = downloadPath + WallStreetZen_data_file

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
     


def build_data_list(path: str) -> Dict[str, str]:
    data_list: Dict[str, str] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        # Skip the first four lines (safe if file has fewer lines)
        for _ in range(4):
            if fh.readline() == "":
                break

        reader = csv.reader(fh)
        for row in reader:
            if not row:
                continue
            # Require at least two columns
            if len(row) < 2:
                continue
            key = row[0].strip()
            value = row[1].strip()
            if key == "":
                continue
            # If duplicate keys appear, the last occurrence will overwrite previous
            data_list[key] = value

    return data_list

def main():
    downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
    #PDF_PATH = Path(downloadPath + r"Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.pdf")
    parser = argparse.ArgumentParser(description="Build dict Ticker -> Price Target from CSV")
    parser = argparse.ArgumentParser(description="Map first CSV column to second column after skipping 4 lines")
    parser.add_argument(
        "csvfile",
        nargs="?",
        default=source,
        #default=downloadPath+"Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.tickers_price_targets.csv",
        help="Path to the CSV file"
    )
    args = parser.parse_args()

    data_list = build_data_list(args.csvfile)

    # Print the resulting dictionary variable
    #print("data_list =")
    #pprint(data_list, width=120)

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
    #data_list = extract_data(data_list:={})
    sys.stdout = Logger()
    
    for stock in stock_Dictionary.keys():

        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        target = data_list[stock].replace("$","").replace(",","")
        # if (data_list[stock])[-1] == 'k':
        #         target = str(float(target.replace("k", "")) * 1000)
        print ("\n1y Target Est = %s\n" % (str(target)))


if __name__ == "__main__":
    main()
