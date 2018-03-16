# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 08:30:38 2016

@author: Henrique
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import pandas as pd
import sqlalchemy as sql
import re
import time
import json
import requests as req
from bs4 import BeautifulSoup as bs
from pandas.io.json import json_normalize
import csv 
from sqlalchemy import create_engine
import psycopg2


# Driver
engine = create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')
# Driver
driver = webdriver.Chrome('C:\\Users\paulohmb\Documents\chromedriver.exe')
wait = WebDriverWait(driver, 20)

#########################################################################################################
# Banco Comercial
#########################################################################################################
driver.get("http://www4.bcb.gov.br/fis/cosif/rest/buscar-instituicoes_app.asp#?segmentoId=2")
#### Armazenando os links e CNPJs
time.sleep(1)
link = driver.find_elements_by_xpath('//a[@class="ng-binding ng-scope"]')
cnpj = []
for i in range(len(link)):
    link[i] = link[i].get_attribute("href")
    cnpj.append(re.search("[0-9]*$", link[i]).group(0))

orgaos= []
cadastrobanco = pd.DataFrame()
for i in range(len(cnpj)):
    print(i)
    driver.get('https://www3.bcb.gov.br/informes/rest/cadastros/pessoa-juridica/%s'%(cnpj[i]))
    soup = bs(driver.page_source,"html5lib")
    data = json.loads(soup.find("body").text)   
    for key, value in data.items():
        temp = [key,value]
        orgaos.append(temp)
    df = pd.DataFrame({
                       'Banco':cnpj[i],
                       'cadastro':orgaos
                       })
    cadastrobanco= cadastrobanco.append(df)
    orgaos= []
    
#cooperativa credito
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

orgaos= []
cadastrocoop = pd.DataFrame()
for i in range(len(cnpj)):
    print(i)
    driver.get('https://www3.bcb.gov.br/informes/rest/cadastros/pessoa-juridica/%s'%(cnpj[i]))
    soup = bs(driver.page_source,"html5lib")
    data = json.loads(soup.find("body").text)   
    for key, value in data.items():
        temp = [key,value]
        orgaos.append(temp)
    df = pd.DataFrame({
                       'Banco':cnpj[i],
                       'cadastro':orgaos
                       })
    cadastrocoop= cadastrocoop.append(df)
    orgaos= []
    





### Criando tabelas que serão exportadas


### Começando a tirar os dados dos bancos
driver.get("http://www4.bcb.gov.br/fis/cosif/rest/buscar-instituicoes_app.asp#?segmentoId=2")
#### Armazenando os links e CNPJs
time.sleep(1)
link = driver.find_elements_by_xpath('//a[@class="ng-binding ng-scope"]')
cnpj = []
for i in range(len(link)):
    link[i] = link[i].get_attribute("href")
    cnpj.append(re.search("[0-9]*$", link[i]).group(0))

#### Criando listas de cadatros
endereco= []
tarifas = []
telefones = []
nat_jur = []
tipo = []
situacao = []
auditor = []
end_eletr = []
codigo = []

