#!/usr/bin/env python3

from typing import List, Tuple, Dict
import time
import datetime
from datetime import date
from path import Path
import os
import sys
import shutil
import re
import logging

logger = logging.getLogger("")
logging.basicConfig(level=logging.CRITICAL, format="%(levelname)s: %(message)s")

# read the file
# os.path.expanduser( '~' ) + '\\Downloads\\'+ \\Watchlist.pdf  by lines,  starting after the line that contains "Next Year".
# Removes commas from each line
# output  to list,
#
# Default PDF path:
# os.path.join(os.path.expanduser("~"), "Downloads", "Stock Watchlist & Portfolio Tracker.pdf")
# copy the first string in each element in the list to a list key_list
# copy the forth string in each element in the list to a list value_list
#
# create a dictionary type variable data_list
# zap key_list, value_list to data_list

# read
# os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\" + "STOCK.txt" to line_list

# copy  the string in the parentheses of each element in line_list to a list key_list
# copy the string from begining to the ninth character from the end to a list value1_list
# copy the string in the  square brackets of each element in line_list to a list value2_list
#
# copy element  from value1_list, "stock", element from value2_list to value_list
#
# create a dictionary type variable stock_Dictionary
# zip key_list, value_list to stock_Dictionary

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stock_Analysis\\"
downloadPath = os.path.expanduser( '~' ) + r'\\Downloads\\'
sTock_Analysis_data_file_name = "Stock Watchlist & Portfolio Tracker"
sTock_Analysis_pdf_file = sTock_Analysis_data_file_name + ".pdf"
sTock_Analysis_data_file = sTock_Analysis_data_file_name + ".csv"
source = downloadPath + sTock_Analysis_pdf_file
stock_txt_path = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\" + "STOCK.txt"
text_path = stock_txt_path
pdf_path = source

def extract_text_lines(pdf_path):
    """
    Extract text lines from a PDF. Try pdfplumber first, then PyPDF2.
    Returns a list of lines (strings).
    """
    # pdfplumber preferred
    try:
        import pdfplumber
        lines = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                lines.extend(text.splitlines())
        return lines
    except Exception:
        pass

    # fallback to PyPDF2
    try:
        import PyPDF2
        lines = []
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text() or ""
                lines.extend(text.splitlines())
        return lines
    except Exception:
        pass

    raise RuntimeError("No PDF text extractor available. Install pdfplumber or PyPDF2.")

def parse_watchlist(pdf_path=None):
    """
    Parse the watchlist PDF per the user's rules and return:
      rows: list of token lists (each line -> tokens after comma removal)
      key_list: list of first tokens
      value_list: list of values per rule
      data_list: dict mapping key -> value
    """
    if pdf_path is None:
        pdf_path = source

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    lines = extract_text_lines(pdf_path)

    # find first line containing "Next Year" and start after it
    start_idx = None
    for i, ln in enumerate(lines):
        if "Next Year" in ln:
            start_idx = i + 1
            break
    if start_idx is None:
        raise ValueError('Could not find a line containing "Next Year" in the PDF text.')

    rows = []
    for ln in lines[start_idx:]:
        cleaned = ln.replace(",", "")
        if not cleaned.strip():
            continue
        parts = cleaned.split()
        if parts:
            rows.append(parts)

    key_list = []
    value_list = []
    for parts in rows:
        # key: first token (guaranteed by rows construction)
        key = parts[0] if len(parts) >= 1 else ""
        key_list.append(key)

        # value selection rule:
        # if third token exists and its last character is '%', use fourth token (if present)
        # else use third token (if present). If missing, use empty string.
        val = ""
        if len(parts) >= 3:
            third = parts[2]
            if third.endswith("%"):
                val = parts[3] if len(parts) >= 4 else ""
            else:
                val = third
        elif len(parts) == 2:
            # fallback: only two tokens, use second as value
            val = parts[1]
        else:
            val = ""
        value_list.append(val)

    # create dictionary mapping keys to values
    data_list = dict(zip(key_list, value_list))

    return key_list, value_list, data_list

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


if __name__ == "__main__":
    key_list, value_list, data_list = parse_watchlist()

    build_stock_dictionary

    try:
        shutil.rmtree(dataPath)
    except:
         pass
    time.sleep(2)
    try:
        os.mkdir(dataPath)
    except:
        pass

    stock_Dictionary = build_stock_dictionary(text_path)

    sys.stdout = Logger()

    for stock in stock_Dictionary.keys():

        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        print ("\n1y Target Est = %s\n" % (data_list[stock]))
