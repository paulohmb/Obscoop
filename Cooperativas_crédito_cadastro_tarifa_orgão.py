# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 02:51:47 2016

@author: Henrique
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import re
import time

# Driver
engine = create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')
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
#########################################################################################################
# Cooperativas
#########################################################################################################

### Criando tabelas que serão exportadas
tab_cadastro = pd.DataFrame()
tab_orgaos   = pd.DataFrame()
tab_tarifas  = pd.DataFrame()
tab_redes    = pd.DataFrame()
### Começando a tirar os dados das cooperativas


#WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'paginacao')))
#
#### Passando pelas páginas e armazenando os links e CNPJs.
#paginas = driver.find_element_by_xpath('//div[@class="paginacao ng-binding"]')
#paginas = re.search("/ [0-9]* ", paginas.text).group(0)
#paginas = int(re.search(" [0-9]* ", paginas).group(0))
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

#/*/*/*/*/*/**/*//*/    
    #for j in range(paginas-1):
for j in range(1):
#driver.find_element_by_xpath('//span[text() = "Próxima"]').click()  
    time.sleep(3)
    link_aux = driver.find_elements_by_xpath('//a[@ng-if="filiacao.s || isConfederacaoNaoFinanceira(filiacao)"]')
    cnpj_aux = []
    for i in range(len(link_aux)):
        link_aux[i] = link_aux[i].get_attribute("href")
        cnpj_aux.append(re.search("[0-9]*$", link_aux[i]).group(0))
    link = link + link_aux
    cnpj = cnpj + cnpj_aux

#### Criando listas de cadatros
tarifas = []
telefones = []
fax = []
nat_jur = []
tipo = []
situacao = []
auditor = []
end_eletr = []
codigo = []
#### Aqui entraremos em cada uma das cooperativas
for j in range(len(cnpj)):
    print(j)
    ##### Entrando no site e na frame certa
    driver.get('http://www4.bcb.gov.br/fis/cosif/rest/mostrar-instituicao.asp#?cnpj='+cnpj[j])
    driver.refresh()
    a = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'iframeapp')))
    driver.switch_to_frame(driver.find_element_by_class_name("iframeapp"))
    
    ##### Aqui pego os dados de cadastro
    
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ng-binding")))
    try:    
        telefones.append(driver.find_element_by_xpath('//span[@ng-show="instituicao.telefone"]').text)
    except:
        telefones.append("nao_possui")
    try:
        fax.append(driver.find_element_by_xpath('//span[@ng-show="instituicao.fax"]').text)
    except:
        fax.append("nao_possui")
    try:        
        codigo.append(driver.find_element_by_xpath('//span[@ng-show="instituicao.codigoCompensacao"]').text)
    except:
        codigo.append("nao_possui") 
    try:
        end_eletr.append(driver.find_element_by_xpath('//span[@ng-show="instituicao.endereco.enderecoEletronico"]').text)
    except:
        end_eletr.append("nao_possui")        
    textos = driver.find_element_by_xpath("//div[@ng-show='mostraSede']").text
    textos = textos.split("\n")[-4:]
    nat_jur.append(textos[0])
    tipo.append(textos[1])
    situacao.append(textos[2])
    auditor.append(textos[3])

    ##### Armazena o link das Tarifas para mais tarde
    if elem_existe('//a[@title = "Tarifas"]'):
        tarifas.append(driver.find_element_by_xpath('//a[@title = "Tarifas"]').get_attribute('href'))
    else:
        tarifas.append('sem_tarifas')
        
    
    ##### Órgãos Estatutários
    #wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@ng-click='mostraOrgaos = !mostraOrgaos']")))
