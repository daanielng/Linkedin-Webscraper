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




def valid(profile):
    blanks = []
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    uni = soup.find('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'})
    certs = soup.find('section',{'id':'certifications-section'})
    internships = soup.find('section',{'id':'experience-section'})
    major = soup.find('section', {'id': 'education-section'})
    
    blanks.extend([uni, certs, internships, major])
    
    count=0
    while blanks.count(None)>3:
        print(f"refreshing profile {index+1}")
        
        blanks = []
        driver.get(profile)
        time.sleep(5)
        
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        
        uni = soup.find('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'})
        certs = soup.find('section',{'id':'certifications-section'})
        internships = soup.find('section',{'id':'experience-section'})
        major = soup.find('section', {'id': 'education-section'})
        
        blanks.extend([uni, certs, internships, major])
        count+=1
        print(f'{count} refresh(s), ', blanks)
    print('valid profile', blanks)


username = '#YOUR USERNAME#'
password = '#YOUR PASSWORD#'



#Pandas
df = pd.DataFrame(columns = ['Name', 'University', 'Major', 'Internships', 'Certifications'])


#log in
#driver = webdriver.Chrome(r"#chromedriver Path#")
driver.get('https://www.linkedin.com/login')


elementID = driver.find_element_by_id('username')
elementID.send_keys(username)
elementID = driver.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

#time.sleep(10)
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

index = 0
for profile in profile_links:
    driver.get(profile)
    time.sleep(5) #it allows for the page source to fully load
    
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')


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
        #ul.pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more
        #education-section.pv-profile-section.education-section.ember-view

        major = soup.find('section', {'id': 'education-section'})
        #major = soup.find('p', {'class': 'pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal'})
        #major = major.find('ul')
        major = major.find('span', {'class': 'pv-entity__comma-item'})
        
        major = major.get_text()
        
    except:
        major = 'Blank'
        print(f'profile {index+1}: {name}\'s major is blank')
        

#CERTIFICATIONS
    try:
        
        certs = soup.find('section',{'id':'certifications-section'})
        #certs = certs.find_all('ul', {'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more'})
        #certs = certs.find('ul')
        #certs = certs.find_all('li', {'class': 'pv-profile-section__sortable-item pv-certification-entity ember-view'})
        certs = certs.find_all('h3', {'class': 't-16 t-bold'})

        C = []
        for i in certs:
            C.append(i.get_text().strip())
        certs = C
        #certs = ''.join(C)

    except:
        certs = 'Blank'
        print(f'profile {index+1}: {name}\'s cert is blank')
        

#INTERNSHIPS
    try:
        internships = soup.find('section',{'id':'experience-section'})
        #internships = soup.find('ul', {'class': 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more'})
        #internships = internships.find('ul')
        internships = internships.find_all('h3', {'class': 't-16 t-black t-bold'})

        I =[]
        for i in internships:
            I.append(i.get_text().strip())

        internships = I

    except:
        internships = 'Blank'
        print(f'profile {index+1}: {name}\'s internship is blank')


    # #Internships Descriptions
    # try:
    #     intern_descriptions = soup.find('section',{'id':'experience-section'})


    df.loc[index,'Name'] = name
    df.loc[index, 'University'] = uni
    df.loc[index, 'Major'] = major
    df.loc[index, 'Internships'] = internships
    df.loc[index, 'Certifications'] = certs
    
    print(f'scrapped profile {index+1}')
    time.sleep(0.7)
    index +=1

driver.close()


df.to_csv("testing4.csv", encoding = 'utf-8', index= False) #saving as .csv file





