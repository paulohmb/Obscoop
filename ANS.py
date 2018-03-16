# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:02:34 2017

@author: paulohmb

Scraping das demonstrações contabeis da NSN; Compilando uma tabela com o resulado;
Integrando os dados no banco de dados
----------------------------------------------------------------------------------
Scraping of NSN accounting statements; Building new table; Sending to database
database 

"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import pandas as pd
from sqlalchemy import create_engine

#Drive and enginer
driver = webdriver.Chrome('C:\\Users\paulohmb\Documents\chromedriver.exe')
wait = WebDriverWait(driver,20)

engine = create_engine('****')


#Downloading of accounting statements
driver.get('http://dados.gov.br/dataset/http-www-ans-gov-br-perfil-do-setor-dados-abertos-dados-abertos-disponiveis-n3')
#Find all the links
links = driver.find_elements_by_xpath('//*[@id="dataset-resources"]/ul/li/a')
lCsv = []
for link in links:
    temp = link.get_attribute('href')
    lCsv.append(temp)
#Dowloading
for i in range(len(lCsv)):
    driver.get(lCsv[i])
    driver.find_element_by_xpath('//*[@id="content"]/div[3]/section/div[1]/p/a').click()

#Creating Dataframe
dfDemonstracos = pd.DataFrame()

#Path of downloads
path = 'C:\\Users\paulohmb\Downloads\DemoCont'

#Compile all dataset on a single table
j = 0
for root, dirs, files in os.walk(path):
    for name in files:
        dfTemp = pd.read_csv('{%s}\{%s}'.format(root,name),sep=';',encoding = 'latin-1')
        dfDemonstracos = dfDemonstracos.append(dfTemp)
dfDemonstracos =  dfDemonstracos.drop('   ',axis = 1)

#Sending to database
dfDemonstracos.to_sql('Demontracoes_ANS',engine,schema='temp',if_exists='fail',index=True, chunksize = 10000)

