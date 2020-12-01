#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:19:51 2020

@author: codyotoole
"""
#Scrape metadata for published articles from bio/medRxiv
#just use bio/medRxiv meta file 


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver





#create list corresponding to number of aRxiv pages wanting to scrape
linklist = []
pages = pd.read_csv('/Users/codyotoole/Desktop/metag_bioRxiv_meta.csv') 
for i in np.arange(0, len(pages)):
        linklist.append(pages['Link'][i])
 
       
        

#Get contents of first page 
driver = webdriver.Chrome('/Users/codyotoole/Downloads/chromedriver')
driver.get('https://www.' + linklist[0])        
html = driver.page_source 
page_html = BeautifulSoup(html, 'html5lib')
publish_meta = page_html.find_all('div', class_='panel-display panels-960-layout jcore-2col-layout')
    
    


#delete first page from list
del linklist[0]


n = 1

#for every PMC page in the list
#takes some time, needs to fully load each aRxiv page to make sure proper
#data is gathered
for link in linklist:

	#Make a get request
    print('Progress = ' + str(n) + '/' + str(len(linklist)))
    driver.get('https://www.' + link)
    html = driver.page_source
    page_html = BeautifulSoup(html, 'html5lib')
    publish_meta1 = page_html.find_all('div', class_='panel-display panels-960-layout jcore-2col-layout')

	#bring results together
    publish_meta.extend(publish_meta1)
    n = n+1

len(publish_meta)




#empty lists for titles, subjects, doi, and journals
list_titles = []
list_doi = []
list_journal = []
list_date = []




#get the metadata from the HTML gathered previously
for n in np.arange(0, len(publish_meta)):


	#Getting the title
    try:
        title = publish_meta[n].find('h1', class_='highwire-cite-title').get_text()
        list_titles.append(title)
    except:
        list_titles.append('N/A')

	#Get Meta
    meta = publish_meta[n].find('div', class_='pub_jnl')

    #get journal
    try:
        journal = meta.get_text()
        list_journal.append(journal)
    except:
        list_journal.append('N/A')
    
    #get DOI
    try: 
        doi = meta.find('a')['href']
        list_doi.append(doi)
    except:
        list_doi.append('N/A')
        
    #get date
    date = publish_meta[n].find('div', class_='panel-pane pane-custom pane-1').get_text()
    list_date.append(date)
    
 
for n, i in enumerate(list_journal):
   if i == 'This article is a preprint and has not been certified by peer review [what does this mean?].':
       list_journal[n] = 'N/A'
       
for n, i in enumerate(list_doi):
   if i == '/content/what-unrefereed-preprint':
       list_doi[n] = 'N/A'       




 
#make into data frame (make sure all lists are the same length)
df_publsih_meta = pd.DataFrame(
	{
     'Title': list_titles,
     'Date': list_date,
     'Journal': list_journal,
     'DOI': list_doi
	 })




#cleaning    
df_publsih_meta = df_publsih_meta.replace('\n','', regex=True)

for i in range(2321,len(df_publsih_meta)):
    df_publsih_meta['Date'][i] = df_publsih_meta['Date'][i].split('Posted')[1]

df_publsih_meta = df_publsih_meta.replace('N/A',np.NaN)

#df_publsih_meta['DOI'] = df_publsih_meta['DOI'].replace(np.NaN, 'N/A')
   
#df_publsih_meta = df_publsih_meta.dropna()


#Make into csv
df_publsih_meta.to_csv('/Users/codyotoole/Desktop/metag_bioRxiv_publish_meta.csv')