#    while(len(driver.find_elements_by_xpath("//a[@ng-click='mostraOrgaos = !mostraOrgaos']")) == 0):
#        time.sleep(1)
#        print('Aguardando Órgao')
#    if (driver.find_element_by_partial_link_text("Órgãos Estatutários").is_displayed() == 1):
    try:
        driver.find_element_by_xpath("//a[@ng-click='mostraOrgaos = !mostraOrgaos']").click()        
        orgaos = driver.find_element_by_xpath('//select[@ng-model="orgao"]')
        aOrgao = orgaos.find_elements_by_tag_name('option')
        k =0
        for k in range(len(aOrgao)):
            if (not orgaos.is_displayed()):
                wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@ng-click='mostraOrgaos = !mostraOrgaos']")))
                driver.find_element_by_xpath("//a[@ng-click='mostraOrgaos = !mostraOrgaos']").click()        
                aOrgao = orgaos.find_elements_by_tag_name('option')
            aOrgao[k].click()
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
                                   'orgao':aOrgao[k].text,
                                   'cpf':cpf,
                                   'nome':nome,
                                   'cargo':cargo})
            tab_orgaos = tab_orgaos.append(tabela, ignore_index = True)
            #### Redes de atendimento
        if elem_existe('//div[@ng-show="mostraAgencias"]'):
          redes = driver.find_element_by_xpath('//div[@ng-show="mostraAgencias"]/table/tbody') 
          nome      = []
          endereco  = []
          municipio = []
          cod_comp  = []
          for l in redes.find_elements_by_xpath('tr'): # Ou seja, para cada linha
               type(nome)                         
               nome.append(l.find_element_by_xpath('td[1]').text)
               endereco.append(l.find_element_by_xpath('td[2]').text)
               municipio.append(l.find_element_by_xpath('td[3]').text)
               cod_comp.append(l.find_element_by_xpath('td[4]').text)
          nome      = pd.Series(nome)
          endereco  = pd.Series(endereco)
          municipio = pd.Series(municipio)
          cod_comp  = pd.Series(cod_comp)
          redes = pd.DataFrame({'banco':cnpj[j],
                                 'nome':nome,
                                 'municipio':municipio,
                                 'codigo':cod_comp})
          tab_redes = tab_redes.append(redes, ignore_index = True)
    except:
        continue
##### Importante para ele carregar o próximo direito.
driver.get("about:blank")
    
# Criar essa tabela com as informações de.
telefones = pd.Series(telefones)
fax = pd.Series(fax)
nat_jur = pd.Series(nat_jur)
tipo = pd.Series(tipo)
situacao = pd.Series(situacao)
auditor = pd.Series(auditor)
end_eletr = pd.Series(end_eletr)
codigo = pd.Series(codigo)

telefones = telefones.apply(limpar)
fax = fax.apply(limpar)
codigo = codigo.apply(limpar)
end_eletr = end_eletr.apply(limpar)

tab_cadastro = pd.DataFrame({'cnpj':cnpj, 
                             'telefone':telefones,
                             'fax': fax,
                             'natureza_juridica': nat_jur,
                             'tipo': tipo,
                             'situacao': situacao,
                             'auditor':auditor,
                             'endereco_eletronico':end_eletr,
                             'codigo_compensacao': codigo
                             })

##################################################################
# Tarifas
##################################################################
k = 0
for i in tarifas:       
    if i != 'sem_tarifas':
        # Entra no site
        driver.get(i)
        try:
            driver.find_element_by_xpath('html/body/div[2]/div[3]/p[3]/a[1]/span').click()
        except:
            continue
        # Criando as listas para as colunas 
        produto = []
        unidade = []
        data    = []
        valor   = []
        period  = []
    
        # Pegando as informações    
        for j in driver.find_elements_by_class_name('fundoPadraoBClaro3'): # Todas as linhas que quero.
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
        # Transformando listas em séries
        produto = pd.Series(produto)
        unidade = pd.Series(unidade)
        data    = pd.Series(data)
        valor   = pd.Series(valor)
        period  = pd.Series(period)
        
        # Criando e empilhando a tabela
        tabela = pd.DataFrame({'cooperativa':cnpj[k],
                               'produto':produto,
                               'unidade':unidade,
                               'data':data,
                               'valor':valor,
                               'period':period})
        
        tab_tarifas = tab_tarifas.append(tabela, ignore_index = True)
        k = k + 1
#####################
# Exportar para SQL
#####################
tab_cadastro.to_sql('cadastro_coopcredito_2017',engine,schema='temp',if_exists='fail',index=True)
tab_orgaos.to_sql('orgao2017',engine,schema='coop',if_exists='fail',index=True)
tab_tarifas.to_sql('tarifas_cooperativacredito',engine,schema='temp',if_exists='fail',index=True)
tab_redes.to_sql('rede_coopcred_2017',engine,schema='temp',if_exists='fail',index=True)
