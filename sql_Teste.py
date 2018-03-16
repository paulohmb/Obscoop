# -*- coding: utf-8 -*-
"""
Autor: Paulo Barbosa

"""
import os
import sqlalchemy as sql
import pandas as pd
from unicodedata import normalize
import re
#################################################################################################################################
#Função de retirar pontuação das string
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
if __name__ == '__main__':
    from doctest import testmod
    testmod()
#################################################################################################################################
#acessando servidor   
engine = sql.create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')
#################################################################################################################################
#Renomeando arquivos
for root, dirs, files in os.walk("C:\\Users\paulohmb\Documents\Sql\Quantidade e Valor dos Contratos por Município"
                                 , topdown=False):
   for name in files:
       slash = "\\"
       print(name)
       sNome = remover_acentos(name)
       sNome = sNome.replace(" ", "")
       os.rename(root + slash + name,root + slash + sNome)
#################################################################################################################################
#Juntando tabelas
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
#renomeando colunas
dftemp = dftemp.rename(index = str, columns={'Unnamed: 3':'Municipio'
                                             ,'Unnamed: 5':'Estado'
                                             ,'Unnamed: 6':'Codmun'
                                             ,'Unnamed: 7':'Atividade'})
vModelo = dftemp['Modelo']
############################################################################################################################################
#Criando coluna programa
#A expressão ?<=... olha apensa para frente do...
i = 0
lPrograma = list()
for a in dftemp['Modelo']:
    print(a)
    sPrograma=dftemp.iloc[i,14]
    sPrograma = re.findall('(?<=Programa_)(.*)(?=_Recurso)', sPrograma)
    lPrograma.append(sPrograma[0])
    i = i+1
dftemp['Programa'] = lPrograma
############################################################################################################################################
i = 0
lRecurso = list()
for a in vModelo:
    print(a)
    sRecurso=dftemp.iloc[i,14]
    sRecurso = re.findall('(?<=Recurso_)(.*)(?=\(2)', sRecurso)
    lRecurso.append(sRecurso[0])
    i = i+1
dftemp['Recurso'] = lRecurso
#################################################################################################################################
i = 0
lano = list()
for a in vModelo:
    print(a)
    sano=dftemp.iloc[i,14]
    sano = re.findall('(?<=\()(.*)(?=\)\.csv)', sano)
    lano.append(sano[0])
    i = i+1
dftemp['Ano'] = lano
#################################################################################################################################
#removendo Total e coluna Modelo
dftemp = dftemp.drop(['Modelo'],axis = 1)
dftemp = dftemp[dftemp.Atividade != 'Total']
#################################################################################################################################
#substituindo nan
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
dftemp.to_sql('ContratosFinal',engine,schema='temp',if_exists='replace',index=True)