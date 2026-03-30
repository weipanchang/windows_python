#!/usr/bin/env python
"""
Firefox version: 73.0 (64-bit)
"""
import requests, urllib3, sys
import re
from path import Path
import os
import holidays
import shutil
import random
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import datetime
from datetime import date
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\data"
Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
profile_path = os.path.expanduser( '~' ) + r"\\AppData\Roaming\\Mozilla\Firefox\\Profiles\\mg91we5v.default-release"
stock = ""

class Logger(object):

    def __init__(self):
#        global downloadPath
        global stock
        today = date.today()
        #d1 = today.strftime("%m%d%Y")
        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report__From_Yahoo_"+ today.strftime("%m%d%Y") + ".txt" , "a+")

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

        self.delay = 0
        self.currentDateTime = datetime.datetime.now()
        self.date = self.currentDateTime.date()
        self.options = Options()
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", downloadPath)
        self.options.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
        self.options.set_preference("browser.helperApps.alwaysAsk.force", False)
        self.options.set_preference("browser.download.manager.alertOnEXEOpen", False)
        self.options.set_preference("browser.download.manager.focusWhenStarting", False)
        self.options.set_preference("browser.download.manager.useWindow", False)
        self.options.set_preference("browser.download.manager.showAlertOnComplete", False)
        self.options.set_preference("browser.download.manager.closeWhenDone", False)
        self.options.set_preference("browser.cache.disk.enable", False)
        self.options.set_preference("browser.cache.memory.enable", False)
        self.options.set_preference("browser.cache.offline.enable", False)
        self.options.set_preference("network.http.use-cache", False)
        #self.options.binary_location = ("C:\Program Files\Mozilla Firefox")
        self.desiredCapabilities = DesiredCapabilities.FIREFOX.copy()
        #self.service = Service(r"'~'+'\.cache\selenium\geckodriver\win64\0.36.0'")

        # firefox_profile = FirefoxProfile()
        # firefox_profile.set_preference("javascript.enabled", False)
        # options.profile = firefox_profile

        #run in profile
        # self.options.add_argument("-profile")
        # self.options.add_argument(profile_path)

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
        
       #  Rotate user agents 
       #  user_agents = [
       #      # Add your list of user agents here
       #      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
       #      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
       #      'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
       #      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
       #      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
       #      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
       #      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
       #      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
       #  
       #  
       #  select random user agent
       # user_agent = random.choice(user_agents)
       # self.options.add_argument(f'user-agent={user_agent}')
    def driver_init(self):
        self.driver = Firefox(service=FirefoxService(GeckoDriverManager().install()), options=self.options)
#        self.driver = webdriver.Firefox(options=self.options)
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

    driver = init_webdriver().driver_init()
    try:
        driver.get('https://finance.yahoo.com/')
    except:
        pass
    time.sleep(1)
    driver.minimize_window()
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
    sys.stdout = Logger()
    fetch_Stock_Name(stock_Dictionary:={})
    for stock in stock_Dictionary.keys():

#        sys.stdout = Logger()
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print("\n")
        
        url_stock = "https://finance.yahoo.com/quote/"+ stock.upper()
        # driver.get(url_stock)
        # 
        # driver.implicitly_wait(1)
#       delay = 1
        while True:
            try:
                driver.get(url_stock)
                driver.implicitly_wait(1)
                time.sleep(1)
                print(str(driver.current_url))
                if stock.upper() in str(driver.current_url):
                    break
            except:
                print ("Yahoo page slow, will reloop!", end=" ")
                pass
        time.sleep(1)



        if check_exists_by_xpath(driver, "//span[@data-testid='qsp-price']"):
            print ('\nCurrent Price:   %s' % (driver.find_element(By.XPATH,"//span[@data-testid='qsp-price']").text))  
        
        if check_exists_by_xpath(driver, "//fin-streamer[@data-field='regularMarketPreviousClose']"):
            print("\nPrevious   :     %s\n" % (driver.find_element(By.XPATH,"//fin-streamer[@data-field='regularMarketPreviousClose']").text))

        if check_exists_by_xpath(driver, '//span[@data-testid="qsp-post-price"]'):
            print ('After Hours Price:   %s\n' % (driver.find_element(By.XPATH,'//span[@data-testid="qsp-post-price"]').text))
        try:
             Open = driver.find_element(By.XPATH,"//fin-streamer[@data-field='regularMarketOpen']").text        
        except:
              Open = driver.find_element(By.XPATH,'/html/body/div[2]/main/section/section/section/section/div[2]/ul/li[2]/span[2]/fin-streamer').text
        print("\nOpen =  %.2f" %float(Open.replace(',','')))
        print()

        Range_elm = driver.find_element(By.XPATH,"//fin-streamer[@data-field='regularMarketDayRange']").text

        Low, High  = Range_elm.split(' - ')[0], Range_elm.split(' - ')[1]
        print ("LOW = %s, HIGH = %s\n" %(Low, High))
        
#        from selenium import webdriver

# # Assuming driver is a webdriver instance and elem references an existing element
# next_sibling_button = driver.find_element_by_xpath("//button[@id='submit-button']/following-sibling::div[1]")
# 
# # Do something with next_sibling_button
#         
# 
# 
# # Assuming driver is a webdriver instance and elem references an existing element
# next_sibling_lambda = (lambda element: element.find_element_by_xpath("following-sibling::*[1]"))(elem)
# 
# # Do something with next_sibling_lambda

        Ex_Dividend_Label = driver.find_element(By.XPATH,"//span[@title='Ex-Dividend Date']")
        Ex_Dividend = (lambda element: element.find_element(By.XPATH,"following-sibling::*[1]"))(Ex_Dividend_Label).text

        print ("Ex-Dividend Date = %s\n" %Ex_Dividend)

        beta_Label = driver.find_element(By.XPATH,"//span[@title='Beta (5Y Monthly)']")
        beta = (lambda element: element.find_element(By.XPATH,"following-sibling::*[1]"))(beta_Label).text

        print( "Beta (5Y Monthly) = ", beta)
        
        target = driver.find_element(By.XPATH,"//fin-streamer[@data-field='targetMeanPrice']").text

        print( "\n1y Target Est =========> ", target)
        print("")
        
        PE_Ratio_Section = driver.find_element(By.XPATH,"//span[@title='PE Ratio (TTM)']")
        PE_Ratio = (lambda element: element.find_element(By.XPATH,"following-sibling::*[1]"))(PE_Ratio_Section).text
        print ("PE_Ratio ( Smaller is better ) = %s" %PE_Ratio)
        
        EPS_Section = driver.find_element(By.XPATH,"//span[@title='EPS (TTM)']")
        EPS=(lambda element: element.find_element(By.XPATH,"following-sibling::*[1]"))(EPS_Section).text
        print ("EPS ( > 1 is better ) ====       %s" %EPS)

        Volume = driver.find_element(By.XPATH,"//fin-streamer[@data-field='regularMarketVolume']").text.replace(",","") 
        Avg_Volume = driver.find_element(By.XPATH,"//fin-streamer[@data-field='averageVolume']").text.replace(",","") 
        try:
            print ("\nVolume over Average = %s\n" %round(float(Volume)/float(Avg_Volume),2))
        except:
            pass
        print ("EOT")
        print ('\n' *2)

    driver.quit()
        
if __name__ == "__main__":
    main()
