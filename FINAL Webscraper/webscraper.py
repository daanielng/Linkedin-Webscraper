"""Scrap Linkedin data with given URLs."""
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
import glob
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
df = pd.DataFrame(columns = ['Name', 'University', 'Major', 'Major Year', 'Internships', 'Internship Duration', 'Internship Description', 'Certifications', 'Education Description', 'Profile Link'])

dict_blanks = {'blanks': 0}

# Logging in
driver = webdriver.Chrome(driver_path)
driver.get('https://www.linkedin.com/login')
elementID = driver.find_element_by_id('username')
elementID.send_keys(username)
elementID = driver.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()


# Linkedin URLs directory
urls_dir = 'URLs'



def scrape(profile, index):
    driver.get(profile)
    time.sleep(3) #it allows for the page source to fully load

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
        major = major.find_all('span', {'class': 'pv-entity__comma-item'}) # find all majors

        #majors
        M = []
        for i in major:
            M.append(i.get_text().strip())

        major = M

    except:
        major = 'Blank'

#MAJOR YEAR
    try:
        major_year = soup.find('section', {'id': 'education-section'})
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

        #reset blank count
        dict_blanks['blanks']=0

    elif [profile, index] in linkedin_fails:
        print(f'failed to scrape {name}\'s profile') 

        #keeping track of consecutive blank profiles
        dict_blanks['blanks'] +=1
        print(f'blanks: {dict_blanks["blanks"]}')

    else:
        print(f'profile {index+1}: unable to scrape {name}\'s profile')
        linkedin_fails.append([profile,index])

        #keeping track of consecutive blank profiles        
        dict_blanks['blanks'] +=1
        print(f'blanks: {dict_blanks["blanks"]}')



    time.sleep(0.7)



linkedin_fails = [] #list to append all failed profiles



# Execute scraping function
def execute(profile_links,driver):
    index = 0

    for profile in profile_links:

        if dict_blanks['blanks']==7: #attempt to clear security check
            print('Action Required: Clear security check!')
            time.sleep(60)
        elif dict_blanks['blanks']==8: #attempt failed
            print('Security check stopped scraper')
            break

        scrape(profile, index)

        index +=1
    driver.close()

    # Execute scraping function on failed profiles
    if len(linkedin_fails) > 0:
        try:
            # Logging in
            driver = webdriver.Chrome('path to chromedriver')
            driver.get('https://www.linkedin.com/login')
            elementID = driver.find_element_by_id('username')
            elementID.send_keys(username)
            elementID = driver.find_element_by_id('password')
            elementID.send_keys(password)
            elementID.submit()
            time.sleep(100)
            for profile, index in linkedin_fails:
                if dict_blanks['blanks']==7: #attempt to clear security check
                    print('Action Required: Clear security check!')
                    time.sleep(60)
                elif dict_blanks['blanks']==8: #attempt failed
                    print('Security check stopped scraper')
                    break

                scrape(profile, index)
        except:
            print("Re-attempt failed, saving csv file now")
    driver.close()





for csvfile in glob.glob(urls_dir + '/*'):
    uni_name = csvfile.split('/')[-1].split('_')[0]

    start = time.time() #start timer

    csv_df = pd.read_csv(csvfile) #read csv file
    profile_links = list(csv_df['linkedin URLs']) #list of urls
    execute(profile_links, driver) #execute scrapper

    # Store info into csv file
    df.to_csv(f"{uni_name} profiles.csv", encoding = 'utf-8', index= False) #saving as .csv file

    end = time.time() #end timer

    print(f'{uni_name} csv file created: scraping took {(end-start)/60} minutes')
