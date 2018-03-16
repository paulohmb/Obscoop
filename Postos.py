# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 14:48:23 2018

@author: paulohmb
"""
import sqlalchemy as sql
import pandas as pd 

engine = sql.create_engine('postgresql://coop:p1e2r3@4@200.144.244.212/coop')
root = 'C:\\Users\paulohmb\Downloads'
pd.read_csv()
dfTemp = pd.read_csv(root +'\\Postos de atendimento.csv', sep = ';',encoding = 'latin-1')

dfTemp.to_sql('Postos_de_atendimento',engine,schema='temp',if_exists='fail')
