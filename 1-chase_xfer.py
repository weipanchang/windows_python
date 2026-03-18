#!/usr/bin/env python3
"""
Read a cHase_file_nameby lines, start at the first occurrence of "Watch_list",
collect lines into a list, remove the first element and the last three elements,
then for each full 5-line block extract the substring inside parentheses from
the block's 1st line and copy the whole 5th line into a new list, and print the new list.

cHase_file_namepath used exactly as requested:
    os.path.expanduser('~') + '\\Downloads\\' + 'Markets - Watchlists - chase.com.pdf'

As a Python developer, develope a python script to read the file
os.path.expanduser( '~' ) + '\\Downloads\\'+ \\Markets - Watchlists - chase.com.pdf  by lines,  start from "Watchlist",
output  to list, after remove the first element from the list and last three elements,
copy the string in the parentheses of every first element. copy every fifth element to a new list
printout the new list

"""
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
import logging.handlers
#import pymupdf
# import pdfplumber
from typing import List
from pprint import pprint

logger = logging.getLogger("watchlist_parens_and_fifth")

logging.basicConfig(level=logging.CRITICAL, format="%(levelname)s: %(message)s")

#Prefer pdfplumber for text extraction; fallback to PyPDF2
try:
    import pdfplumber

    _HAS_PDFPLUMBER = True
except Exception:
    _HAS_PDFPLUMBER = False

dataPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Chase\\"
downloadPath = os.path.expanduser( '~' ) + '\\Downloads\\'
cHase_file_name = "Markets - Watchlists - chase.com"
cHase_pdf_file = cHase_file_name + ".pdf"
cHase_data_file = cHase_file_name + ".txt"
source = downloadPath + cHase_pdf_file



#cHase_pdf_file = os.path.expanduser("~") + "\\Downloads\\" + "Markets - Watchlists - chase.com.pdf"
WATCHLIST_RE = re.compile(r"Watch_list", re.IGNORECASE)
PARENS_RE = re.compile(r"\(([^)]*)\)")

def extract_lines_from_pdf(path: str) -> List[str]:
    """
    Extract all text lines from the cHase_file_nameand return them as a flat list of strings.
    """
    if not os.path.isfile(source ):
        logger.error("cHase_file_namenot found at: %s", source )
        sys.exit(1)

    lines: List[str] = []

    if _HAS_PDFPLUMBER:
        try:
            logger.info("Extracting text with pdfplumber.")
            with pdfplumber.open(source) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    for ln in text.splitlines():
                        lines.append(ln.rstrip())
            return lines
        except Exception as e:
            logger.warning("pdfplumber extraction failed: %s", e)

def find_watch_list_start(all_lines: List[str]) -> int:
    """
    Return index of the first line that contains 'Watch_list' (case-insensitive).
    If not found, exit.
    """
    for idx, ln in enumerate(all_lines):
        if WATCHLIST_RE.search(ln):
            logger.info("Found 'Watch_list' at line index %d.", idx)
            return idx
    logger.error("'Watch_list' not found in document.")
    sys.exit(2)


def extract_first_paren(text: str) -> str:
    """
    Return the first substring inside parentheses in text, or empty string if none.
    """
    m = PARENS_RE.search(text)
    return m.group(1).strip() if m else ""


def build_new_list(lines_from_watch: List[str]) -> List[str]:
    """
    - Remove the first element from lines_from_watch.
    - Remove the last three elements.
    - Partition the remainder into consecutive 5-line blocks.
    - For each full block, extract parentheses content from block[0] and
      take the whole block[4]; append them to new_list in that order.
    """
    if not lines_from_watch:
        return []

    working = list(lines_from_watch)  # copy to avoid mutating caller

    # Remove the first element if present
    removed_first = working.pop(0) if working else None
    logger.info("Removed first element: %r", removed_first)

    # Remove last three elements (or fewer if not enough)
    removed_last = []
    for _ in range(min(3, len(working))):
        removed_last.append(working.pop())
    if removed_last:
        removed_last.reverse()
        logger.info("Removed last elements: %r", removed_last)

    new_list: List[str] = []
    block_size = 5
    i = 0
    while i + block_size - 1 < len(working):
        block = working[i : i + block_size]
        first_text = block[0]
        fifth_text = block[4]
        first_paren = extract_first_paren(first_text)
        # Append the parentheses string (may be empty) and the whole fifth line
        new_list.append(first_paren)
        new_list.append(fifth_text)
        i += block_size

    if i < len(working):
        logger.info("Ignored trailing %d lines after last full 5-line block.", len(working) - i)

    return new_list

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
    # logger.info("cHase_file_namepath: %s", cHase_pdf_file)
    all_lines = extract_lines_from_pdf(source)
    # if not all_lines:
    #     logger.error("No text extracted from PDF.")
    #     sys.exit(1)

    start_idx = find_watch_list_start(all_lines)
    # Collect from the Watch_list line (inclusive) to the end
    lines_from_watch = all_lines[start_idx:]

    processed_list = build_new_list(lines_from_watch)

    data_list = {}
    keys_list = processed_list[::2]   # Start from beginning, step by 2
    values_list = processed_list[1::2]
    data_list = dict(zip(keys_list, values_list))

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

    #shutil.move(source, dataPath)

    fetch_Stock_Name(stock_Dictionary:={})

    sys.stdout = Logger()

    for stock in stock_Dictionary.keys():

        print ("")
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        target_price = data_list[stock].replace("$","")
        print ("\n1y Target Est = %s\n" % (target_price))

if __name__ == "__main__":
    main()
