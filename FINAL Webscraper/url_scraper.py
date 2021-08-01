"""Extract Linkedin URLs based on Google search results."""
import requests
from bs4 import BeautifulSoup
import re
import datetime
import parsel
from parsel import Selector
import time
import configparser
import numpy as np
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()
config.read("config.ini")

driver_path = config["DRIVER"]["path"]

# Logging in
driver = webdriver.Chrome(driver_path)

#google search linkedin URLs
universities = ['National University of Singapore', 'Singapore Management University', 'Nanyang Technological University']
driver.get('https://www.google.com')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "National University of Singapore"')
search_query.send_keys(Keys.RETURN)



src = driver.page_source
soup = BeautifulSoup(src, 'lxml')

total_height = int(driver.execute_script("return document.body.scrollHeight"))

for i in range(1, total_height, 4):
    if i == int(total_height/2) or i == int(total_height/2)+1:
        time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, {});".format(i))

time.sleep(0.8)

linkedin_urls = []

for link in soup.findAll('a', href = True):
    if 'https://sg.linkedin.com/in/' in link.get('href'):
        url = link.get('href')
        linkedin_urls.append(url)
        print(url)

driver.close()
