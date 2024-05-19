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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from path import Path
from bs4 import BeautifulSoup
from lxml import html
import time
import re
import datetime
import shutil
import sys
from datetime import date
#from selenium_stealth import stealth
import random
import os
import logging
#from csv import DictReader

from dateutil.relativedelta import relativedelta
from datetime import date
#from cachetools import cached

Path(os.path.expanduser( '~' ) + "\\Documents\\Python Scripts").chdir()
downloadPath = os.path.expanduser( '~' ) + "\\Documents\\Python Scripts\\Tipranks"

print ("")

class Logger(object):

    def __init__(self):
        global downloadPath
        today = date.today()

        try:
            shutil.rmtree(downloadPath)
            # shutil.rmtree(downloadPath_pickle)
        except:
#            print("failed to remove")
            pass
        time.sleep(1)
        
        try:
            os.mkdir(downloadPath)
            # os.mkdir(downloadPath_pickle)
        except:
            pass
        # time.sleep(2)
        self.terminal = sys.stdout
        self.log = open(downloadPath +"\\Summary_Report_From_Tipranks_"+ today.strftime("%m%d%Y") + ".txt" , "a+")

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
        #self.options.add_argument("--headless")
        
        # disable the AutomationControlled feature of Blink rendering engine
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        #  
        # disable pop-up blocking
        self.options.add_argument('--disable-popup-blocking')
        #  
        # # start the browser window in maximized mode
        self.options.add_argument('--start-minimized')
        #self.options.add_argument('--start-maximized')
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
        self.driver.minimize_window()
        return(self.driver)
        
    # def quit(self):
    #     self.driver.quit()
        
def main():
 #   sys.stdout = Logger()
    def check_exists_by_xpath(driver, xpath):
        try:
            driver.find_element(By.XPATH, xpath)
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

            stock = stock.group().rstrip().rstrip(')').lstrip('(')
            msft_ticket = msft_ticket.group().rstrip().rstrip(']').lstrip('[')
            stock_Dictionary[stock] = [stock_fund_name.rstrip()[:-9]]
            
            stock_Dictionary[stock].append(stock_or_fund)
            stock_Dictionary[stock].append(msft_ticket)
            
    def extract_price(s, sub1, sub2):

        idx1 = s.index(sub1)
        idx2 = s.index(sub2)
        return(s[idx1 + len(sub1) + 1: idx2])
    
    def extract_price_3(s, sub1, sub2):

        idx1 = s.index(sub1)
        idx2 = s.index(sub2)
        return(s[idx1 + len(sub1): idx2 + 1])
    
    
    def extract_price_2(s, sub1):

        idx1 = s.index(sub1)
        return(s[idx1 + len(sub1):])
    
#     def fetch_Stock_Name(stock_Dictionary):
#         stock_fund_names =  [line for line in open("STOCK.txt", "r")]
#         for stock_fund_name in stock_fund_names:
#             if len(stock_fund_name) < 2 or "IGNOR" in stock_fund_name :
#                 continue
# 
#             stock = re.search(r'(\(\^\w+\))', stock_fund_name)
#             if stock is None:
#                 stock = re.search('\(\w+\)', stock_fund_name)
#                 msft_ticket = re.search('\[\w+\]', stock_fund_name)
# 
#             is_stock =  re.search("ETF|Fund",stock_fund_name)
# #            print is_stock
#             if is_stock:
#                 if 'ETF' in stock_fund_name:
#                     stock_or_fund =  'ETF'
#                 else:
#                     stock_or_fund = 'Fund'
#             else:
#                 stock_or_fund ='STOCK'
#             # print(stock_or_fund)
#             stock = stock.group().rstrip().rstrip(')').lstrip('(')
#             msft_ticket = msft_ticket.group().rstrip().rstrip(']').lstrip('[')
#             stock_Dictionary[stock] = [stock_fund_name.rstrip()[:-9]]
#             
#             stock_Dictionary[stock].append(stock_or_fund)
#             stock_Dictionary[stock].append(msft_ticket)

    logging.basicConfig(level=logging.INFO)
    driver = init_webdriver().driver_init()
    driver.get("https://www.tipranks.com/sign-in?redirectTo=%2Fsmart-portfolio%2Fwelcome")
    time.sleep(3)
