# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from ast import literal_eval
import datetime

data_dir = r'data directory path'

#load csv file
df = pd.read_csv(data_dir)


# %%
# create Year 1 to Year 5 Columns
df['Year 1'] = 'No'
df['Year 2'] = 'No'
df['Year 3'] = 'No'
df['Year 4'] = 'No'
df['Year 5'] = 'No'


# %%
def date_between(index, num_lst, year_lst, start_date):
    if len(start_date)>4:
        year_index = 0
        # example --> year1: 2016aug to 2017aug, year2: 2017aug to 2018aug, year3: 2018aug to 2019aug, year4: 2019aug to 2020aug

        for i in range(len(num_lst)):
            start = f'Aug {num_lst[i]}'
            end = f'Aug {num_lst[i]+1}'
            
            date_start = datetime.datetime.strptime(start, '%b %Y')
            date_check = datetime.datetime.strptime(start_date, '%b %Y')
            date_end = datetime.datetime.strptime(end, '%b %Y')

            if date_start< date_check < date_end:
                df.iloc[index, df.columns.get_loc(f'{year_lst[year_index]}')] = 'Yes'
            year_index += 1
        

for index, row in df.iterrows():
    edu_lst = literal_eval(row['Major'])
    internship_lst = literal_eval(row['Internships'])

    #check for Bachelor's Degree
    if edu_lst: #if not empty list
        for edu in edu_lst:
            if 'Bachelor' in edu and ':' in edu: #if 'Bachelor' in string
                duration = edu.split(' : ')[-1]
                start_year = int(duration.split('-')[0])
                end_year = int(duration.split('-')[1])
    #continue loop if no Bachelor's Degree or degree duration suspiciously long
    if (end_year - start_year)>5 or not edu_lst:   
        continue 
    
    year_lst = []
    num_lst = []
    count = 1
    while count <= (end_year-start_year):
        year_lst.append(f'Year {count}')
        num_lst.append(start_year + count-1)
        count += 1


    #check for internships during Bachelor's Degree
    #example: year 1 student --> 2018 Aug to 2019 Aug
    if not internship_lst:
        continue
    for internship in internship_lst:
        intern_duration = internship.split(' : ')[-1]
        start_date = intern_duration.split(' – ')[0]
        
        date_between(index, num_lst, year_lst, start_date)


df


# %%
# check how many Year 5 Internships are there: out of curiousity... --> if very few or zero, remove entire column

(df.loc[df['Year 5 Internship']=='Yes']) # seems like only one person has year 5 internship and not from local university, thus remove entire row

df = df.drop(df[df.Name == 'Aung P.'].index)


# %%
# create new csv file with added columns

structured_df = pd.DataFrame(columns = ['Name', 'University', 'Major', 'Internships', 'Year 1 Internship', 'Year 2 Internship', 'Year 3 Internship', 'Year 4 Internship', 'Certifications', 'Hackathon/Case Competition Experience', 'Profile Link'])

structured_df['Name'] = df['Name']
structured_df['University'] = df['University']
structured_df['Major'] = df['Major']
structured_df['Internships'] = df['Internships']
structured_df['Year 1 Internship'] = df['Year 1']
structured_df['Year 2 Internship'] = df['Year 2']
structured_df['Year 3 Internship'] = df['Year 3']
structured_df['Year 4 Internship'] = df['Year 4']
structured_df['Certifications'] = df['Certifications']
structured_df['Hackathon/Case Competition Experience'] = df['Hackathon/Case Competition Experience']
structured_df['Profile Link'] = df['Profile Link']

structured_df


# %%
# store in csv file
structured_df.to_csv("cleaned_data_w_year_n_internship.csv", encoding = 'utf-8', index= False) #saving as .csv file
    


