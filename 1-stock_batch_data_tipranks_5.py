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

#         try:
#             shutil.rmtree(downloadPath)
#             # shutil.rmtree(downloadPath_pickle)
#         except:
# #            print("failed to remove")
#             pass
#         time.sleep(1)
#         
#         try:
#             os.mkdir(downloadPath)
#             # os.mkdir(downloadPath_pickle)
#         except:
#             pass
#         # time.sleep(2)
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
        #self.my_proxy = "45.190.170.254:999"
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
        #self.desiredCapabilities['proxy'] = {"proxyType": "MANUAL", "httpProxy": self.my_proxy, "ftpProxy": self.my_proxy,"sslProxy": self.my_proxy}
        self.options = Options()
        
        #self.driver = webdriver.Firefox(capabilities=self.desiredCapabilities, options=self.options)

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
        # options.add_argument('--start-maximized')
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
 #   sys.stdout = Logger()
    
    def check_exists_by_xpath(xpath):
        try:
            driver.find_element(By.XPATH,xpath)
            #driver.find_element_by_xpath(driver, xpath)
        except NoSuchElementException:
            return False
        return True
    
    def extract_price(s, n, sub2):

        idx2 = s.index(sub2)
        return(s[3: idx2])
    
    def extract_price_3(s, sub1, sub2):
    
        idx1 = s.index(sub1)
        idx2 = s.index(sub2)
        return(s[idx1 + len(sub1): idx2])
    
    
    # def extract_price_2(s, sub1):
    # 
    #     idx1 = s.index(sub1)
    #     return(s[idx1 + len(sub1):])
    
    def fetch_Stock_Name(stock_Dictionary):
        stock_fund_names =  [line for line in open("STOCK.txt", "r")]
#        stock_fund_names =  [line for line in open("STOCK-01.txt", "r")]
        
        for stock_fund_name in stock_fund_names[10:15]:
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
      
    logging.basicConfig(level=logging.INFO)
    driver = init_webdriver().driver_init()
    #driver.minimize_window() 
    #driver = init_webdriver().driver
    driver.get("https://www.tipranks.com/sign-in?redirectTo=%2Fsmart-portfolio%2Fwelcome")
    time.sleep(3)
    #actions = ActionChains(driver)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(3)
    
    #driver.find_element("xpath","//input[@name = 'email'").click()
    email_box = driver.find_element(By.XPATH,"//input[contains(@class, 'w12 py4 px3 radiimedium')]")
    email_box.click()
    email_box.send_keys("weipanchang@aol.com")
    
    password_box = driver.find_element(By.XPATH,"//input[contains(@type, 'password')]")
    password_box.click()
    password_box.send_keys("abcde12345")
    
    #signin_button = driver.find_element(By.XPATH,"colorwhite w12 radiiround displayflex bgorange-light hoverBgorange h_px1 flexrcc fontSize6 fontWeightsemibold aligncenter w_px6 mt4 mb3 mobile_fontSize6 mobile_py3 mobile_h_pxauto mobile_mt5')]")
    signin_button = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/form/button")
    
    signin_button.click()
    
    time.sleep(10)   
    #actions = ActionChains(driver)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(3)

    #stock_input_box =  driver.find_element(By.XPATH,"//input[@id='react-select-2-input']")
    sys.stdout = Logger()                                    
    fetch_Stock_Name(stock_Dictionary:={})
    for stock in stock_Dictionary.keys():
    
#        sys.stdout = Logger()
        print("\n")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print ("Processing " + stock_Dictionary[stock][0] +" data")
        print (("=") * len("Processing " + stock_Dictionary[stock][0] +" data"))
        print("\n")
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(15)
        # if check_exists_by_xpath('//div[@class="Card__CardHeader-sc-1s2p2gv-1 a__sc-3vtlsk-1 givWLU cVIXeq"]'):
        #     driver.find_element(By.XPATH,'//button[@class="Button__StyledButton-a1qza5-0 fLZgds"]').click()
        # stock_input_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='react-select-2-input']")))
        # stock_input_box.click()
        # time.sleep(1)
        # stock_input_box.clear()
        # time.sleep(1)
        # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        # time.sleep(1)
        # 
        # stock_input_box.send_keys(stock)
        # time.sleep(3)
        # stock_input_box.send_keys(Keys.ENTER)

        # stock_input_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='react-select-2-input']")))
        # stock_input_box.click()

        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        stock_path = "https://www.tipranks.com/stocks/" + stock + "/forecast"
        driver.get(stock_path)
        time.sleep(5)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(6)
 
        if check_exists_by_xpath('//div[@class="w12 p0   displayflex positionrelative grow1"]'):

            try:
    #           driver.find_element(By.XPATH,'//*[@id="tr-stock-page-content"]')
    #           /html/body/div[2]/div[2]/div[4]/div[3]/div[1]/div[1]/div[5]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div[1]
                frame = driver.find_element(By.XPATH,'//*[@id="tr-stock-page-content"]')
    #            print("Found")
            except NoSuchElementException:
                print("Frame NOT Found")
                sys.exit()
        else:
            sys.exit() 
        time.sleep(3)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        #os.system("PAUSE")
        
        if check_exists_by_xpath('//div[@class="flexccc    mt3 displayflex colorpale shrink0 lineHeight2 fontSize2 ml2 ipad_fontSize3"]'):
            
            element = frame.find_element(By.XPATH,'//div[@class="flexccc    mt3 displayflex colorpale shrink0 lineHeight2 fontSize2 ml2 ipad_fontSize3"]')
        
        if check_exists_by_xpath('//div[@class="flexccc    mt3 displayflex colorpurple-dark shrink0 lineHeight2 fontSize2 ml2 ipad_fontSize3"]'):
            
            element = frame.find_element(By.XPATH,'//div[@class="flexccc    mt3 displayflex colorpurple-dark shrink0 lineHeight2 fontSize2 ml2 ipad_fontSize3"]')
        try:
            element.click()
        except:
            sys.exit()
        value = str((element.text).encode('utf8'))
        target  = extract_price_3(value, "$","\\n\\xe2")
        print( "1y Target Est = %s\n" %(target))

    # Close browser
    driver.quit()


if __name__ == "__main__":
    main()