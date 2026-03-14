#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Extract 'Ticker' and 'Price Target' from a PDF region defined by two marker lines,
# remove "Strong Buy" and "Buy", split the Price Target cell and keep the third-from-end
# token, then save results to CSV with every field double-quoted.
# 
# Adjust PDF_PATH if needed.
# 
# As a Python developer, develope a python script to read the file
# C:\Users\William Chang\Downloads\Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.pdf
# Return_Records.pdf , after line  containing  "Overview Zen Rating Price Value Growth",
# find the table, grab data in column "Ticker" and "Price Target", stop the line containing "How to Use a Stock Screener",
# remove the string "Strong Buy", remove the string "Buy". remove the string "Unlock", Split string under column" Price Target",
# remove all elements except the third from the end. output to csv with double quote format



from pathlib import Path
import re
import csv
import sys
from typing import List, Optional
import os
import pandas as pd
import pdfplumber


downloadPath = os.path.expanduser( '~' ) + '\Downloads\\'
PDF_PATH = Path(downloadPath + r"Best Stock Screener App In 2026 - #1 Top Free Stock Scanner _ WallStreetZen.pdf")
OUTPUT_CSV = Path(PDF_PATH).with_suffix(".csv")
#OUTPUT_CSV = Path(PDF_PATH).with_suffix(".tickers_price_targets.csv")


START_MARKER = "Overview Zen Rating Price Value Growth"
END_MARKER = "How to Use a Stock Screener"

# Strings to remove from cells
REMOVE_STRINGS = ["Strong Buy", "Buy", "Unlock"]

# Heuristic regex to detect ticker tokens (1-5 uppercase letters, optional dot suffix)
TICKER_RE = re.compile(r'^[A-Z]{1,5}(?:\.[A-Z]{1,2})?$')

# Helper functions
def remove_unwanted_strings(s: str) -> str:
    if s is None:
        return ""
    out = str(s)
    for rem in REMOVE_STRINGS:
        out = re.sub(re.escape(rem), "", out, flags=re.IGNORECASE)
    return out.strip()

def normalize_price_token(tok: str):
    """
    Normalize a token like '$305.12', '1.06k', '305.12' into a numeric value when possible.
    If conversion fails, return the cleaned token string.
    """
    if tok is None:
        return ""
    s = str(tok).strip()
    s = s.replace('$', '').replace(',', '')
    if not s:
        return ""
    # handle trailing 'k' or 'K' as thousands
    if s.lower().endswith('k'):
        try:
            return float(s[:-1]) * 1000
        except:
            return s
    # handle trailing 'm' or 'b' if present (optional)
    if s.lower().endswith('m'):
        try:
            return float(s[:-1]) * 1_000_000
        except:
            return s
    if s.lower().endswith('b'):
        try:
            return float(s[:-1]) * 1_000_000_000
        except:
            return s
    # try float
    try:
        return float(s)
    except:
        # fallback: strip non-numeric except dot and minus
        s2 = re.sub(r'[^0-9.\-]', '', s)
        try:
            return float(s2)
        except:
            return s

def extract_region_lines(pdf_path: str) -> dict:
    """
    Return lines between START_MARKER (exclusive) and END_MARKER (exclusive),
    and the page range that contains the region.
    """
    lines_between: List[str] = []
    start_found = False
    end_found = False
    start_page_idx: Optional[int] = None
    end_page_idx: Optional[int] = None

    with pdfplumber.open(pdf_path) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            page_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            if not start_found:
                for i, ln in enumerate(page_lines):
                    if START_MARKER.lower() in ln.lower():
                        start_found = True
                        start_page_idx = p_idx
                        # collect lines after the marker on the same page
                        lines_between.extend(page_lines[i+1:])
                        break
            else:
                stop_here = False
                for i, ln in enumerate(page_lines):
                    if END_MARKER.lower() in ln.lower():
                        end_found = True
                        end_page_idx = p_idx
                        # collect lines before the end marker on this page
                        lines_between.extend(page_lines[:i])
                        stop_here = True
                        break
                if not stop_here:
                    lines_between.extend(page_lines)
            if end_found:
                break

    return {
        "lines": lines_between,
        "start_page": start_page_idx,
        "end_page": end_page_idx if end_page_idx is not None else start_page_idx
    }

def try_extract_tables_pdfplumber(pdf_path: str, start_page: Optional[int], end_page: Optional[int]) -> Optional[pd.DataFrame]:
    """
    Try to extract tables from pages in [start_page, end_page] using pdfplumber.
    Return combined DataFrame or None.
    """
    if start_page is None:
        return None
    dfs = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in range(start_page, (end_page or start_page) + 1):
            if p < 0 or p >= len(pdf.pages):
                continue
            page = pdf.pages[p]
            try:
                tables = page.extract_tables()
            except Exception:
                tables = None
            if tables:
                for tbl in tables:
                    if len(tbl) >= 2:
                        df = pd.DataFrame(tbl[1:], columns=tbl[0])
                    else:
                        df = pd.DataFrame(tbl)
                    dfs.append(df)
    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        return combined
    return None

