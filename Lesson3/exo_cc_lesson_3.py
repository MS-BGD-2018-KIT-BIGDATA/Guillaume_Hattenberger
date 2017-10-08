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
         #print(res.text)
         return soup
    else:
         return None

def trim_tranform_func(x):
    return int(x.text.strip().replace(' ',''))

def extract_newPrice(soup):
           
    classname="fpPrice price"
    share_content = soup.find_all(class_=classname)
    price=share_content[1].text.strip().replace('€','.').replace(',','.')
    
    return price

def extract_oldPrice(soup):
    
    classname="fpStriked"
    share_content = soup.find_all(class_=classname)
    price=share_content[-1].text.strip().replace('€','').replace('*','').replace(',','.')
    
    return price
#(list(map(trim_tranform_func, share_content)))
    


url_acer="https://www.cdiscount.com/informatique/ordinateurs-pc-portables/acer-pc-portable-aspire-es1-523-15-6-hd-ram-4go/f-10709-nxgl0ef001.html#mpos=1|cd"
#extract_Prices(getsoup(url_acer))
url_del="https://www.cdiscount.com/informatique/ordinateurs-pc-portables/ordinateur-portable-dell-latitude-e6410-core-i7-d/f-1070992-del0002567897987.html?idOffre=112279796#mpos=1|mp"

prices=[]
prices.append([extract_oldPrice(getsoup(url_acer)),extract_newPrice(getsoup(url_acer))])
prices.append([extract_oldPrice(getsoup(url_del)),extract_newPrice(getsoup(url_del))])

print(prices)

df = pd.DataFrame(prices, index=['Acer','Dell'], columns=list(['Old','New']))

print(df)


    
    
    
    
    
    
    