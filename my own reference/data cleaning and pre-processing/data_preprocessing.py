
# %%
import pandas as pd
import os
from ast import literal_eval

#csv directory
csv_dir = r'your path'


#create dataframe from csv file
for doc in os.listdir(csv_dir):
    uni_name = doc.split(' ')[0]
    if uni_name == 'NUS':
        nus_df = pd.read_csv(csv_dir + '/' + doc)
    if uni_name == 'NTU':
        ntu_df = pd.read_csv(csv_dir + '/' + doc)
    if uni_name == 'SMU':
        smu_df = pd.read_csv(csv_dir + '/' + doc)



#combine individual dataframes
combined_df = pd.concat([nus_df, ntu_df, smu_df])

#reset index in combined dataframe
combined_df = combined_df.reset_index(drop = True)

combined_df


# %%
# clean 'Major' column

# use 'Major Year' to check how many education levels: seems like there are at most 3 educational levels

#Note: there are too many variations in the 'Major' column, i.e some profiles added A level score, distinctions, etc. which are too tedious to hardcode in the conditions

def combine_major(index, major_lst, major_year):
    lst_major = []
    while len(major_lst)>2 and len(major_year)>1:
        word_1 = major_lst[0]
        word_2 = major_lst[1]
        
        year = major_year.pop(0)
        name = word_1 + ', ' + word_2 + ' : ' + year
        
        lst_major.append(name)
        major_lst = major_lst[2:]

    if len(major_lst)==3 and len(major_year)>0:
        word_1 = major_lst[0]
        word_2 = major_lst[1]
        word_3 = major_lst[2]

        year = major_year.pop(0)
        name = word_1 + ', ' + word_2 + ', ' + word_3 + ' : ' + year
        
        lst_major.append(name)

    elif len(major_lst)==2 and len(major_year)>0:
        word_1 = major_lst[0]
        word_2 = major_lst[1]
        
        year = major_year.pop(0)
        name = word_1 + ', ' + word_2 + ' : ' + year
        
        lst_major.append(name)
    elif len(major_lst)==1 and len(major_year)>0:
        word_1 = major_lst[0]
        
        year = major_year.pop(0)
        name = word_1 + ' : ' + year
        
        lst_major.append(name)

    major_lst = lst_major
    combined_df.iloc[index, combined_df.columns.get_loc('Major')] = major_lst

# execute combine_major function for all rows
for index, row in combined_df.iterrows():
    if row['Major Year']=='Blank':
        row['Major Year'] = []
        
    else:
        combine_major(index, literal_eval(row['Major']), literal_eval(row['Major Year']))
    print(index, row['Major'])


# %%
# clean 'Internships' column

def clean_internship_column(index, internship_lst):
    clean_lst = []
    
    for i in internship_lst:
        if '\n' not in i:
            clean_lst.append(i) #valid job title
        else:
            name = i.split('\n')[-1]
            clean_lst.append(name) #company related job title: no specified job title

    internship_lst = clean_lst
    combined_df.iloc[index, combined_df.columns.get_loc('Internships')] = internship_lst

def add_internship_year(index, internship_lst, internship_duration_lst):
    clean_lst = []
    for i in range(min(len(internship_duration_lst), len(internship_lst))):
        internship = internship_lst[i]
        duration = internship_duration_lst[i]
        combined = internship + ' : ' + duration

        clean_lst.append(combined)

    internship_lst = clean_lst
    combined_df.iloc[index, combined_df.columns.get_loc('Internships')] = internship_lst


for index, row in combined_df.iterrows():
    if row['Internship Duration']=='Blank':
        combined_df.iloc[index, combined_df.columns.get_loc('Internship Duration')]  = []
    if row['Internships'] == 'Blank':
        combined_df.iloc[index, combined_df.columns.get_loc('Internships')] = []
    else:
        clean_internship_column(index, literal_eval(row['Internships']))
        add_internship_year(index, row['Internships'], literal_eval(row['Internship Duration']))


# %%
# Create boolean Hackathon/Case Competition column

bool_lst = []
for index, row in combined_df.iterrows():
    edu_lst = literal_eval(row['Education Description'])
    
    if len(edu_lst) > 0:
        for edu_desc in edu_lst:
            if 'Hackathon' in edu_desc or 'hackathon' in edu_desc or 'Case Competition' in edu_desc or 'case competition' in edu_desc:
                bool_lst.append('Yes')
                break
            else:
                bool_lst.append('No')
                break
    else:
        bool_lst.append('No')


combined_df['Hackathon/Case Competition Experience'] = bool_lst


# %%
# clean 'Certificates' column

for index, row in combined_df.iterrows():
    if row['Certifications'] == 'Blank':
        combined_df.iloc[index, combined_df.columns.get_loc('Certifications')]  = []


# %%
# create structured dataframe from csv file
structured_df = pd.DataFrame(columns = ['Name', 'University', 'Major', 'Internships', 'Certifications', 'Hackathon/Case Competition Experience', 'Profile Link'])

structured_df['Name'] = combined_df['Name']
structured_df['University'] = combined_df['University']
structured_df['Major'] = combined_df['Major']
structured_df['Internships'] = combined_df['Internships']
structured_df['Certifications'] = combined_df['Certifications']
structured_df['Hackathon/Case Competition Experience'] = combined_df['Hackathon/Case Competition Experience']
structured_df['Profile Link'] = combined_df['Profile Link']

structured_df


# %%
# store in csv file
structured_df.to_csv("cleaned_data.csv", encoding = 'utf-8', index= False) #saving as .csv file


# %%