j=0
#### Aqui entraremos em cada um dos bancos
for j in range(len(link)):
    ##### Entrando no site e na frame certa
    driver.get(link[j])
    driver.refresh()
    time.sleep(1)
    driver.switch_to_frame(driver.find_element_by_class_name("iframeapp"))
    ##### Aqui pego os dados de cadastro
    try:
        endereco.append(driver.find_element_by_partial_link_text('rua').text)
    except:
        endereco.append("nao_possui")
    try:    
        telefones.append(driver.find_element_by_xpath('//span[@ng-show="instituicao.telefone"]').text)
    except:
        telefones.append("nao_possui")
    try:        
        codigo.append(driver.find_element_by_xpath('//span[@ng-show="instituicao.codigoCompensacao"]').text)
    except:
        codigo.append("nao_possui") 
    try:
        end_eletr.append(driver.find_element_by_xpath('//span[@ng-show="instituicao.endereco.enderecoEletronico"]').text)
    except:
        end_eletr.append("nao_possui")        
    nat_jur.append
    tipo.append
    situacao.append
    auditor.append
    endereco.append
    ##### Armazena o link das Tarifas para mais tarde
    if elem_existe('//a[@title = "Tarifas"]'):
        tarifas.append(driver.find_element_by_xpath('//a[@title = "Tarifas"]').get_attribute('href'))
    else:
        tarifas.append('sem_tarifas')
        
    ##### Órgãos Estatutários
    if elem_existe("//a[contains(@ng-click,'mostraOrgaos')]"):
        driver.find_element_by_xpath("//a[contains(@ng-click,'mostraOrgaos')]").click()        
        orgaos = driver.find_element_by_xpath('//select[@ng-model="orgao"]')
        if len(orgaos.find_elements_by_xpath('option')) == 1:
            tabela = driver.find_element_by_xpath('//div[@ng-show="mostraOrgaos"]/table/tbody')
            cpf   = []
            nome  = []
            cargo = []        
            for l in tabela.find_elements_by_xpath('tr'): # Ou seja, para cada linha
                cpf.append(l.find_element_by_xpath('td[1]').text)
                nome.append(l.find_element_by_xpath('td[2]').text)
                cargo.append(l.find_element_by_xpath('td[3]').text)
            cpf   = pd.Series(cpf)
            nome  = pd.Series(nome)
            cargo = pd.Series(cargo)
            tabela = pd.DataFrame({'banco':cnpj[j],
                                   'orgao':orgaos.find_element_by_xpath('option').text,
                                   'cpf':cpf,
                                   'nome':nome,
                                   'cargo':cargo})
            tab_orgaos = tab_orgaos.append(tabela, ignore_index = True)            
        else:
            for k in orgaos.find_elements_by_xpath('option'):
                k.click()
                tabela = driver.find_element_by_xpath('//div[@ng-show="mostraOrgaos"]/table/tbody')
                cpf   = []
                nome  = []
                cargo = []        
                for l in tabela.find_elements_by_xpath('tr'): # Ou seja, para cada linha
                    cpf.append(l.find_element_by_xpath('td[1]').text)
                    nome.append(l.find_element_by_xpath('td[2]').text)
                    cargo.append(l.find_element_by_xpath('td[3]').text)
                cpf   = pd.Series(cpf)
                nome  = pd.Series(nome)
                cargo = pd.Series(cargo)
                tabela = pd.DataFrame({'banco':cnpj[j],
                                       'orgao':k.text,
                                       'cpf':cpf,
                                       'nome':nome,
                                       'cargo':cargo})
                tab_orgaos = tab_orgaos.append(tabela, ignore_index = True)
    
    #### Redes de atendimento
    if elem_existe('//div[@ng-show="mostraAgencias"]'):
       redes = driver.find_element_by_xpath('//div[@ng-show="mostraAgencias"]/table/tbody') 
       nome      = []
       endereco2  = []
       municipio = []
       cod_comp  = []
       for l in redes.find_elements_by_xpath('tr'): # Ou seja, para cada linha
           nome.append(l.find_element_by_xpath('td[1]').text)
           endereco2.append(l.find_element_by_xpath('td[2]').text)
           municipio.append(l.find_element_by_xpath('td[3]').text)
           cod_comp.append(l.find_element_by_xpath('td[4]').text)
       nome      = pd.Series(nome)
       endereco2  = pd.Series(endereco2)
       municipio = pd.Series(municipio)
       cod_comp  = pd.Series(cod_comp)
       redes = pd.DataFrame({'banco':cnpj[j],
                             'nome':nome,
                             'municipio':municipio,
                             'edereco': endereco2,
                             'codigo':cod_comp})
       tab_redes = tab_redes.append(redes, ignore_index = True)
       
       ##### Importante para ele carregar o próximo direito.
    driver.get("about:blank")

# Criar essa tabela com as informações de.
telefones = pd.Series(telefones)
nat_jur = pd.Series(nat_jur)
tipo = pd.Series(tipo)
situacao = pd.Series(situacao)
auditor = pd.Series(auditor)
end_eletr = pd.Series(end_eletr)
codigo = pd.Series(codigo)
endereco=pd.Series(endereco)
telefones = telefones.apply(limpar)
codigo = codigo.apply(limpar)
end_eletr = end_eletr.apply(limpar)

tab_cadastro = pd.DataFrame({'cnpj':cnpj, 
                             'telefone':telefones,
                             'natureza_juridica': nat_jur,
                             'endereco':endereco,
                             'tipo': tipo,
                             'situacao': situacao,
                             'auditor':auditor,
                             'endereco_eletronico':end_eletr,
                             'codigo_compensacao': codigo})

##################################################################
# Tarifas
##################################################################
k = 0
for i in tarifas:
    
    if i != 'sem_tarifas':
        # Entra no site
        driver.get(i)
        
        # Criando as listas para as colunas 
        produto = []
        unidade = []
        data    = []
        valor   = []
        period  = []
    
        # Pegando as informações    
        for j in driver.find_elements_by_class_name('fundoPadraoBClaro3'): # Todas as linhas que quero.
            produto.append(j.find_element_by_xpath('td[2]').text)
            unidade.append(j.find_element_by_xpath('td[3]').text)
            data.append(j.find_element_by_xpath('td[4]').text)
            valor.append(j.find_element_by_xpath('td[5]').text)
            period.append(j.find_element_by_xpath('td[6]').text)
        
        # Transformando listas em séries
        produto = pd.Series(produto)
        unidade = pd.Series(unidade)
        data    = pd.Series(data)
        valor   = pd.Series(valor)
        period  = pd.Series(period)
        
        # Criando e empilhando a tabela
        tabela = pd.DataFrame({'banco':cnpj[k],
                               'produto':produto,
                               'unidade':unidade,
                               'data':data,
                               'valor':valor,
                               'period':period})
        
        tab_tarifas = tab_tarifas.append(tabela, ignore_index = True)
        k = k + 1
        
######################
## Exportar para SQL
######################