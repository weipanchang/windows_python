#!/usr/bin/env python3
"""
Extract the first and fourth token from each line in a PDF starting at the line that contains "Next Year".
Removes commas from each line before tokenizing.

Default PDF path:
os.path.join(os.path.expanduser("~"), "Downloads", "Stock Watchlist & Portfolio Tracker.pdf")

Outputs:
- key_list: list of first tokens
- value_list: list of fourth tokens (or None if missing)
- data_list: dict mapping key -> value (later keys overwrite earlier ones)
"""


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
import argparse


dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stock_Analysis\\"
downloadPath = os.path.expanduser( '~' ) + r'\Downloads\\'
sTock_Analysis_data_file_name = "Stock Watchlist & Portfolio Tracker"
sTock_Analysis_pdf_file = sTock_Analysis_data_file_name + ".pdf"
sTock_Analysis_data_file = sTock_Analysis_data_file_name + ".csv"
source = downloadPath + sTock_Analysis_pdf_file
pdf_path = source

# Try preferred extractor first
try:
    import pdfplumber
    ENGINE = "pdfplumber"
except Exception:
    try:
        from pypdf import PdfReader
        ENGINE = "pypdf"
    except Exception:
        ENGINE = None

def extract_lines_from_pdf(path):
    """Extract text lines from PDF in reading order."""
    if ENGINE == "pdfplumber":
        lines = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                lines.extend([ln.rstrip() for ln in text.splitlines()])
        return lines

    if ENGINE == "pypdf":
        lines = []
        with open(path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text = page.extract_text() or ""
                lines.extend([ln.rstrip() for ln in text.splitlines()])
        return lines

    raise RuntimeError("No PDF engine available. Install pdfplumber or pypdf (pip install pdfplumber pypdf).")

def process_lines(lines, start_pattern="Next Year", remove_commas=True, case_sensitive=False):
    """
    Find the first line containing start_pattern and process subsequent lines.
    Returns (key_list, value_list, data_dict, start_index).
    """
    if not case_sensitive:
        cmp = lambda s: s.lower()
        pat = start_pattern.lower()
    else:
        cmp = lambda s: s
        pat = start_pattern

    start_idx = -1
    for i, ln in enumerate(lines):
        if pat in cmp(ln):
            start_idx = i
            break

    if start_idx == -1:
        return [], [], {}, -1

    key_list = []
    value_list = []
    data_list = {}

    for ln in lines[start_idx + 1:]:
        if not ln or not ln.strip():
            continue
        if remove_commas:
            ln = ln.replace(",", "")
        tokens = ln.strip().split()
        if not tokens:
            continue
        key = tokens[0]
        value = tokens[3] if len(tokens) > 3 else None
        key_list.append(key)
        value_list.append(value)
        data_list[key] = value

    return key_list, value_list, data_list, start_idx

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
    parser = argparse.ArgumentParser(description="Extract first and fourth tokens from PDF lines starting at 'Next Year'.")
    parser.add_argument("--pdf", "-p",
                        default=source,
                        help="Path to PDF file (default: Downloads/Stock Watchlist & Portfolio Tracker.pdf)")
    parser.add_argument("--pattern", default="Next Year", help="Start pattern (default: 'Next Year')")
    parser.add_argument("--no-remove-commas", dest="remove_commas", action="store_false",
                        help="Do not remove commas before tokenizing")
    args = parser.parse_args()

    pdf_path = args.pdf
    if not os.path.isfile(pdf_path):
        print(f"PDF not found at: {pdf_path}", file=sys.stderr)
        sys.exit(2)

    if ENGINE is None:
        print("Install pdfplumber or pypdf: pip install pdfplumber pypdf", file=sys.stderr)
        sys.exit(3)

    try:
        lines = extract_lines_from_pdf(pdf_path)
    except Exception as e:
        print("Failed to extract text from PDF:", e, file=sys.stderr)
        sys.exit(4)

    key_list, value_list, data_list, start_idx = process_lines(
        lines,
        start_pattern=args.pattern,
        remove_commas=args.remove_commas,
        case_sensitive=False
    )
    # print(key_list)
    # print(data_list)
    if start_idx == -1:
        print(f"Start pattern '{args.pattern}' not found in document.", file=sys.stderr)
        sys.exit(5)

    def fetch_Stock_Name(stock_Dictionary):
        stock_fund_names =  [line for line in open("STOCK.txt", "r")]
        for stock_fund_name in stock_fund_names:
            if len(stock_fund_name) < 2 or "IGNOR" in stock_fund_name :
                continue

            stock = re.search(r'(\(\^\w+\))', stock_fund_name)
            if stock is None:
                stock = re.search(r'\(\w+\)', stock_fund_name)
                msft_ticket = re.search(r'\[\w+\]', stock_fund_name)

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

#    shutil.move(source, dataPath)
    fetch_Stock_Name(stock_Dictionary:={})

#    print(stock_Dictionary)
    sys.stdout = Logger()
#    os.system("pause")

    #extract_data(data_list:={})
    for stock in stock_Dictionary.keys():

        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        print ("\n1y Target Est = %s\n" % (data_list[stock].replace('"','')))




if __name__ == "__main__":
    main()
