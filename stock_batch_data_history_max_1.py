#!/usr/bin/env python
"""
Firefox version: 73.0 (64-bit)
"""
#import xml.etree.ElementTree as ET
#import urllib2
import requests, urllib3, sys
import re
import os
import holidays
import shutil

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
import time
import datetime
from datetime import date
import sys
# from bs4 import BeautifulSoup as bs
from selenium import webdriver
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\data"
#short_cut_url = "https://finance.yahoo.com/quote/AVGO/history?period1=1249516800&period2=1626307200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
stock = ""
#home_dir = os.path.expanduser( '~' )

class Logger(object):

    def __init__(self):
        global downloadPath
        global stock
        today = date.today()
        d1 = today.strftime("%m%d%Y")
        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report_"+ d1 + ".txt" , "a+")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

class get_historical_data():

    #def __init__(self, stock_name, startDate, endDate, downloadPath):
    def __init__(self, stock_or_fund):
        global downloadPath
        global stock
#        stock_name = stock
        print ("")
#        print ("Processing " + self.stock_name.upper() +" stock data")
        self.stock_or_fund = stock_or_fund
        delay = 0
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", downloadPath)
        profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
        profile.set_preference("browser.download.manager.focusWhenStarting", False)
        profile.set_preference("browser.download.manager.useWindow", False)
        profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        profile.set_preference("browser.download.manager.closeWhenDone", False)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        desiredCapabilities = DesiredCapabilities.FIREFOX.copy()
        desiredCapabilities['firefox_profile'] = profile.encoded
        options = Options()
#        options.add_argument("--headless")

        driver = webdriver.Firefox(capabilities=desiredCapabilities, options=options)

        driver.set_page_load_timeout(10)
        wait = WebDriverWait(driver, 100, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
#        url = "https://finance.yahoo.com/quote/" + self.stock_name + "?p=" + self.stock_name + "&.tsrc=fin-srch"

        url = "https://finance.yahoo.com"
        while True:
            try:
                driver.get(url)
                driver.delete_all_cookies()
                driver.implicitly_wait(10) # seconds
                time.sleep(delay + 1)
                print ("Yahoo finance Page is loaded")
                if 'finance' in str(driver.current_url):
                    break
            except TimeoutException:
                pass

        url_stock = "https://finance.yahoo.com/quote/"+stock.upper()+"?p="+stock.upper()
    #     time.sleep(delay + 1)
    # 
    #     while True:
    #         time.sleep(delay + 1)
    #         try:
    #             time.sleep(delay + 1)
    #             driver.get(url_stock)
    #             driver.implicitly_wait(10)
    #             time.sleep(delay + 1)
    # #            print (stock_name.upper(), str(driver.current_url))
    #             if stock.upper() in str(driver.current_url):
    #                 break
    # 
    #         except:
    #              print ("Yahoo page slow, will reloop!")

        #
        print ("Retrieving Historical Data ")

        ts = datetime.datetime.strptime(str(date),"%Y-%m-%d")

#        tuple = element.timetuple()
        timestamp = str(int(time.mktime(ts.timetuple())))
        # print (timestamp)
        # print (date)
        url_history = "https://finance.yahoo.com/quote/" + stock + "/history?period1=00&period2=" + timestamp +"&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
#        url_history = "https://finance.yahoo.com/quote/" + stock + "/history?period1=00&period2=1626480000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
        while True:
            time.sleep(delay + 1)
            try:
                time.sleep(delay + 1)
                driver.get(url_history)
                driver.implicitly_wait(5)
                if stock.upper() in str(driver.current_url):
                    break
            except:
                 print ("Yahoo page slow, will reloop!")

        print ("clikc at Apply")
        try:
            elm = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Apply"]'))).click()
        except TimeoutException:
            pass

        time.sleep(delay + 3)

        a_elm = driver.find_element_by_xpath("//a[@class = 'Fl(end) Mt(3px) Cur(p)']")
        print ("click at download link")
        a_elm.click()
        time.sleep(delay + 3)
        print ('\n')

#        if stock[1:] not in ['XAX', 'IXIC', 'DJI', 'GSPC', 'NYA']:

        print ("Display Summary Page")
#        print(stock.upper(), str(driver.current_url))
#        time.sleep(10000000)
        while True:
            try:
                driver.get(url_stock)
                driver.implicitly_wait(5)
                time.sleep(delay + 1)

                if stock.upper() in str(driver.current_url):
                    break

            except:
                print ("Yahoo slow, will reloop!")
                pass

        print ('Current Price:   %s' % (driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]').text))

        if self.stock_or_fund == 'stock':
            try:
                elm = driver.find_element_by_xpath("//div[@class= 'Fw(b) Fl(end)--m Fz(s) C($primaryColor']").text
                print (elm, end = '\n')
            except Exception:
                pass

            Current_price = driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]').text

            Open = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span').text
            print("Open =  %.2f" %float(Open))

            Range_elm = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]').text
            Low, High  = Range_elm.split(' - ')[0], Range_elm.split(' - ')[1]
            print ("LOW = %s, HIGH = %s" %(Low, High))

            Volume_elm = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span').text
            Volume_elm = Volume_elm.replace(',', '')
            print("Volume =  %d" %int(Volume_elm))

            weekno = datetime.datetime.today().weekday()
            north_america = holidays.US()
