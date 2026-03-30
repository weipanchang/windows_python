#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# As a Python developer, develope a python script
#  read the file , "C:\Users\William Chang\Downloads\Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.pdf" line by line.
#  start the line  containing  "Overview Zen Rating Price Value Growth", skip one line. Stop at the line 'How to Use a Stock Screener to Find Undervalued Stocks', printout
# Skip the last line, split element each line to a list
# In the element in the list  Remove the string "Strong Buy"  , remove the string "Buy". remove the string "Unlock", remove the last string, 
# copy the first element to key_list, copy the second element from the end  remove "$",   if the "k" in the element, remove "k", conver to float, multiple 1000, convert to string,  copy to value_list
# zap key_list, value_list to dictionary data_list, print data_list
#
# read
# C:\Users\William Chang\Documents\Python Scripts\STOCK.txt to line_list
# if the line start with "IGNOR"skip the line 
# copy  the string in the parentheses of each element in line_list to a list key_list
# copy the string from begining to the ninth character from the and to a list value1_list
# copy the string in the  square brackets of each element in line_list to a list value2_list
# create a dictionary type variable stock_Dictionary
# copy element  from value1_list, "stock", element from value2_list to value_list
#  zap key_list, value_list to stock_Dictionary
# print stock_Dictionary


from pathlib import Path
import re
import csv
import sys
from typing import List, Optional
import os
import pandas as pd
import time
import datetime
from datetime import date
import logging
import pdfplumber

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen\\"
downloadPath = os.path.expanduser( '~' ) + '\\Downloads\\'
WallStreetZen_data_file_name = "Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen"
stock_txt_path = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\" + "STOCK.txt"
WallStreetZen_pdf_file = WallStreetZen_data_file_name + ".pdf"
WallStreetZen_data_file = WallStreetZen_data_file_name + ".txt"
source = downloadPath + WallStreetZen_pdf_file
pdf_path = source
text_path = stock_txt_path

# Set logging configuration
logging.basicConfig(level=logging.CRITICAL, format="%(levelname)s: %(message)s")

def build_data_list(pdf_path):
    key_list = []
    value_list = []
    with pdfplumber.open(pdf_path) as pdf:
        all_lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_lines.extend(text.split('\n'))

        start_extracting = False
        captured_lines = []

        # Iterating through lines with logic to skip/stop
        for i, line in enumerate(all_lines):
            if "Overview Zen Rating Price Value Growth" in line:
                start_extracting = True
                continue # This skips the current line and effectively the "one line" after if logic permits

            if 'How to Use a Stock Screener to Find Undervalued Stocks' in line:
                break

            if start_extracting:
                captured_lines.append(line)

        processed_lines = captured_lines[1:-1]

        for line in processed_lines:
            #print(f"Processing line: {line}")
            elements = line.split()

            # Clean elements: Remove "Strong Buy", "Buy", "Unlock"
            clean_elements = [e for e in elements if e not in ["Strong", "Buy", "Unlock"]]
            # Remove the last string in the list
            if clean_elements:
                clean_elements.pop()

            if len(clean_elements) >= 2:
                # 1. Copy first element to key_list
                key_list.append(clean_elements[0])

                # 2. Process second element from the end
                val_raw = clean_elements[-2].replace("$", "")
                if 'k' in val_raw.lower():
                    val_num = float(val_raw.lower().replace('k', '')) * 1000
                else:
                    try:
                        val_num = float(val_raw)
                    except ValueError:
                        val_num = 0.0

                value_list.append(str(val_num))

    data_list = dict(zip(key_list, value_list))

    return data_list

def build_stock_dictionary(text_path):
    stock_key_list = []
    stock_value_list = []

    with open(text_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("IGNOR"):
                continue
            parens = re.search(r'\((.*?)\)', line)

            k = parens.group(1) if parens else "Unknown"

            stock_key_list.append(k)

            # Extract string from beginning to 9th character from the end
            # (Calculation: line[:-9])
            v1 = line[:-9].strip()

            # Extract string in square brackets: [VALUE]
            brackets = re.search(r'\[(.*?)\]', line)
            v2 = brackets.group(1) if brackets else ""

            # Combine: [element from v1, "stock", element from v2]
            stock_value_list.append([v1, "stock", v2])

    stock_Dictionary = dict(zip(stock_key_list, stock_value_list))

    return stock_Dictionary

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
    # home = os.path.expanduser('~')
    # pdf_path = os.path.join(home, "Downloads", FILENAME)
    if not os.path.isfile(pdf_path):
        print(f"PDF not found at: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    data_list = build_data_list(pdf_path)

    # Build stock dictionary and lists
    stock_Dictionary = build_stock_dictionary(text_path)

    try:
        shutil.rmtree(dataPath)
    except:
         pass
    time.sleep(2)
    try:
        os.mkdir(dataPath)
    except:
        pass

    sys.stdout = Logger()

    for stock in stock_Dictionary.keys():
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        target = data_list[stock]
        print ("\n1y Target Est = %s\n" % (str(target)))

if __name__ == "__main__":
    main()
