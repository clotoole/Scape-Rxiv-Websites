#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:13:34 2020

@author: codyotoole
"""


# -*- coding: utf-8 -*-
import csv
from os import walk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import shutil
#
# Steps to follow: Create a folder in the Desktop for the topic you want to download PDFs for.
# Read and convert the pmcid txt to csv, and create a folder for downloading the pdfs. Also create a new folder
# to store the renamed files.
# set the value of baseDir to the path of the folder that you just created. and don't forget to follow it up with a '/'
# In addition to this, Set the pdfpath variable to the pdf downloaded folder which you newly created in step 1.
# ipcsv is the csv file that contains the PMCID List. set the variable with the name of the .csv file created in step 1.
# Summary wil contain the success and failures of download.
# Also, the log statements in the command line helps you keep track of the download process
# The last downloaded file for pmcid is the latest pmcid for which pdf has been downloaded.
# In case the system stops, remove all the rows that are completed from ipcsv
# Store the folder name of the renamed folder in the variable renaedpdfpath.
# if downloading is taking a long time, change the time.sleep(25) in line 57 to something like time.sleep(30).



#Change the basedir of files for reading pmcid excel
baseDir = '/Volumes/Elements/Research Materials/Papers/Covid_paper_2020/NSF_Grant/metag_preprint/'

#this is the directory your files are downloaded to
download_dir = '/Volumes/Elements/Research Materials/Papers/Covid_paper_2020/NSF_Grant/metag_preprint/PDFs'

#change this path to get pdf inside ur basedir
pdfpath = 'PDFs'
renamedpdfpath = 'Named_PDFs'
downloadDir =baseDir+ pdfpath + '/'
opDir = baseDir+ renamedpdfpath + '/'
ipcsv = 'metag_bioRxiv_full_meta.csv'
opcsv = 'summary.csv'
nmcsv = 'metag_bioRxiv_full_meta.csv'

# Path to and writer for output file (summary sheet)
filez = open(baseDir + opcsv, 'ab')
opwriter = csv.writer(filez)


# Path to and writer for input file (rxiv full metadata sheet)
pmidlist = []
ipfile = open(baseDir+ipcsv, 'rU')
pireader = csv.reader(ipfile)

#this will give full titles to papers
titlelist = []
nmfile = open(baseDir+nmcsv, 'rU')
nmreader = csv.reader(nmfile)

#change this to the location of your chromedriver
#in addition I changed it so it doesnt open a new window each iteration
options = Options()
options.add_experimental_option("prefs", {"download.default_directory": downloadDir,
                                              "plugins.always_open_pdf_externally": True})
options.add_argument("/Users/codyotoole/Applications/Google Chrome.app")
driver = webdriver.Chrome('/Users/codyotoole/Downloads/chromedriver', chrome_options=options)

def getPDF(term):
    print("Lauching browser for pmcid",term)
    

    # driver.maximize_window()
    
    driver.get('https://www.' + term+'.pdf')
    ####IF YOU ARE USING ARXIV THEN USE:
    #driver.get(term)
    
    
    # driver.maximize_window()
    #time.sleep(3)
  
    


#this will wait until the file is downloaded to continue 
def check_if_download_folder_has_unfinished_files():
    for (dirpath, dirnames, filenames) in walk(download_dir):
        return str(filenames)


def wait_for_files_to_download():
    time.sleep(5)  # let the driver start downloading
    file_list = check_if_download_folder_has_unfinished_files()
    while 'Unconfirmed' in file_list or 'crdownload' in file_list:
        file_list = check_if_download_folder_has_unfinished_files()
        time.sleep(1)




#renames files
def renameFile(title):
    print("Renaming file",title)
    try:
        files = []
        files = os.listdir(downloadDir)
        for file in files:
            if file.endswith('.pdf'):
                shutil.move(downloadDir+file,opDir+title+".pdf")

    except Exception as e:
        print("Failed to rename file:",title)




#I changed the set up here so it tells you how many have been downloaded
def setUp():
    # Read pmcids from excel and write it to list pmidlist
    for row in pireader:
        pmidlist.append(row[0])
    for row in nmreader:
        titlelist.append(row[1])
        #print row[0]
    n = 1
    del titlelist[0]
    del pmidlist[0]
    print("Number of articles",len(pmidlist))
    for term, title in zip(pmidlist, titlelist):
        print('Progress = ' + str(n) + '/' + str(len(pmidlist)))
        n = n + 1
        print(term,'start')
        # Download pdf for each pmcid in the excel sheet
        getPDF(term)
        wait_for_files_to_download()
        renameFile(title)
        


if __name__=="__main__":
    print ("begin execution")
    # read csv files to get a list of pmcids to download
    setUp()
    #close the files
    filez.close()
    ipfile.close()
    print("End of execution")
