#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 13:04:14 2020

@author: codyotoole
"""
#this code scrapes all of the links and titles 


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver



driver = webdriver.Chrome('/Users/codyotoole/Downloads/chromedriver')
driver.get('https://www.biorxiv.org/search/metagenome%20numresults%3A75%20sort%3Arelevance-rank?page=0')        
html = driver.page_source 
		
#Parse content of the request with BeautifulSoup
page_html = BeautifulSoup(html, 'html5lib')
		
#News Identification
covid_news = page_html.find_all('div', class_='highwire-article-citation highwire-citation-type-highwire-article')



n = 1
#create list corresponding to number of pages wanting to scrape
pages = [str(i) for i in range(1,69)] 

#for every page in the given interval
for page in pages:

	#Make a get request
    print('Progress = ' + str(n) + '/' + str(len(pages)))
    driver.get('https://www.biorxiv.org/search/metagenome%20numresults%3A75%20sort%3Arelevance-rank?page='+page)


	#Parse content of the request with BeautifulSoup
    html1 = driver.page_source
    page_html1 = BeautifulSoup(html1, 'html5lib')

	#News Identification
    covid_news1 = page_html1.find_all('div', class_='highwire-article-citation highwire-citation-type-highwire-article')

	#bring results together
    covid_news.extend(covid_news1)
    n = n+1

len(covid_news)





#empty lists for contents, links and titles
list_links = []
list_titles = []
list_authors = []


for n in np.arange(0, len(covid_news)):

    link_data = covid_news[n].find('span', class_='highwire-cite-title')


	#Getting the link of the article
    link = link_data.find('a')['href']
    list_links.append(link)

	#Getting the title
    title = link_data.get_text()
    list_titles.append(title)

    try:
        authors = covid_news[n].find('span', class_='highwire-citation-authors').get_text()
        list_authors.append(authors)
    except:
        list_authors.append('N/A')
	
 
    
    
#make into data frame (make sure all lists are the same length)
df_biorxiv = pd.DataFrame(
	{'Link': list_links,
     'Title': list_titles,
     'Authors': list_authors
	 })




#cleaning
df_biorxiv = df_biorxiv.replace('\n','', regex=True)

for i in range(0,len(df_biorxiv)):
    df_biorxiv['Title'][i] = df_biorxiv['Title'][i].strip()
  

for i in range(0,len(df_biorxiv)):
    df_biorxiv['Link'][i] = 'biorxiv.org' + df_biorxiv['Link'][i]
    



#Make into csv
df_biorxiv.to_csv('/Users/codyotoole/Desktop/metag_biorxiv_meta.csv')









