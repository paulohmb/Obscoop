####################################################################################################################################################################################################################
#Scrrap tabelas quantidade dos contratos por Municipio
#site http://www.bcb.gov.br/pt-br#!/r/micrrural/?path=conteudo%2FMDCR%2FReports%2FqvcMunicipio.rdl&nome=Quantidade%20e%20Valor%20dos%20Contratos%20por%20Munic%C3%ADpio&exibeparametros=true&botoesExportar=true   
# Paulo Barbosa
#####################################################################################################################################################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import os
import time

def load(a,b):
    print('Carregando %s'%(b))
    time.sleep(a)
# path_driver = caminho do driver

path_driver = 'C:\\Users\paulohmb\Documents\chromedriver.exe'
driver = webdriver.Chrome(path_driver)
wait = WebDriverWait(driver, 20)

#acesso e passando paramentros 
driver.get('http://www.bcb.gov.br/pt-br#!/r/micrrural/?path=conteudo%2FMDCR%2FReports%2FqvcMunicipio.rdl&nome=Quantidade%20e%20Valor%20dos%20Contratos%20por%20Munic%C3%ADpio&exibeparametros=true&botoesExportar=true')
#time.sleep(5)
#driver.find_element_by_xpath('//*[@id="mesInicio"]/option[7]').click()
#time.sleep(5)
#driver.find_element_by_xpath('//*[@id="mesFim"]/option[8]').click()
#time.sleep(5)
#driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[3]/td[2]/div/button').click()
#driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[3]/td[2]/div/div/ul/li[1]/label/input').click()
#driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[2]/td[2]').click()
#time.sleep(5)

           
#Ano 2013/2014         
anoInicio = driver.find_element_by_xpath('//*[@id="anoInicio"]/option[2]').click()
anoFim = driver.find_element_by_xpath('//*[@id="anoFim"]/option[3]').click()

path = 'C:/Users/paulohmb/Downloads/'
file = 'Quantidade e Valor dos Contratos por Município 07-12-2017.xls'
j=3
i=18
while j < 38:
    driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).click()
    sPrograma =driver.find_element_by_xpath('//*[@id="cdPrograma"]/option[%s]'%(j)).text
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
#2014/2015
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

#2015/2016
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
    
#2016/2017
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