# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 14:03:46 2018

@author: paulohmb
"""
import sqlalchemy as sql
import pandas as pd 

engine = sql.create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')

dftemp =  pd.read_sql('SELECT * FROM temp.cadastro_coopcredito_2017'
                      ,con = engine
                      ,index_col = 'index')

def limpa(coluna):
    sTemp = dftemp[coluna]
    lTemp = list()
    for a in sTemp:
        try:
            i = a.split(sep = ':')
            i = i[1]
            i= i[1:]
            lTemp.append(i)
        except:
            lTemp.append(a)
    dftemp[coluna] = lTemp

limpa('auditor')
limpa('natureza_juridica')
limpa('situacao')
limpa('tipo')
dftemp = dftemp.drop('codigo_compensacao', axis = 1 )
dftemp =  dftemp.drop('fax', axis = 1 )

dftemp.to_sql('cadastro_coopcredito_2017alt', con = engine, schema = 'temp', if_exists='fail')