#                date = currentDateTime.date()

            Day_of_today = date.strftime("%m-%d-%Y")
#                print(Date_today)
            if weekno < 5 and (Day_of_today not in north_america):
                current_time = datetime.datetime.now()
                open_time = current_time.replace(hour=9, minute=15, second=0, microsecond=0)
#                    current_time = datetime.datetime.now().time()
                # print(current_time)
                if (current_time > open_time):
#                    if (int(str(current_time.hour)) > 8):
                # with open(downloadPath +"\\" + stock.upper() + '.csv', 'r') as f:
                #     for line in f:
                #         pass
                #     last_line = line
                # last_date = last_line.split(',')
                # if last_date != str(ts)[:10]:
                    
                
                    with open(downloadPath +"\\" + stock.upper() + '.csv', 'a') as file:
#                       writer = csv.writer(file)
                        last_row = ['\n',str(ts)[:10], ',', Open, ',', High, ',' , Low, ',', Current_price, ',', Current_price, ',', Volume_elm]
                        file.writelines(last_row)

#               Search Beta Value
            table_elm = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody')
            list_elm = table_elm.find_elements_by_xpath('//*/tr[2]')

            for elm in list_elm:
                if 'Beta (5Y Monthly)' in elm.text:
                    print( elm.text)

#               Search One year Target Estimate Value
            list_elm = table_elm.find_elements_by_xpath('//*/tr[8]')

            for elm in list_elm:
                if '1y Target Est' in elm.text:
                    print (elm.text)
                    
#                Print bullish or bearish
            try:

                 print ("bullish or bearish: ==> %s" %(driver.find_element_by_xpath('//html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[1]/div/div[3]/div[2]/div[1]/span[1]/span').text))
            except:
                print("bullish or bearish not found")
                
            EPS =  driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]/span').text
            print ("EPS ( > 1 is better ) = %s" %EPS)
            
            PE_Rato = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]/span').text
            print ("PE_Rato ( Smaller is better ) = %s" %PE_Rato)
        else:

            table_elm = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody')
            list_elm = table_elm.find_elements_by_xpath('//*/tr[6]')

            for elm in list_elm:
                if 'Beta' in elm.text:
                   print (elm.text)

            table_elm = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody')
            list_elm = table_elm.find_elements_by_xpath('//*/tr[2]')
            for elm in list_elm:

                if 'Beta' in elm.text:
                   print (elm.text)

            if stock_or_fund == 'ETF':
                print (driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[1]/span').text, end ='   ')
                print (driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/span').text)

        print ('\n' *3)
        driver.quit()

def main():
    global downloadPath
    global stock
    try:
        shutil.rmtree(downloadPath)
    except:
         pass
    time.sleep(2)
    os.mkdir(downloadPath)

    sys.stdout = Logger()

    now_time = datetime.datetime.now().time()
    print("\nTime: ", now_time, "\n")

    # with open("STOCK.txt","r") as stock_input_file:
    #     stock_fund_names = stock_input_file.readlines()
    stock_fund_names =  [line for line in open("STOCK.txt", "r")]
#        print stock_fund_names

    for stock_fund_name in stock_fund_names:
        if len(stock_fund_name) < 2 or "IGNOR" in stock_fund_name :
            continue

        print (("=") * len("Processing " + stock_fund_name.rstrip() +" data"))
        print ("Processing " + stock_fund_name.rstrip() +" data")
        print (("=") * len("Processing " + stock_fund_name.rstrip() +" data"))
#        stock = re.search('\(\w+\)', stock_fund_name)
        stock = re.search(r'(\(\^\w+\))', stock_fund_name)
        if stock is None:
            stock = re.search('\(\w+\)', stock_fund_name)
        is_stock =  re.search("ETF|Fund",stock_fund_name)
#            print is_stock
        if is_stock:
            if 'Fund' in stock_fund_name:
                stock_or_fund =  'Fund'
            else:
                stock_or_fund = 'ETF'
        else:
            stock_or_fund ='stock'
#        print (stock.group())
        stock = stock.group().rstrip().rstrip(')').lstrip('(')
#        get_stock_data = get_historical_data(stock.group().rstrip().rstrip(')').lstrip('('),  downloadPath, stock_or_fund)
        get_stock_data = get_historical_data(stock_or_fund)

if __name__ == "__main__":

    main()
