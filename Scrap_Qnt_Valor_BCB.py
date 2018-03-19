"""
@author: Paulo Barbosa
Scrap informações sobre crédito rural e tratamento dos dados 
Scrap rural credit information and data treatment
site http://www.bcb.gov.br/pt-br#!/r/micrrural/?path=conteudo%2FMDCR%2FReports%2FqvcMunicipio.rdl&nome=Quantidade%20e%20Valor%20dos%20Contratos%20por%20Munic%C3%ADpio&exibeparametros=true&botoesExportar=true   

"""
#####################################################################################################################################################################################################################

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import sqlalchemy as sql
import pandas as pd
from unicodedata import normalize
import re

#Function to take out latin-1 type of character of string
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
if __name__ == '__main__':
    from doctest import testmod
    testmod()
#################################################################################################################################
#simple function with sleep and identification of download
def load(a,b):
    print('Carregando {}'.format(b))
    time.sleep(a)

# path_driver = path of chrome drive
#and sql conection
engine = sql.create_engine('***')
path_driver = 'C:\\Users\paulohmb\Documents\chromedriver.exe'
driver = webdriver.Chrome(path_driver)
wait = WebDriverWait(driver, 20)

#interacting with drop down menu and select the wanted variable 
driver.get('http://www.bcb.gov.br/pt-br#!/r/micrrural/?path=conteudo%2FMDCR%2FReports%2FqvcMunicipio.rdl&nome=Quantidade%20e%20Valor%20dos%20Contratos%20por%20Munic%C3%ADpio&exibeparametros=true&botoesExportar=true')
time.sleep(5)
driver.find_element_by_xpath('//*[@id="mesInicio"]/option[7]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="mesFim"]/option[8]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[3]/td[2]/div/button').click()
driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[3]/td[2]/div/div/ul/li[1]/label/input').click()
driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[2]/td[2]').click()
time.sleep(5)

    
#Download credit line year 2013/2014 
#and setting years 
anoInicio = driver.find_element_by_xpath('//*[@id="anoInicio"]/option[2]').click()
anoFim = driver.find_element_by_xpath('//*[@id="anoFim"]/option[3]').click()

#setting download directory and the name file of the downloaded file 
#that is needed for the renaming
path = 'C:/Users/paulohmb/Downloads/'
file = 'Quantidade e Valor dos Contratos por Município 07-12-2017.xls'
#local variable set for the loops
j=2
i=2
while j < 38:
    driver.find_element_by_xpath('//*[@id="cdPrograma"]/option{}'.format(j)).click()
    sPrograma =driver.find_element_by_xpath('//*[@id="cdPrograma"]/option{}'.format(j)).text
#Replacing special characters
    sPrograma =sPrograma.replace("/", "-")
    print('%s:%s'%(sPrograma,j))
    i=2
    while i < 28:
        driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).click()
        sRecurso = driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).text
        sRecurso =sRecurso.replace("/","-")
        if i == 18:
            sRecurso = 'LETRA DE CRÉDITO DO AGRONEGÓCIO (LCA) - TAXA(2)'
        print(i)
        load(45, sRecurso)
        driver.find_element_by_xpath('//*[@src="/Paginas/Imagens/excel.gif"]').click()
        load(20, 'download')
        os.rename(os.path.join(path,file),
                  os.path.join(path,'Programa_%s_Recurso_%s(2013-2014).xls'%(sPrograma,sRecurso)))
        i = 1+i
    j = 1+j
    
#Download of 2014/2015
driver.find_element_by_xpath('//*[@id="anoInicio"]/option[3]').click()
time.sleep(10)
driver.find_element_by_xpath('//*[@id="anoFim"]/option[4]').click()

j=2
i=2
while j < 38:
    driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).click()
    sPrograma =driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).text
    sPrograma =sPrograma.replace("/", "-")
    if i == 18:
            sRecurso = 'LETRA DE CRÉDITO DO AGRONEGÓCIO (LCA) - TAXA(2)'
    print('%s:%s'%(sPrograma,j))
    i=2
    while i < 28:
        driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).click()
        sRecurso = driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).text
        sRecurso =sRecurso.replace("/","-")
        print(i)
        load(45, sRecurso)
        driver.find_element_by_xpath('//*[@src="/Paginas/Imagens/excel.gif"]').click()
        load(20, 'download')
        os.rename('C:\\Users\paulohmb\Downloads\Quantidade e Valor dos Contratos por Município 07-12-2017.xls',
                  'C:\\Users\paulohmb\Downloads\Programa_%s_Recurso_%s(2014-2015).xls'%(sPrograma,sRecurso))
        i = 1+i
    j = 1+j

##Download of 2015/2016
driver.find_element_by_xpath('//*[@id="anoInicio"]/option[4]').click()
time.sleep(10)
driver.find_element_by_xpath('//*[@id="anoFim"]/option[5]').click()

