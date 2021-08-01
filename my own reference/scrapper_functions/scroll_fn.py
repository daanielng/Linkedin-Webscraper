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
username = config["ACCOUNT"]["username"]
password = config["ACCOUNT"]["password"]


# Make dataframe to store profile info
df = pd.DataFrame(columns = ['Name', 'University', 'Major', 'Internships', 'Certifications'])


# Logging in
driver = webdriver.Chrome(driver_path)
driver.get('https://www.linkedin.com/login')
elementID = driver.find_element_by_id('username')
elementID.send_keys(username)
elementID = driver.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

# Profiles to scrape
profile_links = [
    'https://sg.linkedin.com/in/chloe-ng-89a5691a6',
    'https://sg.linkedin.com/in/kimberly-wong-may-qi',
    'https://sg.linkedin.com/in/estherngliting',
    'https://www.linkedin.com/in/nicoleteow/',
    'https://www.linkedin.com/in/shi-kai-ng-6149aa172/',
    'https://www.linkedin.com/in/gerald-chua-bale/',
    'https://www.linkedin.com/in/chng-charmaine/',
    'https://www.linkedin.com/in/madelene-kim-86a9171a8/',
    'https://www.linkedin.com/in/lshuyu/',
    'https://www.linkedin.com/in/charisse-lim/',
    'https://www.linkedin.com/in/eetecklim/',
    'https://www.linkedin.com/in/kee-kong-tay/',
    'https://www.linkedin.com/in/victoria-cai-pei-jin-5a2645167/',
    'https://www.linkedin.com/in/liming-yu/',
    'https://www.linkedin.com/in/deborah-tan-72156b1a2/',
    'https://www.linkedin.com/in/junhao-foo/',
    'https://www.linkedin.com/in/noahwongchiehui/',
    'https://www.linkedin.com/in/shanachia/',
    'https://www.linkedin.com/in/claudia-neo-260800/',
    'https://www.linkedin.com/in/kashishrajpal/',
    'https://www.linkedin.com/in/dargohzy/',
    'https://www.linkedin.com/in/pohsuansoon/',
    'https://www.linkedin.com/in/adelyneyu/',
    'https://www.linkedin.com/in/gtanwl/',
    'https://www.linkedin.com/in/chien-yu-toh/',
    'https://www.linkedin.com/in/nixon-loh-yq/',
    'https://www.linkedin.com/in/nghaoyuan/',
    'https://www.linkedin.com/in/xavier-tan-4777a91aa/',
    'https://www.linkedin.com/in/elkanhon/',
    'https://www.linkedin.com/in/chanyongming23/',
    'https://www.linkedin.com/in/gabriellemaswi/',
    'https://www.linkedin.com/in/raymond-lim-496b8719a/',
    'https://www.linkedin.com/in/jungyoujin/'
]


def scrape(profile, index):

    driver.get(profile)
    #time.sleep(5) #it allows for the page source to fully load

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    total_height = int(driver.execute_script("return document.body.scrollHeight"))

    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    time.sleep(3.5)



#NAME
    try:
        name = soup.find('h1',{'class':'text-heading-xlarge inline t-24 v-align-middle break-words'})
        name = name.get_text().strip()

    except:
        name = 'Blank'
        print(f'profile {index+1}\'s name is blank')


#UNIVERSITY
    try:
        uni = soup.find('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'})
        uni = uni.get_text()

    except:
        uni = 'Blank'
        print(f'profile {index+1}: {name}\'s uni is blank')


#MAJOR
    try:

        major = soup.find('section', {'id': 'education-section'})
        major = major.find('span', {'class': 'pv-entity__comma-item'})

        major = major.get_text()

    except:
        major = 'Blank'
        print(f'profile {index+1}: {name}\'s major is blank')


#CERTIFICATIONS
    try:

        certs = soup.find('section',{'id':'certifications-section'})
        certs = certs.find_all('h3', {'class': 't-16 t-bold'})

        C = []
        for i in certs:
            C.append(i.get_text().strip())
        certs = C


    except:
        certs = 'Blank'
        print(f'profile {index+1}: {name}\'s cert is blank')


#INTERNSHIPS
    try:
        internships = soup.find('section',{'id':'experience-section'})
        internships = internships.find_all('h3', {'class': 't-16 t-black t-bold'})

        I =[]
        for i in internships:
            I.append(i.get_text().strip())

        internships = I

    except:
        internships = 'Blank'
        print(f'profile {index+1}: {name}\'s internship is blank')



    if major!= 'Blank' and uni != 'Blank':
        df.loc[index,'Name'] = name
        df.loc[index, 'University'] = uni
        df.loc[index,'Major'] = major
        df.loc[index,'Internships'] = internships
        df.loc[index,'Certifications'] = certs

        print(f'scrapped profile {index+1}')

    else:
        return None
    time.sleep(0.7)

index = 0
for profile in profile_links[:1]:
    scrape(profile, index)
    index+=1
