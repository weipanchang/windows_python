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
    convert_into(pdf_file_name, text_file_name, output_format="csv", pages='all')

class Logger(object):

    def __init__(self):
        global downloadPath
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
    time.sleep(5)
    pdf_table_to_text(downloadPath + sTock_Analysis_pdf_file, downloadPath + sTock_Analysis_data_file)
#    def extract_data(data_list):
        #line_from_Stock_Analysis =""
    with open(dataPath+sTock_Analysis_data_file, encoding='utf8') as Stock_Analysis:
        # try:
        #     line_from_Stock_Analysis = Stock_Analysis.readline()
        # except:
        #     pass
        i = 0
        while i <40:
            lines_from_Stock_Analysis = Stock_Analysis.readline()
    
    
            print(lines_from_Stock_Analysis)
            i = i + 1
            if "Next Year" in lines_from_Stock_Analysis:
                break








            # os.system("pause")
#                    continue
            # os.system("pause")
            
 
if __name__ == '__main__':
    
    main()