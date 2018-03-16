####################################################################################################################################################################################################################
#Scrrap tabelas quantidade dos contratos por Municipio
#site http://www.bcb.gov.br/pt-br#!/r/micrrural/?path=conteudo%2FMDCR%2FReports%2FqvcMunicipio.rdl&nome=Quantidade%20e%20Valor%20dos%20Contratos%20por%20Munic%C3%ADpio&exibeparametros=true&botoesExportar=true   
# Paulo Barbosa
#####################################################################################################################################################################################################################
#2013-2014
from selenium import webdriver
import os
import time

def load(tempo,msg):
    print('Esperando %s'%(msg))
    time.sleep(tempo)


path_driver = 'C:\\Users\paulohmb\Documents\chromedriver.exe'
driver = webdriver.Chrome(path_driver)
driver.get('http://www.bcb.gov.br/pt-br#!/r/micrrural/?path=conteudo%2FMDCR%2FReports%2FqvcMunicipio.rdl&nome=Quantidade%20e%20Valor%20dos%20Contratos%20por%20Munic%C3%ADpio&exibeparametros=true&botoesExportar=true')

driver.find_element_by_xpath('//*[@id="anoInicio"]/option[4]').click()
load(5,'ano')
driver.find_element_by_xpath('//*[@id="anoFim"]/option[5]').click()

j= 30
i= 2 
while j < 38:
    driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[4]/td[2]/div/button').click()
    sPrograma = driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[4]/td[2]/div/div/ul/li[%s]/label'%(j)).text
    sPrograma = sPrograma.replace('/','-')
    driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[4]/td[2]/div/div/ul/li[%s]/label/input'%(j)).click()
    driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[4]/td[2]/div/button').click()
    print(sPrograma)
    time.sleep(60)
    i = 2
    while i < 29:
        driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).click()
        sRecurso= driver.find_element_by_xpath('//*[@id="cdFonteRecurso"]/option[%s]'%(i)).text
        sRecurso = sRecurso.replace( '/', '-' )
        if i == 18:
            sRecurso = sRecurso+'(1)'
        load(40,sRecurso)
        driver.find_element_by_xpath('//*[@src="/Paginas/Imagens/excel.gif"]').click()
        load(20,'Download')
        os.rename('C:\\Users\paulohmb\Downloads\Quantidade e Valor dos Contratos por Município 23-01-2018.xls','C:\\Users\paulohmb\Downloads\Programa_%s_Recurso_%s(2013-2014).xls'%(sPrograma,sRecurso))
        i = i+1
    driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[4]/td[2]/div/button').click()
    driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[4]/td[2]/div/div/ul/li[%s]/label/input'%(j)).click()
    driver.find_element_by_xpath('//*[@id="parametrosPlaceholder"]/table/tbody/tr[4]/td[2]/div/button').click()
    time.sleep(5)
    j = j+1
