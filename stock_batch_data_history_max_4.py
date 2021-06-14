#!/usr/bin/env python
"""
Firefox version: 73.0 (64-bit)
"""
#import xml.etree.ElementTree as ET
#import urllib2
import requests, urllib3, sys
import re
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
from datetime import date
import sys
# from bs4 import BeautifulSoup as bs
from selenium import webdriver

class Logger(object):
    def __init__(self):
        today = date.today()
        downloadPath = "C:\\Users\\William Chang\\Downloads\\Data"
        d1 = today.strftime("%m%d%Y")
        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report_"+ d1 + "txt" , "a")

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
    def __init__(self, stock_name, downloadPath, stock_or_fund):
        self.stock_name = stock_name
        print ("")
#        print ("Processing " + self.stock_name.upper() +" stock data")
        self.downloadPath = downloadPath
        self.stock_or_fund = stock_or_fund
        delay = 0
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", self.downloadPath)
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
        options.add_argument("--headless")

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

        url_stock = "https://finance.yahoo.com/quote/"+stock_name.upper()+"?p="+stock_name.upper()
        time.sleep(delay + 1)

#        time.sleep(delay + 1)
        while True:
            time.sleep(delay + 1)
            try:
                time.sleep(delay + 1)
                driver.get(url_stock)
                driver.implicitly_wait(10)
                # stock_elm = driver.find_element_by_id('yfin-usr-qry')
                # time.sleep(delay + 1)
#                stock_elm.send_keys((self.stock_name.upper()) + (Keys.ENTER))
                time.sleep(delay + 1)
#                print (self.stock_name.upper(), str(driver.current_url))
                if self.stock_name.upper() in str(driver.current_url):
                    break

            except:
                 print ("Yahoo page slow, will reloop!")

        # 
        # print ("Display Historical Data Page")
        # try:
        #     elm = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Historical Data')]"))).click()
        # except TimeoutException:
        #     pass
        # 
        # time.sleep(delay + 1)
        # 
        # input_elm = driver.find_element_by_xpath("//span[@class='C($linkColor) Fz(14px)']")
        # print ("click at input button")
        # input_elm.click()
        # time.sleep(delay + 1)
        # 
        # elm = driver.find_element_by_xpath("//li[4]/button[@data-value='MAX']")
        # print ("click at max")
        # elm.click()
        # time.sleep(delay + 1)
        # 
        # print ("clikc at Apply")
        # try:
        #     elm = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Apply"]'))).click()
        # except TimeoutException:
        #     pass
        # 
        # time.sleep(delay + 3)
        # 
        # a_elm = driver.find_element_by_xpath("//a[@class = 'Fl(end) Mt(3px) Cur(p)']")
        # print ("click at download link")
        # a_elm.click()
        # time.sleep(delay + 3)
        print ('\n')

        print ("Display Summary Page")
        while True:
#            time.sleep(delay + 1)
            try:
                time.sleep(delay + 1)
                driver.get(url_stock)
                driver.implicitly_wait(10)
                time.sleep(delay + 1)
#                print (self.stock_name.upper(), str(driver.current_url))
                if self.stock_name.upper() in str(driver.current_url):
                    break

            except:
#                driver.get(url)
#                driver.delete_all_cookies()
                print ("Yahoo slow, will reloop!")
                pass

        print ('Current Price:   %s' % (driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]').text))

        if self.stock_or_fund == 'stock':
            try:
                elm = driver.find_element_by_xpath("//div[@class= 'Fw(b) Fl(end)--m Fz(s) C($primaryColor']").text
                print (elm, end = '\n')
            except Exception:
                pass



            table_elm = driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody')
            list_elm = table_elm.find_elements_by_xpath('//*/tr[2]')

            for elm in list_elm:
                if 'Beta (5Y Monthly)' in elm.text:
                    print( elm.text)
                    
            list_elm = table_elm.find_elements_by_xpath('//*/tr[8]')

            for elm in list_elm:
                if '1y Target Est' in elm.text:
                    print (elm.text)
            print (driver.find_element_by_xpath('//*[@id="chrt-evts-mod"]/div[2]/div[1]/span[1]/span').text)
#                    //*[@id="quote-summary"]/div[2]/table/tbody/tr[8]/td[1]/span
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
    
    downloadPath = "C:\\Users\\William Chang\\Downloads\\Data"
    sys.stdout = Logger()
    # get_stock_data = get_historical_data("VTI",  downloadPath)
    # get_stock_data = get_historical_data("VIG",  downloadPath)
    # get_stock_data = get_historical_data("VYM",  downloadPath)
    # get_stock_data = get_historical_data("SCHD",  downloadPath)
    # get_stock_data = get_historical_data("vt",  downloadPath)
    # get_stock_data = get_historical_data("sdy",  downloadPath)
    # get_stock_data = get_historical_data("dvy",  downloadPath)

    with open("ETF.txt","r") as stock_input_file:
        stock_fund_names = stock_input_file.readlines()
#        print stock_fund_names

    for stock_fund_name in stock_fund_names:
        if len(stock_fund_name) < 2:
            continue

        print (("=") * len("Processing " + stock_fund_name.rstrip() +" data"))
        print ("Processing " + stock_fund_name.rstrip() +" data")
        print (("=") * len("Processing " + stock_fund_name.rstrip() +" data"))
        stock = re.search(('\(\w+\)'), stock_fund_name)
               
#            print is_stock
        if is_stock:
            if 'Fund' in stock_fund_name:
                stock_or_fund =  'Fund' 
            else:
                stock_or_fund = 'ETF'
        else:
            stock_or_fund ='stock'
#        print (stock.group())
        # time.sleep(10000)
        get_stock_data = get_historical_data(stock.group().rstrip().rstrip(')').lstrip('('),  downloadPath, stock_or_fund)


if __name__ == "__main__":
    main()
