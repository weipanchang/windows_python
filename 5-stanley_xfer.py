#!/usr/bin/env python
import os
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
from PyPDF2 import PdfReader

"""
As a Python developer, develope a python script to read the file
os.path.expanduser( '~' ) + '\Downloads\\'+ \\Watchlist.pdf  by lines,  start from "Watchlist",
output  to list,
remove first two elements from the list,
remove last twenty four elements from the list,

copy last two strings of each element from the list to a new list,
from new list, split each element to a sublist
print new list
output the first element of the sublist from new list to key_list
remove "$" from the second element of the sublist in new list, and copy to value_list
print key_list
print value_list
zap key_list as key and value_list as value to a dictionary variable data_list
print data_list
"""
dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stanley\\"
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
sTanley_file_name = "Watchlist"
sTanley_pdf_file = sTanley_file_name + ".pdf"
# sTanley_data_file = sTanley_file_name + ".txt"
# source = downloadPath + sTanley_data_file
pdf_path = downloadPath+ sTanley_pdf_file

def read_pdf_lines(pdf_path: str) -> list:
    """Return all text lines extracted from the PDF in reading order."""
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError:
        print(f"File not found: {pdf_path}")
        return []
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return []

    lines = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            lines.extend(text.splitlines())
    return lines

def slice_from_keyword(lines: list, keyword: str = "Watchlist") -> list:
    """Return the slice of lines starting at the first line that contains keyword (case-insensitive)."""
    kw = keyword.lower()
    for i, line in enumerate(lines):
        if kw in line.lower():
            return lines[i:]
    return []

def safe_trim(lines: list, remove_first: int = 2, remove_last: int = 24) -> list:
    """Remove the first `remove_first` and last `remove_last` elements safely."""
    if not lines:
        return []
    if remove_first >= len(lines):
        return []
    trimmed = lines[remove_first:]
    if remove_last >= len(trimmed):
        return []
    if remove_last > 0:
        trimmed = trimmed[:-remove_last]
    return trimmed

def last_two_tokens_per_line(lines: list) -> tuple:
    """
    For each line, take the last two whitespace-separated tokens.
    Returns:
      new_list_strings: list of strings where each string is the last two tokens joined by a space
      new_list_sublists: list of lists where each inner list contains the tokens
    """
    new_list_strings = []
    new_list_sublists = []
    for line in lines:
        tokens = line.split()
        if not tokens:
            new_list_strings.append("")
            new_list_sublists.append([])
            continue
        last_two = tokens[-2:] if len(tokens) >= 2 else tokens[:]
        new_list_strings.append(" ".join(last_two))
        new_list_sublists.append(last_two)
    return new_list_strings, new_list_sublists

def build_key_value_lists(split_list: list) -> tuple:
    """
    From split_list (list of sublists), build:
      key_list: first element of each sublist (or empty string if missing)
      value_list: second element of each sublist with '$' removed (or empty string if missing)
    """
    key_list = []
    value_list = []
    for sub in split_list:
        if not sub:
            key_list.append("")
            value_list.append("")
            continue
        key = sub[0]
        val = sub[1] if len(sub) > 1 else ""
        val = val.replace("$", "")
        key_list.append(key)
        value_list.append(val)
    return key_list, value_list

def build_data_dict(keys: list, values: list) -> dict:
    """Create a dictionary mapping each key to its corresponding value. If duplicate keys exist, later values overwrite earlier ones."""
    return {k: v for k, v in zip(keys, values)}

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

if __name__ == "__main__":
    #pdf_path = os.path.join(os.path.expanduser("~"), "Downloads", "Watchlist.pdf")

    # 1) Read all lines from the PDF
    all_lines = read_pdf_lines(pdf_path)

    # 2) Slice from the first occurrence of "Watchlist"
    sliced = slice_from_keyword(all_lines, keyword="Watchlist")

    # 3) Remove first 2 and last 24 elements safely
    trimmed = safe_trim(sliced, remove_first=2, remove_last=24)

    # 4) Copy last two tokens of each element into a new list and split into sublists
    new_list_strings, new_list_sublists = last_two_tokens_per_line(trimmed)

    # 5) Build key_list and value_list
    key_list, value_list = build_key_value_lists(new_list_sublists)

    # 6) Build dictionary data_list mapping key -> value
    data_list = build_data_dict(key_list, value_list)

    # 7) Print results
    # print("Trimmed list:")
    # print(trimmed)
    #
    # print("\nNew list (last two tokens as strings):")
    # print(new_list_strings)
    #
    # print("\nNew list split into sublists:")
    # print(new_list_sublists)
    #
    # print("\nkey_list:")
    # print(key_list)
    #
    # print("\nvalue_list:")
    # print(value_list)

    # print("\ndata_list (dictionary):")
    # print(data_list)

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

    fetch_Stock_Name(stock_Dictionary:={})

    print('\n\n')
    sys.stdout = Logger()

    for stock in stock_Dictionary.keys():
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        target_price = data_list[stock].replace(",","")

        try:
            float(target_price)
            pass
        except ValueError:
            target_price = "0.00"

        print ("\n1y Target Est = %s\n" % (target_price))

