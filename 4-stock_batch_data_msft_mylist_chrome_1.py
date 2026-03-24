#!/usr/bin/env python
import requests, urllib3, sys
import re
from path import Path
import os
import holidays
import shutil
import random
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from datetime import date

# For automatic driver management
from webdriver_manager.chrome import ChromeDriverManager

downloadPath = os.path.expanduser('~') + "\\Documents\\Python Scripts\\MSFT_Analysis"
# Ensure the directory exists for the chdir call
if not os.path.exists(os.path.expanduser('~') + "\\Documents\\Python Scripts"):
    os.makedirs(os.path.expanduser('~') + "\\Documents\\Python Scripts")
Path(os.path.expanduser('~') + "\\Documents\\Python Scripts").chdir()

stock = ""

class Logger(object):
    def __init__(self):
        global stock
        today = date.today()
        self.terminal = sys.stdout
        self.log = open(downloadPath + "\\Summary_Report_From_Microsoft_" + today.strftime("%m%d%Y") + ".txt", "a+")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

class init_webdriver():
    def __init__(self):
        global stock
        print("")
        self.currentDateTime = datetime.datetime.now()
        self.date = self.currentDateTime.date()
        
        # 1. Setup Chrome Options
        self.options = Options()
        
        # 2. Chrome Preferences (Replaces Firefox set_preference)
        prefs = {
            "download.default_directory": downloadPath,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
        }
        self.options.add_experimental_option("prefs", prefs)
        
        # 3. Arguments
        self.options.add_argument("--headless=new") # Modern headless mode
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--log-level=3")
        
        # Step 3: Rotate user agents 
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]
        user_agent = random.choice(user_agents)
        self.options.add_argument(f'user-agent={user_agent}')

    def driver_init(self):
        # Uses ChromeDriverManager to automatically handle the chromedriver.exe
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_page_load_timeout(50)
        return self.driver
        
def main():
    global stock
    try:
        if os.path.exists(downloadPath):
            shutil.rmtree(downloadPath)
    except Exception as e:
         print(f"Error cleaning directory: {e}")
    
    time.sleep(2)
    try:
        os.makedirs(downloadPath, exist_ok=True)
    except:
        pass

    now_time = datetime.datetime.now().time()
    print("\nTime: ", now_time, "\n")

    driver = init_webdriver().driver_init()
    
    # Helper functions (keeping your existing logic)
    def check_exists_by_xpath(driver, xpath):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True
        
    def fetch_Stock_Name(stock_Dictionary):
        # Assumes STOCK.txt exists in the working directory
        try:
            with open("STOCK.txt", "r") as f:
                stock_fund_names = f.readlines()
            for stock_fund_name in stock_fund_names:
                if len(stock_fund_name) < 2 or "IGNOR" in stock_fund_name:
                    continue

                stock_match = re.search(r'(\(\^\w+\))', stock_fund_name)
                if stock_match is None:
                    stock_match = re.search(r'\(\w+\)', stock_fund_name)
                
                msft_match = re.search(r'\[\w+\]', stock_fund_name)

                is_stock = re.search("ETF|Fund", stock_fund_name)
                stock_or_fund = 'ETF' if is_stock and 'ETF' in stock_fund_name else ('Fund' if is_stock else 'STOCK')
                
                stock_code = stock_match.group().strip('()')
                msft_ticket = msft_match.group().strip('[]')
                
                stock_Dictionary[stock_code] = [stock_fund_name.rstrip()[:-9], stock_or_fund, msft_ticket]
        except FileNotFoundError:
            print("Error: STOCK.txt not found.")

    stock_Dictionary = {}
    fetch_Stock_Name(stock_Dictionary)
    sys.stdout = Logger()
    
    for stock_key in stock_Dictionary.keys():

        print (("=") * len("Processing " + stock_Dictionary[stock_key][0] +" data"))
        print(f"Processing {stock_Dictionary[stock_key][0]} data")
        print (("=") * len("Processing " + stock_Dictionary[stock_key][0] +" data"))

        msft_ticket = stock_Dictionary[stock_key][2]
        url_stock = f"https://www.msn.com/en-us/money/watchlist?ocid=winp1taskbar&duration=1M&id={msft_ticket}&l3=L3_Earnings"
        driver.get(url_stock)
        driver.implicitly_wait(1)
        time.sleep(3)

        print("Display Earning Page... \n")

        time.sleep(2)
        
        # Price Check logic
        price_found = False
        selectors = [
            '//div[contains(@class, "mainPrice color_red")]',
            '//div[contains(@class, "mainPrice color_green")]',
            '//div[contains(@class, "mainPrice color_nochange")]'
        ]
        
        for selector in selectors:
            if check_exists_by_xpath(driver, selector):
                print(f'Current Price:   {driver.find_element(By.XPATH, selector).text}')
                price_found = True
                break
            
        if check_exists_by_xpath(driver, '//div[@class = "price_PreAfter"]'):
            price_PreAfter = driver.find_element("xpath",'//div[@class = "price_PreAfter"]')
            print(f"After Hours:     {price_PreAfter.text}\n")
        
        elm_list = driver.find_elements(By.XPATH, '//span[@class = "summaryValue-DS-EntryPoint1-2"]')
        if len(elm_list) > 1:
            target = elm_list[0].text.replace('USD', '')
            print(f"1y Target Est =  {target}")
            print(f"Price Volatility: {elm_list[1].text}")
        
        try:
            sibling_element = driver.find_element(By.XPATH, "//span[@title='Industry Recommendation']/following-sibling::*[1]")                                       
            print(f"Recommendation:   {sibling_element.text}\n")
        except:
            pass
            
    driver.quit()
        
if __name__ == "__main__":
    main()