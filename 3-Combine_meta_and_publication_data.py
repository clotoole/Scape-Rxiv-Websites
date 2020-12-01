#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:56:06 2020

@author: codyotoole
"""


import pandas as pd



#BIORXIV
df1 = pd.read_csv('/Users/codyotoole/Desktop/metag_bioRxiv_meta.csv')

df2 = pd.read_csv('/Users/codyotoole/Desktop/metag_bioRxiv_publish_meta.csv')
df2.index = df2['Unnamed: 0']
df2.columns = ['Unnamed:0', 'Title2', 'Date', 'Journal', 'DOI']

df3 = df1.join(df2, how='outer')
df3 = df3.drop('Unnamed:0', axis=1)
df3.to_csv('/Users/codyotoole/Desktop/metag_bioRxiv_full_meta.csv')




#MEDRXIV
df1 = pd.read_csv('/Users/codyotoole/Desktop/COVID_Preprints/Rxiv/medRxiv_meta.csv')

df2 = pd.read_csv('/Users/codyotoole/Desktop/COVID_Preprints/publish_data_6_17/medRxiv_publish_meta.csv')
df2.index = df2['Unnamed: 0']
df2.columns = ['Unnamed:0', 'Title2', 'Journal', 'DOI']

df3 = df1.join(df2, how='outer')
df3 = df3.drop('Unnamed:0', axis=1)
df3.to_csv('/Users/codyotoole/Desktop/medRxiv_full_meta.csv')




#ARXIV
df1 = pd.read_csv('/Users/codyotoole/Desktop/COVID_Preprints/aRxiv/aRxiv_meta.csv')

df2 = pd.read_csv('/Users/codyotoole/Desktop/COVID_Preprints/publish_data_6_17/aRxiv_publish_meta.csv')
df2.index = df2['Unnamed: 0']
df2.columns = ['Unnamed:0', 'Title2', 'Subject', 'Journal']

df3 = df1.join(df2, how='outer')
df3 = df3.drop('Unnamed:0', axis=1)
df3.to_csv('/Users/codyotoole/Desktop/aRxiv_full_meta.csv')