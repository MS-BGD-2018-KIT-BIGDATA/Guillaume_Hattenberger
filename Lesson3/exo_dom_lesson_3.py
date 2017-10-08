#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 09:17:16 2017

@author: Guillaume Hattenberger
"""
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


def getsoup (url):
    res = requests.get(url)
    
    if res.status_code == 200:
         soup = BeautifulSoup(res.text, 'html.parser')
         return soup
    else:
         return None

def trim_tranform_func(x):
    return int(x.text.strip().replace(' ',''))

def extract_ABCDdata(soup):
    
    classname="montantpetit G"
    share_content = soup.find_all(class_=classname)[1:]
    del share_content[1:3]
    del share_content[2:8]
    del share_content[3:5]
    del share_content[4:]
    
    return(list(map(trim_tranform_func, share_content)))
    

temporary_result=[]
rows_name= ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A",\
            "TOTAL DES CHARGES DE FONCTIONNEMENT = B",\
            "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",\
            "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]

for i in range(3,6):
    url='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=201'+str(i)
    temporary_result.append( extract_ABCDdata(getsoup(url)))


temporary_result=np.asarray(temporary_result).transpose()

df = pd.DataFrame(temporary_result, index=rows_name, columns=list(['2013','2014','2015']))

print(df)


    
    
    
    
    
    
    