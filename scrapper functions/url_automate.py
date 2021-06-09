import requests
from bs4 import BeautifulSoup
import re
import datetime
import parsel
from parsel import Selector
import time
import numpy as np
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


username = 'alexandertham95@gmail.com'
password = 'AT95password'



# Logging in
driver = webdriver.Chrome('/Users/danielng/Documents/Coding/Data Science:Analytics Stuff/Useful notebooks/Web Scraping on Linkedin/chromedriver')
# driver.get('https://www.linkedin.com/login')
# elementID = driver.find_element_by_id('username')
# elementID.send_keys(username)
# elementID = driver.find_element_by_id('password')
# elementID.send_keys(password)

# elementID.submit()

#google search linkedin URLs
universities = ['National University of Singapore', 'Singapore Management University', 'Nanyang Technological University']
driver.get('https://www.google.com')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "Nanyang Technological University"')
search_query.send_keys(Keys.RETURN)
time.sleep(60)


#'https://sg.linkedin.com/in/profilename'

#linkedin_urls = driver.find_elements_by_class_name('yuRUbf')


start = time.time()
linkedin_urls = []
count = 0
while count!=50:
    try:
        if int(driver.execute_script("return document.body.scrollHeight"))==1248: #to catch random security checks
            time.sleep(100)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        total_height = int(driver.execute_script("return document.body.scrollHeight"))

        for i in range(1, total_height, 4):
            if i == int(total_height/2) or i == int(total_height/2)+1:
                time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, {});".format(i))

        time.sleep(0.8)


        # linkedin_urls = soup.findAll('a', href = True)
        #linkedin_urls = linkedin_urls.find_all('div', {'class':'yuRUbf'})
        
        for link in soup.findAll('a', href = True):
            url = link.get('href')
            if 'https://sg.linkedin.com/in/' in url and url not in linkedin_urls:
                linkedin_urls.append(url)
                print(f'stored: {url}')
                
        time.sleep(0.5)
        print(f'scrapped page {count+1} ')
        next_page = driver.find_element_by_id('pnnext')
        next_page.click()
        count += 1
    except:
        print('error: No more pages left')
        break
    
end = time.time()
print(f'scrapping took {end-start} seconds')
if len(linkedin_urls)>0:
    df = pd.DataFrame(data= {'linkedin URLs': linkedin_urls})
    df.to_csv("linkedin_urls.csv", encoding = 'utf-8', index= False) #saving as .csv file
    print('csv file created')

driver.close()