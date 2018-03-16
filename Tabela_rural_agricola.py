# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 10:33:06 2018

@author: paulohmb
"""

import os
import sqlalchemy as sql
import pandas as pd
from unicodedata import normalize
import re
slash = "\\"
#
##Função de retirar pontuação das string
#def remover_acentos(txt):
#    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
#if __name__ == '__main__':
#    from doctest import testmod
#    testmod()
##acessando servidor   
#engine = sql.create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')
#
##Renomeando arquivos
#for root, dirs, files in os.walk("C:\\Users\paulohmb\Documents\Sql\Pecuaria", topdown=False):
#   for name in files:
#       print(name)
#       sNome = remover_acentos(name)
#       sNome = sNome.replace(" ", "")
#       os.rename(root + slash + name,root + slash + sNome)
#Juntando tabelas Pecuaria
i=0
dfPecuariatemp = pd.DataFrame()
for root, dirs, files in os.walk("C:\\Users\paulohmb\Documents\Sql\Pecuaria", topdown=False):
   for name in files:
        temp = pd.read_csv(root + slash + name, sep = ';', header  = 10,encoding='latin -1')
        temp = temp.dropna(axis=1, how='all')
        temp = temp.dropna(how='all')
        temp = temp.dropna(thresh=2)
        print(name,i)
        temp['Modelo'] = name
        dfPecuariatemp = dfPecuariatemp.append(temp)
#        dftemp.to_sql('ContratosFinal',engine,schema='temp',if_exists='replace',index=True)
        i=i+1
#renomeando colunas Pecuaria 
dfPecuariatemp = dfPecuariatemp.rename(index = str, columns={'IF':'Instituicao'})

#Criando coluna programa
#a expressão ?<=... olha apensa para frente do...
i = 0
lPrograma = list()
for a in dfPecuariatemp['Modelo']:
    print(a)
    sPrograma=dfPecuariatemp.iloc[i,5]
    sPrograma = re.findall('(?<=\()(.*)(?=\)Modalidade)', sPrograma)
    lPrograma.append(sPrograma[0])
    i = i+1
dfPecuariatemp['Atividade'] = lPrograma
####################################################################################################
i = 0
lRecurso = list()
for a in dfPecuariatemp['Modelo']:
    print(a)
    sRecurso=dfPecuariatemp.iloc[i,5]
    sRecurso = re.findall('(?<=Modalidade_)(.*)(?=_Produto)', sRecurso)
    lRecurso.append(sRecurso[0])
    i = i+1
dfPecuariatemp['Modalidade'] = lRecurso
#####################################################################################################
i = 0
lano = list()
for a in dfPecuariatemp['Modelo']:
    print(a)
    sano=dfPecuariatemp.iloc[i,5]
    sano = re.findall('(?<=\(20)(.*)(?=\)\.csv)', sano)
    lano.append(sano[0])
    i = i+1
dfPecuariatemp['Ano'] = lano
#Excluindo modalidade
dfPecuariatemp = dfPecuariatemp.drop(['Modelo'],axis = 1)
#substituindo nan
dfPecuariatemp = dfPecuariatemp.fillna(0)
i=0
for a in dfPecuariatemp['Produto']:
    if a != 0:
        replace = dfPecuariatemp.iloc[i,0]
        i= i+1
        print(replace,i)
    else:
        dfPecuariatemp.iloc[ i, 0] = replace
        i = i+1
i=0
for a in dfPecuariatemp['Segmento']:
    if a != 0:
        replace = dfPecuariatemp.iloc[i,1]
        i= i+1
        print(replace,i)
    else:
        dfPecuariatemp.iloc[ i, 1] = replace
        i = i+1
i=0
for a in dfPecuariatemp['Instituicao']:
    if a != 0:
        replace = dfPecuariatemp.iloc[i,2]
        i= i+1
        print(replace,i)
    else:
        dfPecuariatemp.iloc[ i, 2] = replace
        i = i+1

#Juntando tabelas Pecuaria
i=0
dfAgritemp = pd.DataFrame()
for root, dirs, files in os.walk("C:\\Users\paulohmb\Documents\Sql\Quantidade e Valor dos Contratos de custeio Agricola por Segmento", topdown=False):
   for name in files:
        temp = pd.read_csv(root + slash + name, sep = ';', header  = 10,encoding='latin -1')
        temp = temp.dropna(axis=1, how='all')
        temp = temp.dropna(how='all')
        temp = temp.dropna(thresh=2)
        print(name,i)
        temp['Modelo'] = name
        dfAgritemp = dfAgritemp.append(temp)
#        dftemp.to_sql('ContratosFinal',engine,schema='temp',if_exists='replace',index=True)
        i=i+1
#renomeando colunas Pecuaria 
dfAgritemp = dfAgritemp.rename(index = str, columns={'IF':'Instituicao'})

#Criando coluna programa
#a expressão ?<=... olha apensa para frente do...
i = 0
lPrograma = list()
for a in dfAgritemp['Modelo']:
    print(a)
    sPrograma=dfAgritemp.iloc[i,5]
    sPrograma = re.findall('(?<=\()(.*)(?=\)Modalidade)', sPrograma)
    lPrograma.append(sPrograma[0])
    i = i+1
dfAgritemp['Atividade'] = lPrograma
####################################################################################################
i = 0
lRecurso = list()
for a in dfAgritemp['Modelo']:
    print(a)
    sRecurso=dfAgritemp.iloc[i,5]
    sRecurso = re.findall('(?<=Modalidade_)(.*)(?=_Produto)', sRecurso)
    lRecurso.append(sRecurso[0])
    i = i+1
dfAgritemp['Modalidade'] = lRecurso
#####################################################################################################
i = 0
lano = list()
for a in dfAgritemp['Modelo']:
    print(a)
    sano=dfAgritemp.iloc[i,5]
    sano = re.findall('(?<=\(20)(.*)(?=\)\.csv)', sano)
    lano.append(sano[0])
    i = i+1
dfAgritemp['Ano'] = lano
#Excluindo modalidade
dfAgritemp = dfAgritemp.drop(['Modelo'],axis = 1)
#substituindo nan
dfAgritemp = dfAgritemp.fillna(0)
i=0
for a in dfAgritemp['Produto']:
    if a != 0:
        replace = dfAgritemp.iloc[i,0]
        i= i+1
        print(replace,i)
    else:
        dfAgritemp.iloc[ i, 0] = replace
        i = i+1
i=0
for a in dfAgritemp['Segmento']:
    if a != 0:
        replace = dfAgritemp.iloc[i,1]
        i= i+1
        print(replace,i)
    else:
        dfAgritemp.iloc[ i, 1] = replace
        i = i+1
i=0
for a in dfAgritemp['Instituicao']:
    if a != 0:
        replace = dfAgritemp.iloc[i,2]
        i= i+1
        print(replace,i)
    else:
        dfAgritemp.iloc[ i, 2] = replace
        i = i+1

dfProdutostemp = pd.DataFrame()
dfProdutostemp = dfProdutostemp.append(dfAgritemp)
dfProdutostemp = dfProdutostemp.append(dfPecuariatemp)

engine = sql.create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')
dfProdutostemp.to_sql('Credito_Rural_por_Atividade_Instituicao',engine,schema='temp',if_exists='replace',index=True)
dfProdutostemp = dfProdutostemp[dfProdutostemp.Instituicao != 'Total']
