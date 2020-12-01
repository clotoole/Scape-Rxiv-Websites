#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:57:14 2020

@author: codyotoole
"""

#Scrape metadata for published articles from aRxiv
#just use aRxiv meta file 


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver





#create list corresponding to number of aRxiv pages wanting to scrape
linklist = []
pages = pd.read_csv('/Users/codyotoole/Desktop/COVID_Preprints/aRxiv/arxiv_meta.csv') 

for i in range(0,len(pages)):
    pages['Link'][i] = pages['Link'][i].replace('pdf', 'abs')
    
for i in np.arange(0, len(pages)):
        linklist.append(pages['Link'][i])
 
       
        

#Get contents of first page 
driver = webdriver.Chrome('/Users/codyotoole/Downloads/chromedriver')
driver.get(linklist[0])        
html = driver.page_source 
page_html = BeautifulSoup(html, 'html5lib')
publish_meta = page_html.find_all('div', class_='leftcolumn')
    
    


#delete first page from list
del linklist[0]




#for every PMC page in the list
#takes some time, needs to fully load each aRxiv page to make sure proper
#data is gathered
for link in linklist:

	#Make a get request
    driver.get(link)
    html = driver.page_source
    page_html = BeautifulSoup(html, 'html5lib')
    publish_meta1 = page_html.find_all('div', class_='leftcolumn')

	#bring results together
    publish_meta.extend(publish_meta1)

len(publish_meta)




#empty lists for titles, subjects, doi, and journals
list_titles = []
list_subj = []
list_journal = []




#get the metadata from the HTML gathered previously
for n in np.arange(0, len(publish_meta)):


	#Getting the title
    title = publish_meta[n].find('h1', class_='title mathjax').get_text()
    list_titles.append(title)

	#Get Subjects
    try:
        subj = publish_meta[n].find('td', class_='tablecell subjects').get_text()
        list_subj.append(subj)
    except:
        list_subj.append('N/A')

    #get journal
    try:
        journal = publish_meta[n].find('td', class_='tablecell jref').get_text()
        list_journal.append(journal)
    except:
        list_journal.append('N/A')
    
        

	
 
#make into data frame (make sure all lists are the same length)
df_publsih_meta = pd.DataFrame(
	{
     'Title': list_titles,
	 'Subject': list_subj,
     'Journal': list_journal
	 })




#cleaning

for i in range(0,len(df_publsih_meta)):
    try:
        df_publsih_meta['Title'][i] = df_publsih_meta['Title'][i].split(":", 1)
        df_publsih_meta['Title'][i] = df_publsih_meta['Title'][i][1]
    except:
        continue

for i in range(0,len(df_publsih_meta)):
        df_publsih_meta['Subject'][i] = df_publsih_meta['Subject'][i].lstrip()
        
df_publsih_meta = df_publsih_meta.replace('\n','', regex=True)

df_publsih_meta = df_publsih_meta.replace('N/A',np.NaN)
   
df_publsih_meta = df_publsih_meta.dropna()

for i in range(0,len(pages)):
    pages['Link'][i] = pages['Link'][i].replace('abs', 'pdf')


#Make into csv
df_publsih_meta.to_csv('/Users/codyotoole/Desktop/aRxiv_publish_meta.csv')
