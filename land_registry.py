'''
This is a docstring for the module
'''
import os, os.path, shutil
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager #installs Chrome webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import csv
import urllib.request
from tqdm import tqdm
from pathlib import Path
import tempfile
import uuid #universally unique id
from uuid import UUID
import json
from json import JSONEncoder
import pandas as pd

class Scraper:

    def __init__(self, url: str = "https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads", browser = "Edge"):  
        
        try:
            if browser == "Chrome":
                options = ChromeOptions()
                options.add_argument("--incognito") #open Chrome browser in incognito mode - csv file cannot be loaded/saved via normal Chrome
                self.driver = Chrome(ChromeDriverManager().install(), options=options)
            else:
                self.driver = webdriver.Edge() #create Microsoft Edge driver (Chrome is blocking downloads from Land Registry)
            self.driver.get(url)
            print("Webpage loaded successfully")

        except NoSuchElementException:
            print("Webpage not loaded - please check for errors")

        self.driver.maximize_window() #maximise window upon loading webpage

    #click accept cookies button on webpage
    def accept_cookies(self, xpath: str = '//div[@id="global-cookie-message"]'): 
        '''
        Looks for and clicks on the accept cookies button

        Parameters:
        ---------
        xpath: str
            The xpath of the accept cookies button

        '''
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))) #locate cookies frame
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="global-cookie-message"]/div[1]/div/div[2]/button[1]').click() #click "Accept Cookies" button
            print("'Accept Cookies' button clicked")
            time.sleep(2)
            
        except TimeoutException: #if accept button is not found after 10 seconds by driver
            print("No cookies found") 

        #check if there is an additional message to be hidden after clicking "Accept Cookies" button
        try:
            self.driver.find_element(By.XPATH, '//*[@id="global-cookie-message"]/div[2]/div/button').click() #click "Hide this message" button
            print("'Accepted Cookies' message hidden")
            time.sleep(3)

        except TimeoutException:
            print("No 'Accepted Cookies' message to hide") 

        
        return None

    def find_container(self, xpath: str = '//*[@id="content"]/div[3]/div[1]'):
        return self.driver.find_element(By.XPATH, xpath)
    
    def load_data(self, c_xpath : str = '//*[@id="contents"]/div[2]/div/div/ul[4]/li[1]/a', e_xpath : str = '//*[@id="contents"]/div[2]/div/div/ul[4]/li[2]/a', browser = "Chrome"):
        '''
        This is to find links in the search results container 
        Parameters
        -------
        xpath: str
            locate the links in the container 
        '''
        self.container = self.find_container()
        time.sleep(5)
        try:
            if browser == "Chrome":
                self.data = self.driver.find_element(By.XPATH, c_xpath).send_keys(Keys.CONTROL,'t')
            else:
                self.data = self.driver.find_element(By.XPATH, e_xpath).click()
            print("Link accessed")
        except:
            "Unable to find xpath"
        
        return self.data
    
    def get_data(self, xpath : str = '/html/body'):
        #self.driver.find_element(By.XPATH, xpath).send_keys(Keys.CONTROL,'a')
        
        data = []
        labels = self.driver.find_element(By.XPATH, xpath)
        for x in labels: 
            hello = data.append(x.text)
        print("Data obtained")
        time.sleep(1)
        df = pd.DataFrame(hello)
        time.sleep(5)
        df.to_csv('output123.csv')
        '''#print(text)
        with open('output.csv', 'wb', encoding='utf-8') as data_file:
            writer = csv.writer(data_file, delimiter='\n')
            writer.writerows(data)'''
        return df
        #'/html/body/pre' 
    
    def close_window(self):
        time.sleep(10)
        self.driver.quit()
        print("Webpage closed")

        return None
        


if __name__ == "__main__": #will only run methods below if script is run directly
    scraper = Scraper() #call scraper class
    scraper.accept_cookies()
    scraper.load_data()
    scraper.get_data()