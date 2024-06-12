#!/usr/bin/env python
"""
Firefox version: 73.0 (64-bit)
"""
#import xml.etree.ElementTree as ET
#import urllib2
import requests, urllib3, sys
import re
from path import Path
import os
import holidays
import shutil
import random
import logging
from yahoo_fin import stock_info as si
import yfinance as yf
from openpyxl import load_workbook, Workbook

# from bs4 import BeautifulSoup
# import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
from datetime import date
# import sys
from selenium import webdriver
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\MSFT_Analysis"
Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
eXCEL_File = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Stock_2.xlsx"
        
stock = ""

class Logger(object):

    def __init__(self):
#        global downloadPath
        global stock
        today = date.today()
        #d1 = today.strftime("%m%d%Y")
        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report_From_Microsoft_"+ today.strftime("%m%d%Y") + ".txt" , "a+")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

class init_webdriver():
    def __init__(self):
#        global downloadPath
        global stock
#        stock_name = stock
        print ("")
#        print ("Processing " + self.stock_name.upper() +" stock data")
#        self.stock_or_fund = stock_or_fund
        self.delay = 0
        self.currentDateTime = datetime.datetime.now()
        self.date = self.currentDateTime.date()
        
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.dir", downloadPath)
        self.profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
        self.profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        self.profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
        self.profile.set_preference("browser.download.manager.focusWhenStarting", False)
        self.profile.set_preference("browser.download.manager.useWindow", False)
        self.profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        self.profile.set_preference("browser.download.manager.closeWhenDone", False)
        self.profile.set_preference("browser.cache.disk.enable", False)
        self.profile.set_preference("browser.cache.memory.enable", False)
        self.profile.set_preference("browser.cache.offline.enable", False)
        self.profile.set_preference("network.http.use-cache", False)
        self.desiredCapabilities = DesiredCapabilities.FIREFOX.copy()
        self.desiredCapabilities['firefox_profile'] = self.profile.encoded
        self.options = Options()
        
#        self.driver = webdriver.Firefox(capabilities=self.desiredCapabilities, options=self.options)

        #self.driver.set_page_load_timeout(50)
        #wait = WebDriverWait(self.driver, 200, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        
        #run in headless mode
        self.options.add_argument("--headless")
        
        # disable the AutomationControlled feature of Blink rendering engine
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        #  
        # disable pop-up blocking
        self.options.add_argument('--disable-popup-blocking')
        #  
        # # start the browser window in maximized mode
        self.options.add_argument('--start-maximized')
        #  
        # disable extensions
        self.options.add_argument('--disable-extensions')
        #  
        # disable sandbox mode
        self.options.add_argument('--no-sandbox')
        #  
        # disable shared memory usage
        self.options.add_argument('--disable-dev-shm-usage')
        
        # Step 3: Rotate user agents 
        user_agents = [
            # Add your list of user agents here
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        ]

        # select random user agent
        user_agent = random.choice(user_agents)
#        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        # pass in selected user agent as an argument
        self.options.add_argument(f'user-agent={user_agent}')
    def driver_init(self):
        self.driver = webdriver.Firefox(capabilities=self.desiredCapabilities, options=self.options)
        self.driver.set_page_load_timeout(50)
        return(self.driver)

        
