import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = '#YOUR USERNAME#'
password = '#YOUR PASSWORD#'
username = 'alexandertham95@gmail.com'
password = 'AT95password'
# username = 'ngdanieljr@gmail.com'
# password = '17071992Dan'

#Pandas
df = pd.DataFrame(columns = ['Name', 'Major', 'Internships', 'Certifications'])


#log in
#driver = webdriver.Chrome(r"#chromedriver Path#")
driver = webdriver.Chrome('/Users/danielng/Documents/Coding/Data Science:Analytics Stuff/Useful notebooks/Web Scraping on Linkedin/chromedriver')
driver.get('https://www.linkedin.com/login')

# username = alexandertham95@gmail.com
# password = AT95password


elementID = driver.find_element_by_id('username')
elementID.send_keys(username)
elementID = driver.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

profile_links = [
    'https://sg.linkedin.com/in/chloe-ng-89a5691a6',
    'https://sg.linkedin.com/in/kimberly-wong-may-qi',
    'https://sg.linkedin.com/in/estherngliting',
    'https://www.linkedin.com/in/nicoleteow/'
]

def func(profile_links):
    index=0
    for profile in profile_links:
        driver.get(profile)

        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')

        #LINKS
        # for link in soup.findAll('a', href = True):
        # 	if 'in/' in link.get('href'):
        # 		print(link.get('href'))

        #Clicking show more button
        # show_more = driver.find_element_by_xpath('//*[@id="ember168"]/button')
        # show_more.click()

        #NAME
        try:
            #name = soup.find('div',{'class':'flex-1 mr5 pv-top-card__list-container'})
            name = soup.find('h1',{'class':'text-heading-xlarge inline t-24 v-align-middle break-words'})
            #name = name.find('li')
            name = name.get_text().strip()

        
        except:
            name = 'Blank'

        #CERTIFICATIONS
        try:
            certs = soup.find('section', {'id': 'certifications-section'})
            #certs = certs.find('ul')
            certs = certs.find_all('h3')

            C = []
            for i in certs:
                C.append(i.get_text().strip())
            certs = C
            #certs = ''.join(C)
            
        except:
            certs = 'Blank'

        #MAJOR
        try:
            major = soup.find('section', {'id': 'education-section'})
            #major = major.find('ul')
            major = major.find('span', {'class': 'pv-entity__comma-item'})
            major = major.get_text()

        except:
            major = 'Blank'

        #Internships
        try:
            internships = soup.find('section', {'id': 'experience-section'})
            #internships = internships.find('ul')
            internships = internships.find_all('h3')

            I =[]
            for i in internships:
                I.append(i.get_text().strip())
            internships = I
            #internships = ''.join(I)

        except:
            internships = 'Blank'

        df.loc[index,'Name'] = name
        df.loc[index,'Major'] = major
        df.loc[index,'Internships'] = internships
        df.loc[index,'Certifications'] = certs

        index+=1
        print(df)

func(profile_links)
df.to_csv("testing.csv", encoding = 'utf-8', index= False) #saving as .csv file