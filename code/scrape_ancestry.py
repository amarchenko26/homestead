#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:34:17 2023
@author: anyamarchenko
"""

import os
import time
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


###############################################################################
## Selenium set up
###############################################################################

# Selenium chromedriver path on my computer, installed with 'brew install --cask chromedriver'
DRIVER_PATH = "/usr/local/bin/chromedriver"
service = Service(executable_path = DRIVER_PATH)

# define options
options = webdriver.ChromeOptions()
options.add_argument("start-maximized") # start with max screen
options.add_argument("-headless") # uncomment this to have it not open browser

# Chrome driver installation
driver = webdriver.Chrome(service = service, options = options)



###############################################################################
## Choose code to run
###############################################################################

run_get_url = 1
run_scrape = 0



###############################################################################
## Get URLs to scrape from
###############################################################################

if run_get_url == 1:
    
    # finished 1895-1898 years, this is now stored in diff .csv
    years = range(1873, 1874)
    #years = [year for year in range(1863, 1909) if year not in [1895, 1896, 1897, 1898]] #what i used to remove the yrs i'd already done
    wy_urls = []
    
    for year in years:
        
        page = 1
        
        # Navigate to Homestead Place = WY (Exact) and Year = year (Exact)
        browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?count=50&e-Self-Homestead={}_wyoming-usa_53&e-Self-Homestead_x=0_1-0'.format(year))
        sleep(2)
        # Run this twice to navigate to correct page
        browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?count=50&e-Self-Homestead={}_wyoming-usa_53&e-Self-Homestead_x=0_1-0'.format(year))
            
        while page < 500: 
            
            # Parse the HTML code
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            # Find all elements with class 'tblrow record' (the view record)
            
            urls = [tag['jsopen'] for tag in soup.find_all('tr', class_=('tblrow record','tblrowalt record', 'calloutTrigger'))]
            row_text = soup.find_all('tr', class_=('tblrow record'))
            row_text = [row.text for row in row_text] # makes it a list
            
            # Split the string into lines
            #test_row = row_text[0]
#            lines = for row in row_text.strip().split('\n')

            # Extract the name, date, location, and state
 #           info_list = [lines[1], lines[2], lines[3], lines[4]]

            # save URLs to list
            #wy_urls.extend(urls)
                
# =============================================================================
#             # save URLs to .csv every 5 pages
#             if page % 5 == 0:
#                 # convert list to df
#                 df = pd.DataFrame()
#                 df["wy_urls"] = wy_urls
#                 df.to_csv('/Users/anyamarchenko/Documents/GitHub/homestead/data/wy_urls.csv', index=False)
#             
#             # click next button
#             sleep(2)
#         
            try:
                next_button = driver.find_element(By.CLASS_NAME, 'ancBtn.sml.green.icon.iconArrowRight')
                next_button.click()
            except:
                print(f"No next page found for year {year} after {page}")
                break  # Exit the while loop if an exception occurs
             
             #xpath for next button = //*[@id="pageSets"]/ul/li[5]/a
        
            page += 1  

print("Finished getting WY URLs")

###############################################################################
## Scrape each record
###############################################################################


# code stops finding tables after URL #5. Is this a website issue? Let's try a random 6 URLs. 
#test_urls = wy_urls[53:80] #6 elements

wy_urls_minus_50 = wy_urls[50:]

if run_scrape == 1:
    
    # Initialize an empty df to store patents
    patents = pd.DataFrame()

    # Navigate to a random record 
    record = driver.get(wy_urls_minus_50[0])
    
    count = 1
    for url in wy_urls_minus_50:
    
        # Navigate to correct record
        time.sleep(2)
        record = driver.get(url)

        # Parse the HTML code
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        print(f"Parsed URL number {count}")
        
        time.sleep(5)
        
        # Find all elements with id = 'recordServiceData'
        table = soup.find_all(id ='recordServiceData')
    
        if table:
            
            # Grab first col of table
            col_names = [th.text for th in table[0].find_all('th')]
            
            # Grab second col of table, remove \n and \t 
            first_row_vals = [td.text.strip('\n\t') for td in table[0].find_all('td')]
            
            # Bind into a df called row
            row_df = pd.DataFrame([first_row_vals], columns = col_names)
            
            # Add col keepin track which url we are on
            row_df["url"] = url
            
            # Concat takes care of when columns differ b/w records          
            patents = pd.concat([patents, row_df], axis = 0) #columns are axis = 1 b/c columns look like a 1
            
        else:
            print(f"No table found for url {url}.")
            break
        
        # save URLs to .csv every 50 names
        if count % 50 == 0:
            patents.to_csv('/Users/anyamarchenko/Documents/GitHub/homestead/data/wy_patents.csv', index=False)
        
        count += 1




  

###############################################################################
## Get URLs to scrape from - BY STATE, no next page button
###############################################################################
# =============================================================================
# 
# # Navigate to Wyoming
# browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?count=50&e-Self-Homestead=_wyoming-usa_53')
# sleep(2)
# # Run this twice for it to navigate to correct page
# browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?count=50&e-Self-Homestead=_wyoming-usa_53')
# 
# # Parse the HTML code
# soup = BeautifulSoup(driver.page_source, 'lxml')
# 
# ###### Get URLs from page = 1
# # Find all elements with class 'tblrow record' (the view record)
# all_urls = [tag['jsopen'] for tag in soup.find_all('tr', class_=('tblrow record','tblrowalt record', 'calloutTrigger'))]
# 
# sleep(2)
# 
# 
# ###### Get URLs from all other pages
# page = 50
#  
# # this is the HTML address for all pages after page = 1
# browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?count=50&e-Self-Homestead=_wyoming-usa_53&fh={0}&fsk=MDs0OTs1MA-61--61-'.format(page))
# 
# time.sleep(3)
# 
# soup = BeautifulSoup(driver.page_source, 'lxml')
# 
# # Find all elements with class 'tblrow record' (the view record)
# urls = [tag['jsopen'] for tag in soup.find_all('tr', class_=('tblrow record','tblrowalt record', 'calloutTrigger'))]
# 
# # save URLs to list
# all_urls.extend(urls)
# 
# # iterate by 50 because that's how HTML addresses are set up here. 
# page += 50
#      
# =============================================================================





# ask moira about how to not have website shut you out after many requests 


