# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 02:51:47 2016

@author:Paulo Henrique
Scraping das tarifas cobradas pela cooperativas de creditos do Brasil
----------------------------------------------------------------------
Scraping of transaction tax of credit brazilian co-ops
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from sqlalchemy import create_engine
import pandas as pd
import re
import time

# Driver and Sql conection
engine = create_engine('***')
driver = webdriver.Chrome('C:\\Users\paulohmb\Downloads\chromedriver.exe')
wait = WebDriverWait(driver, 1000)

# Definindo função que checa se um elemento existe.
def elem_existe(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# Definindo função que limpa as listas
def limpar(string):
    if string == '':
        return("nao_possui")
    elif string != 'nao_possui':
        string = string.split(': ')[1]
        return(string)


#Creating DataFrame
tab_tarifas  = pd.DataFrame()

#Scraping CNPJ of all co-ops
p = 0
cnpj = []
for p in range(0, 1040, 20):
    driver.get("http://www4.bcb.gov.br/fis/cosif/rest/buscar-instituicoes_app.asp#?segmentoId=9&inicioPagina={}&inicioPaginaRegime=0".format(p))
    driver.refresh()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[@ng-show='selecionado']")))
    link = driver.find_elements_by_xpath('//a[@ng-if="filiacao.s || isConfederacaoNaoFinanceira(filiacao)"]')
    for i in range(len(link)):
        link[i] = link[i].get_attribute("href")
        cnpj.append(re.search("[0-9]*$", link[i]).group(0))


# Creating list
tarifas = []

#Acessing co-ops and checking if they have transaction tax(tarifas)
for j in range(len(cnpj)):
    print(j)
    driver.get('http://www4.bcb.gov.br/fis/cosif/rest/mostrar-instituicao.asp#?cnpj='+cnpj[j])
    driver.refresh()
    a = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'iframeapp')))
    driver.switch_to_frame(driver.find_element_by_class_name("iframeapp"))
    if elem_existe('//a[@title = "Tarifas"]'):
        tarifas.append(driver.find_element_by_xpath('//a[@title = "Tarifas"]').get_attribute('href'))
    else:
        tarifas.append('sem_tarifas')

#Get the valuer of transaction tax
k = 0
for i in tarifas:       
    if i != 'sem_tarifas':
        driver.get(i)
        try:
            driver.find_element_by_xpath('html/body/div[2]/div[3]/p[3]/a[1]/span').click()
        except:
            continue
        produto = []
        unidade = []
        data    = []
        valor   = []
        period  = []
        for j in driver.find_elements_by_class_name('fundoPadraoBClaro3'):
                    try:        
                        produto.append(j.find_element_by_xpath('td[2]').text)
                    except:
                        produto.append("nao_possui")     
                    try:
                        unidade.append(j.find_element_by_xpath('td[3]').text)
                    except:
                        unidade.append("nao_possui")
                    try:    
                        data.append(j.find_element_by_xpath('td[4]').text)
                    except:
                        data.append("nao_possui")
                    try:
                        valor.append(j.find_element_by_xpath('td[5]').text)
                    except:
                        valor.append("nao_possui")
                    try:    
                        period.append(j.find_element_by_xpath('td[6]').text)
                    except:
                        period.append("nao_possui")
        produto = pd.Series(produto)
        unidade = pd.Series(unidade)
        data    = pd.Series(data)
        valor   = pd.Series(valor)
        period  = pd.Series(period)
        tabela = pd.DataFrame({'cooperativa':cnpj[k],
                               'produto':produto,
                               'unidade':unidade,
                               'data':data,
                               'valor':valor,
                               'period':period})
        
        tab_tarifas = tab_tarifas.append(tabela, ignore_index = True)
        k = k + 1
tab_tarifas.to_sql('tarifas_cooperativacredito',engine,schema='temp',if_exists='fail',index=True)
