#!/usr/bin/env python3

# Read a cHase_file_nameby lines, start at the first occurrence of "Watch_list",
# collect lines into a list, remove the first element and the last three elements,
# then for each full 5-line block extract the substring inside parentheses from
# the block's 1st line and copy the whole 5th line into a new list, and print the new list.
# 
# cHase_file_namepath used exactly as requested:
#     os.path.expanduser('~') + '\\Downloads\\' + 'Markets - Watchlists - chase.com.pdf'
# 
# As a Python developer, develope a python script to read the file
# os.path.expanduser( '~' ) + '\\Downloads\\'+ \\Markets - Watchlists - chase.com.pdf  by lines,  start from "Watchlist",
# output  to list, after remove the first element from the list and last three elements,
# copy the string in the parentheses of every first element. copy every fifth element to a new list
#

# each element from the list, get the key "Ticker" value, split and copy the first element key_list
# each element from the list, get the key 'Price Target' value, remove "$" copy to value_list
# printout key_list
# printout value_list
# create a  dictionary variable data_list
# zip key_list and value_list to data_list

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



import time
import datetime
from datetime import date
from path import Path
import os
import sys
import shutil
import re
import logging
from typing import List


logger = logging.getLogger("")

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
stock_txt_path = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\" + "STOCK.txt"
cHase_pdf_file = cHase_file_name + ".pdf"
cHase_data_file = cHase_file_name + ".txt"
text_path = stock_txt_path
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
        self.log = open(dataPath + "\\Summary_Report_From_Chase_"+ today.strftime("%m%d%Y") + ".txt" , "w")

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

    start_idx = find_watch_list_start(all_lines)
    # Collect from the Watch_list line (inclusive) to the end
    lines_from_watch = all_lines[start_idx:]

    processed_list = build_new_list(lines_from_watch)

    data_list = {}
    keys_list = processed_list[::2]   # Start from beginning, step by 2
    values_list = processed_list[1::2]
    data_list = dict(zip(keys_list, values_list))

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

        print ("")
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        target_price = data_list[stock].replace("$","")
        print ("\n1y Target Est = %s\n" % (target_price))

if __name__ == "__main__":
    main()
