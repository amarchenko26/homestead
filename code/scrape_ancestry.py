#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:34:17 2023

@author: anyamarchenko
"""

import os
import csv
import math
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from bs4 import BeautifulSoup

###############################################################################
## Selenium set up

# selenium chromedriver path on my computer, install with 'brew install --cask chromedriver'
DRIVER_PATH = "/usr/local/bin/chromedriver"
service = Service(executable_path = DRIVER_PATH)

# define options
options = webdriver.ChromeOptions()
options.add_argument("start-maximized") # start with max screen
#options.add_argument('disable-infobars')

# Chrome driver installation
driver = webdriver.Chrome(service = service, options = options)

###############################################################################

browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?e-Self-Homestead=_wyoming-usa_53')
sleep(2)
#just run this twice
browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?e-Self-Homestead=_wyoming-usa_53')

# Parse the HTML code
soup = BeautifulSoup(driver.page_source, 'lxml')

## Get URLs from first page. 
# Find all elements with class 'tblrow record' (the view record)
all_urls = [tag['jsopen'] for tag in soup.find_all('tr', class_=('tblrow record','tblrowalt record', 'calloutTrigger'))]

sleep(2)

# Get URLs from all other pages

num_list = 20
x=0
while x<=100:
    
    # this is the HTML address for all pages after page = 1
    browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?e-Self-Homestead=_wyoming-usa_53&fh={0}&fsk=MDs3OTsyMA-61--61-'.format(num_list))

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find all elements with class 'tblrow record' (the view record)
    urls = [tag['jsopen'] for tag in soup.find_all('tr', class_=('tblrow record','tblrowalt record', 'calloutTrigger'))]

    # save URLs to list
    all_urls.extend(urls)
    
    # iterate by 20 because that's how HTML addresses are set up here. 
    num_list += 20
    x +=1
    