#    driver.minimize_window()
    #actions = ActionChains(driver)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(5)
    
    #driver.find_element("xpath","//input[@name = 'email'").click()
    email_box = driver.find_element(By.XPATH,"//input[contains(@class, 'w12 py4 px3 radiimedium')]")
    email_box.click()
    email_box.send_keys("weipanchang@mail.com")
    
    password_box = driver.find_element(By.XPATH,"//input[contains(@type, 'password')]")
    password_box.click()
    password_box.send_keys("abcde12345")
    
    time.sleep(3)
    # password_box.send_keys(Keys.RETURN)
    signin_button = driver.find_element(By.XPATH,"//button[contains(@class, 'colorwhite w12 radiiround displayflex bgorange-light hoverBgorange h_px1 flexrcc fontSize6 fontWeightsemibold aligncenter w_px6 mt4 mb3 mobile_fontSize6 mobile_py3 mobile_h_pxauto mobile_mt5')]")
    
    signin_button.click()
    
    time.sleep(15)   
    #actions = ActionChains(driver)
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # time.sleep(1)
    
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(5)
    if not check_exists_by_xpath (driver, '/html/body/div[1]/div[2]/div[5]/div[2]/div[3]/div[2]/div[4]/div[1]/div[2]/table/tbody'):
        time.sleep(25)
#    try:
#        stock_table = driver.find_element(By.XPATH, '//tbody[@class="rt-tbody"]')
    if check_exists_by_xpath (driver, '/html/body/div[1]/div[2]/div[5]/div[2]/div[3]/div[2]/div[4]/div[1]/div[2]/table/tbody')  or check_exists_by_xpath (driver, '//tbody[contains(@class,"rt-tbody")]'):
#    if check_exists_by_xpath (driver, '//tbody[contains(@class,"rt-tbody")]'):
#        print("found")
#        stock_table = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[5]/div[2]/div[3]/div[2]/div[4]/div[1]/div[2]/table/tbody')
        stock_table = driver.find_element(By.XPATH, '//tbody[contains(@class,"rt-tbody")]')
        stock_table_html = stock_table.get_attribute('innerHTML')
        stock_table_html = stock_table_html.encode("utf-8")
        # print(stock_table_html)
        print("=======> Found Stock Table!! <======")   #/html/body/div[1]/div[2]/div[5]/div[2]/div[3]/div[2]/div[4]/div[1]
#    except:
    else:
        print("======> Stock Table Not Found!! <======")
        os.system("PAUSE")
        sys.exit("Fail to fetch table")
    driver.quit()
    
    soup = BeautifulSoup(stock_table_html, 'html.parser')
    soup = str(soup).split("><")
 #   soup = str(soup).replace("><", "\n")
    for i in soup:
        print (i)
    print(soup)
    # os.system("PAUSE")

    data_list = []
    for i in soup:
        if 'data-key' in i:
           print(i)
#           print (extract_price_2(i, 'data-key=\"')[:-1], end='\t')
           data_list.append(extract_price_2(i, 'data-key=\"')[:-1])
           
        if 'w_px2 ml3 alignstart">' in i:
#           print (extract_price(i, 'w_px2 ml3 alignstart">')[:-1], end='\t')
           data_list.append(extract_price_3(i, 'w_px2 ml3 alignstart">','</')[:-1])
#           w_px2 ml3 alignstart">    </
        if 'title="The Price now ' in i:
#            print (i)
#            print (extract_price(i, 'Currency in US Dollar\">', '<div class='))
            data_list.append(extract_price(i, 'Currency in US Dollar\">', '<div class='))
    print (data_list)  
    data_dict = {}
    for i in range(0, len(data_list), 3):
        data_dict[data_list[i]] = [(data_list[i + 1])]
        data_dict[data_list[i]].append(data_list[i + 2])
#    print (data_dict)   
    fetch_Stock_Name(stock_Dictionary:={})
    sys.stdout = Logger()
    
    for stock in stock_Dictionary.keys():
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"), end="\n")
        print( "1y Target Est = %s\n" % (data_dict[stock][1]))
        print("Recommedation:   %s\n" % (data_dict[stock][0]))
    

if __name__ == "__main__":
    main()