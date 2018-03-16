# -*- coding: utf-8 -*-
"""
@author: Paulo Barbosa
Cadastro cooperativa de crédito do Banco central, Auditores independentes e Orgãos estatuarios 
"""
import requests
import json
import pandas as pd
import time
from selenium import webdriver
import sqlalchemy as sql
#caminho arquivos pc e acesso sql
engine = sql.create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')
root = 'C:\\Users\paulohmb\Downloads\\'

#Configurando Driver
caminhoChromedrive = 'C:\\Users\paulohmb\Documents\chromedriver.exe'
driver = webdriver.Chrome(caminhoChromedrive)
url ="http://www4.bcb.gov.br/fis/cosif/rest/buscar-instituicoes_app.asp#?segmentoId=9&inicioPagina=0&inicioPaginaRegime=0"
driver.get(url)
time.sleep(3)

# Armazenando os links e CNPJs. Atenção para o header 
driver.find_element_by_xpath('/html/body/div/buscar-instituicoes/div/div[1]/div[2]/div[2]/div[1]/strong/a').click()
time.sleep(10)
driver.close()
dfTemp = pd.read_csv(root + 'instituicoes.csv', sep = ';',header = 6)           
sCnpj = dfTemp['CNPJ']

#Eliminando strings do CNPJ
sCnpj=sCnpj[sCnpj.str.contains("CNPJ") == False]  
sCnpj=sCnpj[sCnpj.str.contains("RELACAO") == False]

#Construindo dict de instutição
dfInstituicao = pd.DataFrame()
for n in sCnpj:
    print('cnpj:' + n)
    r = requests.get('https://www3.bcb.gov.br/informes/rest/cadastros/pessoa-juridica/'+n)
    jData = json.loads(r.text)
    dfInstituicao = dfInstituicao.append(pd.io.json.json_normalize(jData))
dfInstituicao = dfInstituicao.reset_index(drop= True)

#Criando Tabela auditores 
sCnpj = sCnpj.reset_index(drop=True)
dfAuditores = pd.DataFrame()
dfAuditores['CNPJ'] = sCnpj
dfAuditores['Auditor Independente'] =  dfInstituicao['auditorIndependente']

#Criando Tabela Orgãos
i=0
dfOrgao = pd.DataFrame()
dfOrgao['tipo'] = []
orgao = dfInstituicao['orgaos']
for n in orgao:
    a = orgao.iloc[i]
    for d in a:
        dfOrgao = dfOrgao.append(pd.DataFrame.from_dict( d['administradores']))
        dfOrgao = dfOrgao.fillna(d['nome'])
    i= i+1
    
#Jogando para o sql,checar argumento if_exists
dfOrgao.to_sql('Orgao_coopcredito_2018',engine,schema = 'temp', if_exists = 'fail')