j=2
i=2
while j < 38:
    driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).click()
    sPrograma =driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).text
    sPrograma =sPrograma.replace("/", "-")
    if i == 18:
            sRecurso = 'LETRA DE CRÉDITO DO AGRONEGÓCIO (LCA) - TAXA(2)'
    print('%s:%s'%(sPrograma,j))
    i=2
    while i < 28:
        driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).click()
        sRecurso = driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).text
        sRecurso =sRecurso.replace("/","-")
        print(i)
        load(45, sRecurso)
        driver.find_element_by_xpath('//*[@src="/Paginas/Imagens/excel.gif"]').click()
        load(20, 'download')
        os.rename('C:\\Users\paulohmb\Downloads\Quantidade e Valor dos Contratos por Município 07-12-2017.xls',
                  'C:\\Users\paulohmb\Downloads\Programa_%s_Recurso_%s(2015-2016).xls'%(sPrograma,sRecurso))
        i = 1+i
    j = 1+j
    
##Download of 2016/2017
driver.find_element_by_xpath('//*[@id="anoInicio"]/option[5]').click()
time.sleep(10)
driver.find_element_by_xpath('//*[@id="anoFim"]/option[6]').click()

j=2
i=2
while j < 38:
    driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).click()
    sPrograma =driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).text
    sPrograma =sPrograma.replace("/", "-")
    if i == 18:
            sRecurso = 'LETRA DE CRÉDITO DO AGRONEGÓCIO (LCA) - TAXA(2)'
    print('%s:%s'%(sPrograma,j))
    i=2
    while i < 28:
        driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).click()
        sRecurso = driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).text
        sRecurso =sRecurso.replace("/","-")
        print(i)
        load(45, sRecurso)
        driver.find_element_by_xpath('//*[@src="/Paginas/Imagens/excel.gif"]').click()
        load(20, 'download')
        os.rename('C:\\Users\paulohmb\Downloads\Quantidade e Valor dos Contratos por Município 07-12-2017.xls','C:\\Users\paulohmb\Downloads\Programa_%s_Recurso_%s(2016-2017).xls'%(sPrograma,sRecurso))
        i = 1+i
    j = 1+j
    
#################################################################################################################################

#################################################################################################################################
#Renaming files
for root, dirs, files in os.walk("C:\\Users\paulohmb\Documents\Sql\Quantidade e Valor dos Contratos por Município"
                                 , topdown=False):
   for name in files:
       slash = "\\"
       print(name)
       sNome = remover_acentos(name)
       sNome = sNome.replace(" ", "")
       os.rename(root + slash + name,root + slash + sNome)
#################################################################################################################################
#append tables
i=0
dftemp = pd.DataFrame()

for root, dirs, files in os.walk("C:\\Users\paulohmb\Documents\Sql\Quantidade e Valor dos Contratos por Municipio"
                                 , topdown=False):
   for name in files:
        slash = "\\"
        temp = pd.read_csv(root + slash + name, sep = ';', header  = 13,encoding='latin -1')
        temp = temp.dropna(axis=1, how='all')
        print(name,i)
        temp['Modelo'] = name
        dftemp = dftemp.append(temp)
        dftemp.to_sql('ContratosFinal',engine,schema='temp',if_exists='replace',index=True)
        i=i+1
#rename columns
dftemp = dftemp.rename(index = str, columns={'Unnamed: 3':'Municipio'
                                             ,'Unnamed: 5':'Estado'
                                             ,'Unnamed: 6':'Codmun'
                                             ,'Unnamed: 7':'Atividade'})
vModelo = dftemp['Modelo']
############################################################################################################################################
#creating new columns with the the missing information 
#re expression ?<= and ?= that match character in between of the strings 
i = 0
lPrograma = []

for a in dftemp['Modelo']:
    print(a)
    sPrograma=dftemp.iloc[i,14]
    sPrograma = re.findall('(?<=Programa_)(.*)(?=_Recurso)', sPrograma)
    lPrograma.append(sPrograma[0])
    i = i+1
dftemp['Programa'] = lPrograma
############################################################################################################################################
i = 0
lRecurso = []
for a in vModelo:
    print(a)
    sRecurso=dftemp.iloc[i,14]
    sRecurso = re.findall('(?<=Recurso_)(.*)(?=\(2)', sRecurso)
    lRecurso.append(sRecurso[0])
    i = i+1
dftemp['Recurso'] = lRecurso
#################################################################################################################################
i = 0
lano = []
for a in vModelo:
    print(a)
    sano=dftemp.iloc[i,14]
    sano = re.findall('(?<=\()(.*)(?=\)\.csv)', sano)
    lano.append(sano[0])
    i = i+1
dftemp['Ano'] = lano
#################################################################################################################################
#removing garbage of dataframe
dftemp = dftemp.drop(['Modelo'],axis = 1)
dftemp = dftemp[dftemp.Atividade != 'Total']
#################################################################################################################################
#removing nan
dftemp = dftemp.fillna(0)
i=0
for a in dftemp['Municipio']:
    if a != 0:
        replace = dftemp.iloc[i,0]
        i= i+1
        print(replace,i)
    else:
        dftemp.iloc[ i, 0] = replace
        i = i+1
i=0
for a in dftemp['Estado']:
    if a != 0:
        replace = dftemp.iloc[i,1]
        i= i+1
        print(replace,i)
    else:
        dftemp.iloc[ i, 1] = replace
        i = i+1
i=0
for a in dftemp['Codmun']:
    if a != 0:
        replace = dftemp.iloc[i,2]
        i= i+1
        print(replace,i)
    else:
        dftemp.iloc[ i, 2] = replace
        i = i+1
dftemp = dftemp.reset_index(drop = True)
#sending to database
dftemp.to_sql('ContratosFinal',engine,schema='temp',if_exists='replace',index=True)