def main():
#    global downloadPath
    global stock
    try:
        shutil.rmtree(downloadPath)
    except:
         pass
    time.sleep(2)
    try:
        os.mkdir(downloadPath)
    except:
        pass

    now_time = datetime.datetime.now().time()
    print("\nTime: ", now_time, "\n")

    logging.basicConfig(level=logging.INFO)
    driver = init_webdriver().driver_init()
    driver.get('https://www.msn.com/en-us/money/watchlist?ocid=winp1taskbar&duration=1M')
    time.sleep(1)
    def check_exists_by_css_selector(driver, css_selector):
        try:
            driver.find_element(By.CSS_SELECTOR,css_selector)
        except NoSuchElementException:
            return False
        return True
    def check_exists_by_classname(driver,classname):
        try:
            driver.find_element(By.CLASS_NAME,classname)
        except NoSuchElementException:
            return False
        return True
    
    def check_exists_by_xpath(driver,xpath):
        try:
            driver.find_element(By.XPATH,xpath)
        except NoSuchElementException:
            return False
        return True
    def check_exists_by_tag(driver,tag_name):
        try:
            driver.find_element(By.TAG_NAME,tag_name)
        except NoSuchElementException:
            return False
        return True
        
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
#            print is_stock
            if is_stock:
                if 'ETF' in stock_fund_name:
                    stock_or_fund =  'ETF'
                else:
                    stock_or_fund = 'Fund'
            else:
                stock_or_fund ='STOCK'
            # print(stock_or_fund)
            stock = stock.group().rstrip().rstrip(')').lstrip('(')
            msft_ticket = msft_ticket.group().rstrip().rstrip(']').lstrip('[')
            stock_Dictionary[stock] = [stock_fund_name.rstrip()[:-9]]
            
            stock_Dictionary[stock].append(stock_or_fund)
            stock_Dictionary[stock].append(msft_ticket)

    fetch_Stock_Name(stock_Dictionary:={})
    sys.stdout = Logger()
    for stock in stock_Dictionary.keys():

#        sys.stdout = Logger()
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))

        msft_ticket = stock_Dictionary[stock][2]

        url_stock = "https://www.msn.com/en-us/money/watchlist?ocid=winp1taskbar&duration=1M&id="+ msft_ticket+"&l3=L3_Earnings"
        driver.get(url_stock)
        driver.implicitly_wait(1)

        print ("Display Earning Page... \n\n")
        time.sleep(2)
        while True:
            if check_exists_by_xpath(driver, '/html/body/div[1]/div[1]/div/div[5]/div[2]/div/div[1]/div/div[3]/div[2]/div/div/button[4]/span'):
                driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div[5]/div[2]/div/div[1]/div/div[3]/div[2]/div/div/button[4]/span').click()
                break

            if check_exists_by_xpath(driver, '//button[@title="Earnings"]'):
                driver.find_element(By.XPATH,'//button[@title="Earnings"]').click() 
                break

        time.sleep(1)
        
        while True:
            if check_exists_by_xpath(driver, '//div[@class= "mainPrice color_red-DS-EntryPoint1-1"]'):
                print ('Current Price:   %s' % (driver.find_element("xpath",'//div[@class= "mainPrice color_red-DS-EntryPoint1-1"]').text))
                break
            elif check_exists_by_xpath(driver,'//div[@class= "mainPrice color_green-DS-EntryPoint1-1"]'):
                print ('Current Price:   %s' % (driver.find_element("xpath",'//div[@class= "mainPrice color_green-DS-EntryPoint1-1"]').text))
                break
            elif check_exists_by_xpath(driver,'//div[@class= "mainPrice color_nochange-DS-EntryPoint1-1"]'):
                print ('Current Price:   %s' % (driver.find_element("xpath",'//div[@class= "mainPrice color_nochange-DS-EntryPoint1-1"]').text))
                break
            else:
                pass
            
        if check_exists_by_xpath(driver, '//div[@class = "price_PreAfter"]'):
            print("After Hours:     %s\n" % (driver.find_element("xpath",'//div[@class = "price_PreAfter"]').text))
        
        time.sleep(1)    
        elm_list = driver.find_elements(By.XPATH,'//span[@class = "summaryValue-DS-EntryPoint1-2"]')
        target = elm_list[0].text.replace('USD','')
        print( "1y Target Est = %s\n" % (target))
        time.sleep(5)
        print("Recommedation:    %s\n" % (driver.find_element("xpath",'//h2[@class="suggestion-DS-EntryPoint1-1"]').text))
        print("Price Volatility: %s\n" % elm_list[1].text)
        
        # url_stock = "https://www.msn.com/en-us/money/watchlist?ocid=winp1taskbar&duration=1M&id="+ msft_ticket
        # driver.get(url_stock)
        # 
        # print ("Display Summary Page... \n")
        # time.sleep(1)
        
        # elm_list = driver.find_element(By.XPATH,'//div[@class = "factsRowValue-DS-EntryPoint1-1"]')
        # previous = elm_list.text
        # print( "Previous Close = %s\n" % (previous))
        
        time.sleep(1)
    driver.quit()
        
if __name__ == "__main__":
    main()
