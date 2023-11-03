#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:34:17 2023

@author: anyamarchenko
"""

import os
import csv
import time
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

###############################################################################
## Selenium set up
###############################################################################

# selenium chromedriver path on my computer, install with 'brew install --cask chromedriver'
DRIVER_PATH = "/usr/local/bin/chromedriver"
service = Service(executable_path = DRIVER_PATH)

# define options
options = webdriver.ChromeOptions()
options.add_argument("start-maximized") # start with max screen
#options.add_argument("-headless") # uncomment this to have it not open browser

# Chrome driver installation
driver = webdriver.Chrome(service = service, options = options)

###############################################################################

###############################################################################
## Get URLs to scrape from
###############################################################################

# Navigate to Wyoming
browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?e-Self-Homestead=_wyoming-usa_53')
sleep(2)
# Run this twice for it to navigate to correct page
browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?e-Self-Homestead=_wyoming-usa_53')

# Parse the HTML code
soup = BeautifulSoup(driver.page_source, 'lxml')

## Get URLs from page = 1
# Find all elements with class 'tblrow record' (the view record)
all_urls = [tag['jsopen'] for tag in soup.find_all('tr', class_=('tblrow record','tblrowalt record', 'calloutTrigger'))]

sleep(2)

# Get URLs from all other pages

# =============================================================================
# num_list = 20
# x=0 # remove this  
# while x<=3:
#     
#     # this is the HTML address for all pages after page = 1
#     browser = driver.get('https://www.ancestrylibrary.com/search/collections/60593/?e-Self-Homestead=_wyoming-usa_53&fh={0}&fsk=MDs3OTsyMA-61--61-'.format(num_list))
# 
#     time.sleep(3)
# 
#     soup = BeautifulSoup(driver.page_source, 'lxml')
# 
#     # Find all elements with class 'tblrow record' (the view record)
#     urls = [tag['jsopen'] for tag in soup.find_all('tr', class_=('tblrow record','tblrowalt record', 'calloutTrigger'))]
# 
#     # save URLs to list
#     all_urls.extend(urls)
#     
#     # iterate by 20 because that's how HTML addresses are set up here. 
#     num_list += 20
#     x +=1
#     
# 
# =============================================================================
###############################################################################
## Scrape URLs
###############################################################################

# Run this twice for it to navigate to correct page
record = driver.get(urls[0])

# Parse the HTML code
soup = BeautifulSoup(driver.page_source, 'lxml')

# Find all elements with class 'tblrow record' (the view record)
#table = soup.find_all(class_='tableHorizontal tableHorizontalRuled')

table = soup.find_all(xpath = '//*[@id="recordServiceData"]')

if table:
    headers = [th.text for th in table[0].find_all('th')]
    first_row_data = [td.text for td in table[0].find_all('td')]

    df = pd.DataFrame([first_row_data], columns=headers)

    for row in table[0].find_all('tr')[1:]:
        row_data = [td.text for td in row.find_all('td')]
        df = df.append(pd.Series(row_data, index=headers), ignore_index=True)
else:
    print("No table found on the page.")





# Find the first column (headers) and the first row of data
headers = [th.text for th in table[0].find_all('th')]
first_row_data = [td.text for td in table[0].find_all('td')]

# Create a DataFrame with headers as column names and first_row_data as the first row
df = pd.DataFrame([first_row_data], columns=headers)


#th is label 
#td is the value 
#xpath to table is //*[@id="recordServiceData"]

# Extract the column names from the first row
column_names = [th.text for th in table.find('tr').find_all('th')]

# Initialize an empty list to store rows
rows = []

# Iterate through each row in the table
for tr in table.find_all('tr')[1:]:  # Skip the first row (header row)
    row_data = [td.text for td in tr.find_all('td')]
    rows.append(row_data)

# Create a pandas DataFrame using the extracted data
df = pd.DataFrame(rows, columns=column_names)





# Initialize an empty list to store patents
patents = []

for url in all_urls:
    # Make a request to the URL and get the page content
    response = requests.get(url)

    # Parse the HTML code
    soup = BeautifulSoup(response.content, 'lxml')

    # Find all elements with class 'tableHorizontal tableHorizontalRuled'
    tables = soup.find_all(class_='tableHorizontal tableHorizontalRuled')

    # Iterate through each table
    for table in tables:
        # Extract the column names from the first row
        column_names = [th.text for th in table.find('tr').find_all('th')]

        # Initialize an empty list to store rows
        rows = []

        # Iterate through each row in the table
        for tr in table.find_all('tr')[1:]:  # Skip the first row (header row)
            row_data = [td.text for td in tr.find_all('td')]
            rows.append(row_data)

        # Create a pandas DataFrame using the extracted data
        df = pd.DataFrame(rows, columns=column_names)

        # Append the DataFrame to the list
        patents.append(df)


for url in all_urls:
    # Make a request to the URL and get the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with class 'tableHorizontal tableHorizontalRuled'
    tables = soup.find_all(class_='tableHorizontal tableHorizontalRuled')

    # Iterate through each table
    for table in tables:
        # Initialize an empty list to store rows
        rows = []

        # Iterate through each row in the table
        for tr in table.find_all('tr'):
            # Extract the first column as column name and the second column as row data
            cols = tr.find_all('td')
            if len(cols) >= 2:
                column_name = cols[0].text.strip()
                row_data = cols[1].text.strip()

                # Append the data to the rows list
                rows.append([column_name, row_data])

        # Create a pandas DataFrame using the extracted data
        df = pd.DataFrame(rows, columns=['Column_Name', 'Row_Data'])

        # Append the DataFrame to the list
        dataframes.append(df)









<table id="recordServiceData" class="table tableHorizontal tableHorizontalRuled">
					<tbody>

							<tr>
								<th>Name</th>
								<td>
									Christian J. Hepp
								</td>
							</tr>
				
