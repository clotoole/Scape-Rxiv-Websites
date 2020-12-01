#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 13:04:14 2020

@author: codyotoole
"""


import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd




#get result for first page
#Make a get request
response = requests.get('https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=COVID-19&terms-0-field=title&terms-1-operator=OR&terms-1-term=SARS-CoV-2&terms-1-field=abstract&terms-3-operator=OR&terms-3-term=COVID-19&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=SARS-CoV-2&terms-4-field=title&terms-5-operator=OR&terms-5-term=coronavirus&terms-5-field=title&terms-6-operator=OR&terms-6-term=coronavirus&terms-6-field=abstract&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&source=home-covid-19')
		
#Parse content of the request with BeautifulSoup
page_html = BeautifulSoup(response.text, 'html5lib')
		
#News Identification
covid_news = page_html.find_all('li', class_='arxiv-result')




#create list corresponding to number of pages wanting to scrape
pages = [str(i) for i in range(200,600,200)] 

#for every page in the given interval
for page in pages:
		
	#Make a get request
	response1 = requests.get('https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=COVID-19&terms-0-field=title&terms-1-operator=OR&terms-1-term=SARS-CoV-2&terms-1-field=abstract&terms-3-operator=OR&terms-3-term=COVID-19&terms-3-field=abstract&terms-4-operator=OR&terms-4-term=SARS-CoV-2&terms-4-field=title&terms-5-operator=OR&terms-5-term=coronavirus&terms-5-field=title&terms-6-operator=OR&terms-6-term=coronavirus&terms-6-field=abstract&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&source=home-covid-19&start='+page)
		
	#Parse content of the request with BeautifulSoup
	page_html1 = BeautifulSoup(response1.text, 'html5lib')
		
	#News Identification
	covid_news1 = page_html1.find_all('li', class_='arxiv-result')
	
	#bring results together
	covid_news.extend(covid_news1)

len(covid_news)





#empty lists for contents, links and titles
list_links = []
list_titles = []
list_dates = []
list_authors = []
list_abstracts = []

for n in np.arange(0, len(covid_news)):

    link_data = covid_news[n].find('p', class_='list-title is-inline-block')


	#Getting the link of the article
    link = link_data.find('a')['href']
    list_links.append(link)

	#Getting the title
    title = covid_news[n].find('p', class_='title is-5 mathjax').get_text()
    list_titles.append(title)


	#Get Dates
    date = covid_news[n].find('p', class_='is-size-7').get_text()
    list_dates.append(date)

    authors = covid_news[n].find('p', class_='authors').get_text()
    list_authors.append(authors)

    abstract = covid_news[n].find('span', class_='abstract-full has-text-grey-dark mathjax').get_text()
    list_abstracts.append(abstract)
	
 
    
    
#make into data frame (make sure all lists are the same length)
df_arxiv = pd.DataFrame(
	{'Link': list_links,
     'Title': list_titles,
     'Authors': list_authors,
     
     'Abstract': list_abstracts,
	 'Date': list_dates
	 
	 })




#cleaning
for i in range(0,len(df_arxiv)):
    df_arxiv['Date'][i] = df_arxiv['Date'][i].split(";",1)
    df_arxiv['Date'][i] = df_arxiv['Date'][i][0]

df_arxiv = df_arxiv.replace('\n','', regex=True)

for i in range(0,len(df_arxiv)):
    df_arxiv['Title'][i] = df_arxiv['Title'][i].strip()

for i in range(0,len(df_arxiv)):
    df_arxiv['Abstract'][i] = df_arxiv['Abstract'][i].strip()
    
for i in range(0,len(df_arxiv)):
    df_arxiv['Abstract'][i] = df_arxiv['Abstract'][i].split("△",1)
    df_arxiv['Abstract'][i] = df_arxiv['Abstract'][i][0]

    
for i in range(0,len(df_arxiv)):
    df_arxiv['Authors'][i] = df_arxiv['Authors'][i].split(":",1)
    df_arxiv['Authors'][i] = df_arxiv['Authors'][i][1]
    
for i in range(0,len(df_arxiv)):
    df_arxiv['Authors'][i] = df_arxiv['Authors'][i].strip()
    
for i in range(0,len(df_arxiv)):
    df_arxiv['Link'][i] = df_arxiv['Link'][i].replace('abs', 'pdf')
    


#Make into csv
df_arxiv.to_csv('/Users/codyotoole/Desktop/arxiv_meta.csv')