def normalize_cols_and_select(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Normalize column names and select 'Ticker' and 'Price Target' if present.
    """
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if 'ticker' in lc:
            col_map['Ticker'] = c
        if 'price target' in lc or ('price' in lc and 'target' in lc) or lc == 'price' or 'target' in lc:
            col_map.setdefault('Price Target', c)
    if 'Ticker' in col_map and 'Price Target' in col_map:
        out = df[[col_map['Ticker'], col_map['Price Target']]].copy()
        out.columns = ['Ticker', 'Price Target']
        # clean unwanted strings
        out['Ticker'] = out['Ticker'].astype(str).apply(remove_unwanted_strings).str.upper()
        out['Price Target'] = out['Price Target'].astype(str).apply(remove_unwanted_strings)
        # For Price Target column, split tokens and keep third-from-end
        def pick_third_from_end(cell: str):
            tokens = [t for t in re.split(r'\s+', cell) if t]
            if len(tokens) >= 3:
                tok = tokens[-3]
                return normalize_price_token(tok)
            # fallback: try to find a numeric-looking token anywhere
            for t in tokens[::-1]:
                if re.search(r'\d', t):
                    return normalize_price_token(t)
            return ""
        out['Price Target'] = out['Price Target'].apply(pick_third_from_end)
        return out
    return None

def parse_lines_for_pairs(lines: List[str]) -> pd.DataFrame:
    """
    Parse free text lines for ticker + price target pairs using token positions.
    Assumes lines are rows like:
      APPLE INC $3.83T $260.81 $305.12 16.99% Buy 22
    We'll try to find the ticker token and then pick the token at -3 as Price Target.
    """
    extracted = []
    for ln in lines:
        ln_clean = remove_unwanted_strings(ln)
        tokens = [t for t in re.split(r'\s+', ln_clean) if t]
        if not tokens:
            continue
        # find first token that looks like a ticker
        ticker = None
        for i, tok in enumerate(tokens):
            if TICKER_RE.match(tok):
                ticker = tok.upper()
                # attempt to pick price target as token at -3 relative to end
                if len(tokens) >= 3:
                    candidate = tokens[-3]
                    price_val = normalize_price_token(candidate)
                else:
                    # fallback: find first numeric-looking token after ticker
                    price_val = ""
                    for t2 in tokens[i+1:]:
                        if re.search(r'\d', t2):
                            price_val = normalize_price_token(t2)
                            break
                extracted.append({"Ticker": ticker, "Price Target": price_val})
                break
    if not extracted:
        return pd.DataFrame(columns=['Ticker', 'Price Target'])
    df = pd.DataFrame(extracted)
    df = df.drop_duplicates(subset=['Ticker'], keep='first').reset_index(drop=True)
    return df

def save_csv_double_quoted(df: pd.DataFrame, out_path: Path):
    df = df[['Ticker', 'Price Target']].copy()
    # Convert Price Target to string to preserve formatting
    df['Price Target'] = df['Price Target'].apply(lambda v: "" if v is None else str(v))
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['Ticker', 'Price Target'])
        for _, row in df.iterrows():
            writer.writerow([row['Ticker'], row['Price Target']])

def extract_ticker_price(pdf_path: str) -> pd.DataFrame:
    p = Path(pdf_path)
    if not p.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    region = extract_region_lines(pdf_path)
    lines = region["lines"]
    start_page = region["start_page"]
    end_page = region["end_page"]

    # 1) Try pdfplumber table extraction on region pages
    df_tables = try_extract_tables_pdfplumber(pdf_path, start_page, end_page)
    if df_tables is not None:
        normalized = normalize_cols_and_select(df_tables)
        if normalized is not None and not normalized.empty:
            return normalized

    # 2) Fallback: parse collected lines with token heuristic
    parsed = parse_lines_for_pairs(lines)
    if not parsed.empty:
        return parsed

    # 3) Nothing found
    return pd.DataFrame(columns=['Ticker', 'Price Target'])

if __name__ == "__main__":
    try:
        result = extract_ticker_price(PDF_PATH)
        if result.empty:
            print("No Ticker / Price Target pairs found in the specified region.")
            sys.exit(1)
        save_csv_double_quoted(result, OUTPUT_CSV)
        print(f"Saved {len(result)} rows to: {OUTPUT_CSV}")
    except Exception as exc:
        print("Error during extraction:", exc)
        sys.exit(2)
