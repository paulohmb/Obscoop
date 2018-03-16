# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:02:34 2017

@author: paulohmb
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import os
import selenium
import pandas as pd
import html5lib
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

#Drive e enginer
driver = webdriver.Chrome('C:\\Users\paulohmb\Documents\chromedriver.exe')
wait = WebDriverWait(driver,20)
engine = create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')

#
##Baixando demonstraçoes contabeis 
#driver.get('http://dados.gov.br/dataset/http-www-ans-gov-br-perfil-do-setor-dados-abertos-dados-abertos-disponiveis-n3')
#links = driver.find_elements_by_xpath('//*[@id="dataset-resources"]/ul/li/a')
#lCsv = []
#for link in links:
#    temp = link.get_attribute('href')
#    lCsv.append(temp)
#for i in range(len(lCsv)):
#    driver.get(lCsv[i])
#    driver.find_element_by_xpath('//*[@id="content"]/div[3]/section/div[1]/p/a').click()

dfDemonstracos_p1 = pd.DataFrame()
dfDemonstracos_p2 = pd.DataFrame()
dfDemonstracos_p3 = pd.DataFrame()
dfDemonstracos_p4 = pd.DataFrame()
path = 'C:\\Users\paulohmb\Downloads\DemoCont'
j = 0
for root, dirs, files in os.walk(path):
    for name in files:
        if j < 10:
            dfTemp = pd.read_csv('%s\%s'%(root,name),sep=';',encoding = 'latin-1')
            dfDemonstracos_p1 = dfDemonstracos_p1.append(dfTemp)
            print(j)
            j= 1+j
        elif j < 20:
            dfTemp = pd.read_csv('%s\%s'%(root,name),sep=';',encoding = 'latin-1')
            dfDemonstracos_p2 = dfDemonstracos_p2.append(dfTemp)
            print(j)
            j = j+1
        elif j <30:
            dfTemp = pd.read_csv('%s\%s'%(root,name),sep=';',encoding = 'latin-1')
            dfDemonstracos_p3 = dfDemonstracos_p3.append(dfTemp)
            print(j)
            j = j+1
        else:
            dfTemp = pd.read_csv('%s\%s'%(root,name),sep=';',encoding = 'latin-1')
            dfDemonstracos_p4 = dfDemonstracos_p4.append(dfTemp)
            print(j)
            j = j+1
            
dfDemonstracos_p1 =  dfDemonstracos_p1.drop('   ',axis = 1)
dfDemonstracos_p2 =  dfDemonstracos_p2.drop('   ',axis = 1)
dfDemonstracos_p3 =  dfDemonstracos_p3.drop('   ',axis = 1)
dfDemonstracos_p4 =  dfDemonstracos_p4.drop('   ',axis = 1)


dfDemonstracos_p1.to_sql('Demontracoes_ANS_pt1',engine,schema='temp',if_exists='fail',index=True)
dfDemonstracos_p2.to_sql('Demontracoes_ANS_pt2',engine,schema='temp',if_exists='fail',index=True)
dfDemonstracos_p3.to_sql('Demontracoes_ANS_pt3',engine,schema='temp',if_exists='fail',index=True)
dfDemonstracos_p4.to_sql('Demontracoes_ANS_pt4',engine,schema='temp',if_exists='fail',index=True)











r = requests.get('http://www.ans.gov.br/index.php?option=com_ouvidoria&view=ouvidoria&registro=null&task=search&origin=aHR0cDovL3d3dy5hbnMuZ292LmJyL2FhbnMvb3V2aWRvcmlhL291dmlkb3JpYXMtZG9zLXBsYW5vcy1kZS1zYXVkZQ==&post=http://www.ans.gov.br/aans/ouvidoriaindex.php/aans/ouvidoria/lista-de-ouvidorias-privadas-cadastradas&limitstart=0').text
s =soup(r,'lxml')
table = soup.find_all('table')
t= pd.read_html('http://www.ans.gov.br/aansindex.php?option=com_ouvidoria&view=ouvidoria&task=search&origin=aHR0cDovL3d3dy5hbnMuZ292LmJyL2FhbnMvb3V2aWRvcmlhL291dmlkb3JpYXMtZG9zLXBsYW5vcy1kZS1zYXVkZQ==&limitstart=0')


class HTMLTableParser:
    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [(table['id'],self.parse_html_table(table))\
                for table in soup.find_all('table')]  

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
                    
            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        
        return df

hp =HTMLTableParser()
table=hp.parse_url("http://www.ans.gov.br/aansindex.php?option=com_ouvidoria&view=ouvidoria&task=search&origin=aHR0cDovL3d3dy5hbnMuZ292LmJyL2FhbnMvb3V2aWRvcmlhL291dmlkb3JpYXMtZG9zLXBsYW5vcy1kZS1zYXVkZQ==&limitstart=0")[0][1]
