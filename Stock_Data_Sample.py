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
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
import time
# from bs4 import BeautifulSoup as bs
from selenium import webdriver

class get_historical_data():

    #def __init__(self, stock_name, startDate, endDate, downloadPath):
    def __init__(self, stock_name):
        self.stock_name = stock_name
        print ("")
#        print "Processing " + self.stock_name.upper() +" stock history data"
        # self.downloadPath = downloadPath
        # self.stock_or_fund = stock_or_fund
        delay = 0
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
#        profile.set_preference("browser.download.dir", self.downloadPath)
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
        driver.set_page_load_timeout(50)
        wait = WebDriverWait(driver, 100, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
#        url = "https://finance.yahoo.com/quote/" + self.stock_name + "?p=" + self.stock_name + "&.tsrc=fin-srch"
        self.url = "https://finance.yahoo.com"
        self.url_stock = "https://finance.yahoo.com/quote/"+self.stock_name.upper()+"?p="+self.stock_name.upper()
        timeout = 5
        try:
            request = requests.get(self.url, timeout=timeout)
            print("Connected to the Internet")
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection.\n\n")
            time.sleep(self.delay + 3)
            self.quit_driver()
            sys.exit()

        while True:
            try:
#                driver = webdriver.Firefox(capabilities=desiredCapabilities, options=options)
                driver.get(self.url)
                driver.delete_all_cookies()
                driver.implicitly_wait(15)
#                time.sleep(delay + 1)
                print ("Yahoo finance Page is loaded")
                if 'finance' in str(driver.current_url):
                    break
            except TimeoutException:
                pass

        self.url_stock = "https://finance.yahoo.com/quote/"+self.stock_name.upper()+"?p="+self.stock_name.upper()
        time.sleep(delay + 1)

        while True:
            time.sleep(delay + 1)
            try:
                time.sleep(delay + 1)
                driver.get(self.url_stock)
                driver.implicitly_wait(15)

                time.sleep(delay + 1)

                if self.stock_name.upper() in str(driver.current_url):
                    break

            except TimeoutException:

                print ("Yahoo page slow, will reloop!")

        print ("Process " + self.stock_name + "\n\n")
        print ("Display Historical Data Page" + "\n")
        try:
#//*[@id="quote-nav"]/ul/li[6]/a            
            elm = driver.find_element_by_xpath("//span[contains(text(), 'Historical Data')]")
#            elm = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='quote-nav']/ul/li[6]/a"))).click()
        except TimeoutException:
            pass
        elm.click()
        time.sleep(delay + 1)
        input_elm = driver.find_element_by_xpath("//span[@class='C($linkColor) Fz(14px)']")
        print ("click at input button")
        input_elm.click()
        time.sleep(delay + 1)

        try:
            elm = driver.find_element_by_xpath("//button[@class='Py(5px) W(45px) Fz(s) C($tertiaryColor) Cur(p) Bd Bdc($seperatorColor) Bgc($lv4BgColor) Bdc($linkColor):h Bdrs(3px)' and @data-value='3_M']")
        except:
            time.sleep(delay + 1)
            elm = driver.find_element_by_xpath("//button[@class='Py(5px) W(45px) Fz(s) C($tertiaryColor) Cur(p) Bd Bdc($seperatorColor) Bgc($lv4BgColor) Bdc($linkColor):h Bdrs(3px)' and @data-value='3_M']")    
        print ("Select 3 Months Quote")
        elm.click()
        time.sleep(delay + 1)

        print ("clikc at Apply")
        try:
            elm = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Apply"]'))).click()
        except TimeoutException:
            pass

        time.sleep(delay + 3)
        quote_table = driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody')
        quote_lists = quote_table.find_elements_by_tag_name("tr")
#        print(" Date", '\t',"Open", '\t',"High", '\t',"Low", '\t',"Close", '\t',"Adj", '\t',"Vol")
        for quote_list in quote_lists:
            try:
                quotes= quote_list.find_elements_by_tag_name("td")
                Date, Open, High, Low, Close, Adj, Vol = quotes[0].text, quotes[1].text,quotes[2].text,quotes[3].text,quotes[4].text,quotes[5].text,quotes[6].text
    
                print(Date,'\t', Open, '\t',High, '\t',Low, '\t',Close, '\t',Adj, '\t',Vol)
            except:
                continue
        
        driver.quit()
        
        print("\n")
        print ("Display Summary Page, please wait.....")
        driver = webdriver.Firefox(capabilities=desiredCapabilities, options=options)
        driver.set_page_load_timeout(50)
        wait = WebDriverWait(driver, 100, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        driver.get(self.url)
        driver.delete_all_cookies()
        driver.implicitly_wait(15)
        print("\n\n")


        while True:
#            time.sleep(delay + 1)
            try:
                time.sleep(delay + 1)
                driver.get(self.url_stock)
                driver.implicitly_wait(15)
                time.sleep(delay + 1)
#                print (self.stock_name.upper(), str(driver.current_url))
                if self.stock_name.upper() in str(driver.current_url):
                    break
            except:
                driver.get(url)
                driver.delete_all_cookies()

                print ("Yahoo slow, will reloop!")

        print ('Current Price:   %s' % (driver.find_element_by_xpath("//*[@class='Fw(b) Fz(36px) Mb(-4px) D(ib)']").get_attribute('value').replace(',', '')))

        try:
            elm = driver.find_element_by_xpath("//div[@class= 'Fw(b) Fl(end)--m Fz(s) C($primaryColor']").text

        except Exception:
            pass
        print ("%s," % elm) 

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
        print ('\n' *3) 

        driver.quit()

def main():
    
    get_stock_data = get_historical_data("AAPL")
    get_stock_data = get_historical_data("GOOG")

if __name__ == "__main__":
    main()
