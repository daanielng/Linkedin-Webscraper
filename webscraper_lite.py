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
import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#email: usedforotherreasons@gmail.com
# pw: Loyalty@2020
username = 'alexandertham95@gmail.com'
password = 'AT95password'

# username = 'thomaswys9@gmail.com'
# password = 'Loyalty@2020'


# Make dataframe to store profile info
df = pd.DataFrame(columns = ['Name', 'University', 'Major', 'Major Year', 'Internships', 'Internship Duration', 'Internship Description', 'Certifications', 'Education Description', 'Profile Link'])


# Logging in
driver = webdriver.Chrome('/Users/danielng/Documents/Coding/Data Science:Analytics Stuff/Useful notebooks/Web Scraping on Linkedin/chromedriver')
driver.get('https://www.linkedin.com/login')
elementID = driver.find_element_by_id('username')
elementID.send_keys(username)
elementID = driver.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

# Linkedin URLs directory
urls_dir = r'/Users/danielng/Documents/Coding/Data Science:Analytics Stuff/Useful notebooks/Web Scraping on Linkedin/URLs'



def scrape(profile, index):
    
    driver.get(profile)
    time.sleep(2) #it allows for the page source to fully load
    
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    total_height = int(driver.execute_script("return document.body.scrollHeight"))

        
    for i in range(1, total_height, 4):
        if i == int(total_height/2) or i == int(total_height/2)+1:
            time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, {});".format(i))

    time.sleep(0.8)


#NAME
    try:
        name = soup.find('h1',{'class':'text-heading-xlarge inline t-24 v-align-middle break-words'})
        name = name.get_text().strip()

    except:
        name = 'Blank'


#UNIVERSITY
    try:
        uni = soup.find('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'})
        uni = uni.get_text()
    except:
        uni = 'Blank'
        
        
#MAJOR
    try:
        major = soup.find('section', {'id': 'education-section'})
        #major = major.find('span', {'class': 'pv-entity__comma-item'})
        major = major.find_all('span', {'class': 'pv-entity__comma-item'}) # find all majors
        
        #majors
        M = []
        for i in major:
            M.append(i.get_text().strip())
            
        major = M
        #major = major.get_text()
        
    except:
        major = 'Blank'
        
#MAJOR YEAR
    try:
        major_year = soup.find('section', {'id': 'education-section'})
        #major_year = major_year.find_all('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'})
        major_year = major_year.find_all('time')
    
        #major year
        M_year = []
        for i in major_year:
            M_year.append(i.get_text().strip())
          
        lst_years = []  
        for i in range(0, len(M_year),2):
            lst_years.append(f'{M_year[i]}-{M_year[i+1]}') #example: '2018-2020'
            
        major_year = lst_years
        
    except:
        major_year = 'Blank'


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

#INTERNSHIP DURATION
    try:
        intern_dur = soup.find('section',{'id':'experience-section'})
        intern_dur = intern_dur.find_all('h4', {'class': 'pv-entity__date-range t-14 t-black--light t-normal'})

        intern_d =[]
        for i in intern_dur:
            intern_d.append(i.get_text().strip())

        lst_dur = []
        for i in intern_d:
            dur = i.split('\n')[-1]
            lst_dur.append(dur)
        
        intern_dur = lst_dur

    except:
        intern_dur = 'Blank'

#INTERNSHIP DESCRIPTION
    try:
        intern_desc = soup.find('section',{'id':'experience-section'})
        intern_desc = intern_desc.find_all('div', {'class': 'pv-entity__extra-details t-14 t-black--light ember-view'})

        i_desc = []
        for i in intern_desc:
            i_desc.append(i.get_text().strip())
        
        intern_desc = i_desc
        
    except:
        intern_desc = 'Blank'
        
        
#EDUCATION DESCRIPTION  
    try:
        edu_desc = soup.find('section', {'id': 'education-section'})
        edu_desc = edu_desc.find_all('p', {'class': 'pv-entity__description t-14 t-normal mt4'})
        e_desc = []
        for i in edu_desc:
            e_desc.append(i.get_text().strip())
        
        edu_desc = e_desc
        
    except:
        edu_desc = 'Blank'

    insert_info(index, name, uni, major, major_year, internships, intern_dur, intern_desc, certs, edu_desc, profile)



def insert_info(index, name, uni, major, major_year, internships, intern_dur, intern_desc, certs, edu_desc, profile):
    if major!= 'Blank' and uni != 'Blank':
        df.loc[index,'Name'] = name
        df.loc[index, 'University'] = uni
        df.loc[index,'Major'] = major
        df.loc[index, 'Major Year'] = major_year
        df.loc[index,'Internships'] = internships
        df.loc[index, 'Internship Duration'] = intern_dur
        df.loc[index,'Internship Description'] = intern_desc
        df.loc[index,'Certifications'] = certs
        df.loc[index,'Education Description'] = edu_desc
        df.loc[index, 'Profile Link'] = profile
        print(f'scrapped profile {index+1}')
        
    elif [profile, index] in linkedin_fails:
        print(f'failed to scrape {name}\'s profile') 
        
    else:
        print(f'profile {index+1}: unable to scrape {name}\'s profile')
        linkedin_fails.append([profile,index])
        
    time.sleep(0.7)



linkedin_fails = [] #list to append all failed profiles


# Execute scraping function
def execute(profile_links,driver):
    index = 0
    for profile in profile_links:
        scrape(profile, index)
        
        index +=1
    driver.close()

    # Execute scraping function on failed profiles
    if len(linkedin_fails) > 0:
        try:
            # Logging in
            driver = webdriver.Chrome('/Users/danielng/Documents/Coding/Data Science:Analytics Stuff/Useful notebooks/Web Scraping on Linkedin/chromedriver')
            driver.get('https://www.linkedin.com/login')
            elementID = driver.find_element_by_id('username')
            elementID.send_keys(username)
            elementID = driver.find_element_by_id('password')
            elementID.send_keys(password)
            elementID.submit()
                
            for profile, index in linkedin_fails:
                scrape(profile, index)
        except:
            print("Re-attempt failed, saving csv file now")
    driver.close()



start = time.time()
for csvfile in glob.glob(urls_dir + '/*'):
    uni_name = csvfile.split('/')[-1].split('_')[0]
    
    print(f'running {uni_name} csv file')
    if uni_name == 'NUS':
        csv_df = pd.read_csv(csvfile)
        profile_links = list(csv_df['linkedin URLs'])
        execute(profile_links, driver)
        
        # Store info into csv file
        df.to_csv(f"{uni_name} profiles.csv", encoding = 'utf-8', index= False) #saving as .csv file
end = time.time()
#print(f'scraping took {end-start} seconds')







