#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
As a Python developer, develope a python script to read the file
os.path.expanduser( '~' ) + '\Downloads\\'+ \\Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.pdf  by lines,  start from "Watchlist"

after line  containing  "Overview Zen Rating Price Value Growth",
Find the table, grab data in column "Ticker" and "Price Target", stop the line containing "How to Use a Stock Screener",
Remove the string "Strong Buy", remove the string "Buy". remove the string "Unlock", Split string under column" Price Target",
Remove all elements except the third from the end.
covert and output the dataframe to a list
remove first seven elements from the list
remove last elements from the list
printout the list

each element from the list, get the key "Ticker" value, split and copy the first element key_list
each element from the list, get the key 'Price Target' value, remove "$" copy to value_list
printout key_list
printout value_list
create a  dictionary variable data_list
zap key_list and value_list to data_list
printout data_list
"""

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
from datetime import timedelta
import pdfplumber

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\WallStreetZen\\"
downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
WallStreetZen_data_file_name = "Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen"
WallStreetZen_pdf_file = WallStreetZen_data_file_name + ".pdf"
WallStreetZen_data_file = WallStreetZen_data_file_name + ".txt"
source = downloadPath + WallStreetZen_data_file
# sTanley_data_file = sTanley_file_name + ".txt"
# source = downloadPath + sTanley_data_file
pdf_path = downloadPath+ WallStreetZen_pdf_file

# downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
# pdf_path = Path(downloadPath + r"Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.pdf")
#OUTPUT_CSV = Path(PDF_PATH).with_suffix(".csv")

# Prefer pdfplumber for text extraction; fallback to PyPDF2
try:
    import pdfplumber
    _HAS_PDFPLUMBER = True
except Exception:
    _HAS_PDFPLUMBER = False
    try:
        from PyPDF2 import PdfReader
    except Exception:
        PdfReader = None

# pandas optional (used only to convert to DataFrame then to list if available)
try:
    import pandas as pd
except Exception:
    pd = None

# --- Configuration ---
FILENAME = "Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.pdf"
OVERVIEW_MARKER = "Overview Zen Rating Price Value Growth"
WATCHLIST_MARKER = "Watchlist"
STOP_MARKER = "How to Use a Stock Screener"

# tokens to remove from any field before parsing
UNWANTED_TOKENS_RE = re.compile(r'\b(Strong Buy|Buy|Unlock)\b', flags=re.IGNORECASE)
# separators used to split Price Target
SPLIT_SEPARATORS_RE = re.compile(r'[\s,\/\|\-\(\)]+')
# heuristic for ticker-like token
TICKER_RE = re.compile(r'^[A-Z0-9.\-]{1,8}$')

# number of items to remove from the start and end of the final list
N_REMOVE_FROM_START = 7
N_REMOVE_FROM_END = 1  # change if you want to remove more than one from the end


def read_pdf_lines(path):
    """Extract text lines from PDF using pdfplumber or PyPDF2 fallback."""
    lines = []
    if _HAS_PDFPLUMBER:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                for ln in text.splitlines():
                    lines.append(ln.rstrip())
    else:
        if PdfReader is None:
            raise RuntimeError("Install pdfplumber or PyPDF2 to extract PDF text.")
        reader = PdfReader(path)
        for page in reader.pages:
            text = page.extract_text() or ""
            for ln in text.splitlines():
                lines.append(ln.rstrip())
    return lines


def remove_unwanted_tokens(s: str) -> str:
    """Remove Strong Buy, Buy, Unlock and normalize whitespace."""
    if not s:
        return ""
    s = UNWANTED_TOKENS_RE.sub("", s)
    return re.sub(r'\s+', ' ', s).strip()


def third_from_end_token(s: str) -> str:
    """
    Split s on common separators and return the third-from-last element.
    If fewer than 3 tokens exist, return empty string.
    """
    if not s:
        return ""
    parts = [p for p in SPLIT_SEPARATORS_RE.split(s) if p != ""]
    if len(parts) >= 3:
        return parts[-3]
    return ""


def find_start_index(lines, overview_marker, watchlist_marker):
    """
    Find the index to start parsing:
      - locate overview_marker line
      - then find the next Watchlist line after it
      - start parsing after the Watchlist line
    Fallback: first Watchlist anywhere.
    """
    om = overview_marker.lower()
    wm = watchlist_marker.lower()
    for i, ln in enumerate(lines):
        if om in ln.lower():
            for j in range(i + 1, min(i + 500, len(lines))):
                if wm in lines[j].lower():
                    return j + 1
    # fallback: first Watchlist anywhere
    for i, ln in enumerate(lines):
        if wm in ln.lower():
            return i + 1
    return None


def parse_table_section(lines, start_idx, stop_marker):
    """
    Parse lines from start_idx until stop_marker.
    Heuristics:
      - detect header row containing 'Ticker' and 'Price' to map columns
      - otherwise assume first column is ticker and last column is price target
      - remove unwanted tokens before parsing
      - return list of dicts with keys 'Ticker' and 'Price Target'
    """
    stop_l = stop_marker.lower()
    rows = []
    header_map = None

    for i in range(start_idx, len(lines)):
        ln = lines[i]
        if stop_l in ln.lower():
            break
        if not ln.strip():
            continue

        ln_clean = remove_unwanted_tokens(ln)

        # split into columns by runs of 2+ spaces, tabs, or vertical bars
        cols = [c.strip() for c in re.split(r'\s{2,}|\t|\s*\|\s*', ln_clean) if c.strip() != ""]

        # detect header row
        if header_map is None:
            lower_cols = [c.lower() for c in cols]
            if any('ticker' in c for c in lower_cols) and any('price' in c or 'target' in c for c in lower_cols):
                header_map = {}
                for idx, c in enumerate(lower_cols):
                    if 'ticker' in c:
                        header_map['ticker_idx'] = idx
                    if 'price' in c or 'target' in c:
                        header_map['price_idx'] = idx
                continue  # header line not a data row

        ticker = ""
        price_raw = ""

        if header_map:
            ti = header_map.get('ticker_idx')
            pi = header_map.get('price_idx')
            if ti is not None and ti < len(cols):
                ticker = cols[ti]
            if pi is not None and pi < len(cols):
                price_raw = cols[pi]
            if not ticker and len(cols) >= 1:
                ticker = cols[0]
            if not price_raw and len(cols) >= 2:
                price_raw = cols[-1]
        else:
            # try to find a ticker-like token among columns
            found_ticker = None
            for c in cols:
                if TICKER_RE.fullmatch(c):
                    found_ticker = c
                    break
            if found_ticker:
                ticker = found_ticker
                price_raw = cols[-1] if len(cols) >= 2 else ""
            else:
                if len(cols) >= 2:
                    ticker = cols[0]
                    price_raw = cols[-1]
                else:
                    # single-column fallback: regex for "TICKER ... Price Target ..."
                    m = re.search(
                        r'([A-Z]{1,5}(?:[.\-][A-Z0-9]{1,4})?)\b.*?(?:Price Target[:\s]*|PT[:\s]*|\$)?([0-9\.,\s\w\-/\|()]+)',
                        ln_clean, flags=re.IGNORECASE)
                    if m:
                        ticker = m.group(1).strip()
                        price_raw = m.group(2).strip()
                    else:
                        continue  # skip unparseable line

        ticker = remove_unwanted_tokens(ticker)
        price_raw = remove_unwanted_tokens(price_raw)
        price_selected = third_from_end_token(price_raw)

        rows.append({'Ticker': ticker, 'Price Target': price_selected})

    return rows

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

    lines = read_pdf_lines(pdf_path)

    start_idx = find_start_index(lines, OVERVIEW_MARKER, WATCHLIST_MARKER)
    if start_idx is None:
        print("Could not locate the Watchlist start after the Overview marker.", file=sys.stderr)
        sys.exit(1)

    parsed_rows = parse_table_section(lines, start_idx, STOP_MARKER)

    # Convert to DataFrame then to list if pandas is available, else keep list
    if pd is not None:
        df = pd.DataFrame(parsed_rows)
        result_list = df.to_dict(orient='records')
    else:
        result_list = parsed_rows

    # Remove first N_REMOVE_FROM_START elements
    if len(result_list) > N_REMOVE_FROM_START:
        result_list = result_list[N_REMOVE_FROM_START:]
    else:
        result_list = []

    # Remove last N_REMOVE_FROM_END elements
    if N_REMOVE_FROM_END > 0 and len(result_list) >= N_REMOVE_FROM_END:
        result_list = result_list[:-N_REMOVE_FROM_END]

    # Print the trimmed list
    # print("Trimmed result_list:")
    # print(result_list)

    # Build key_list (first token of Ticker) and value_list (Price Target with $ removed)
    key_list = []
    value_list = []
    for rec in result_list:
        ticker = rec.get('Ticker', '') or ''
        # split ticker by whitespace or common separators and take first element
        first_token = re.split(r'[\s\/\|\-]+', ticker.strip())[0] if ticker.strip() else ''
        key_list.append(first_token)
        price = rec.get('Price Target', '') or ''
        # remove leading $ if present and any commas
        price_clean = price.replace('$', '').replace(',', '').strip()
        value_list.append(price_clean)

    # print("key_list:")
    # print(key_list)
    # print("value_list:")
    # print(value_list)

    # Create data_list dictionary by zapping key_list and value_list together
    # If duplicate keys occur, later values overwrite earlier ones.
    data_list = {k: v for k, v in zip(key_list, value_list)}

    # print("data_list:")
    # print(data_list)

    # Return for programmatic use
    # return {
    #     'result_list': result_list,
    #     'key_list': key_list,
    #     'value_list': value_list,
    #     'data_list': data_list
    # }

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
        target = data_list[stock].replace(",","")
        #target = data_list[stock].replace("$","").replace(",","")
        if (data_list[stock])[-1] == 'k':
                target = str(float(target.replace("k", "")) * 1000)
        print ("\n1y Target Est = %s\n" % (str(target)))

if __name__ == "__main__":
    main()
