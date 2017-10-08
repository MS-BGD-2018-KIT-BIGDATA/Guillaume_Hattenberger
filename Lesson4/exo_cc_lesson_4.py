#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 09:17:16 2017

@author: Guillaume Hattenberger
"""
import requests
import pandas as pd
import numpy as np
import json
import sys
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re
from multiprocessing import Pool
from multiprocessing import Process, Queue, Lock
from functools import partial
import multiprocessing


def getsoup(url):
    
    temp = get_request(url)
    if temp is None :
        raise ValueError('Wrong response from server')
    
    else :
        return BeautifulSoup(temp.text, 'html.parser')

def get_request(url) :
    
    res= requests.get(url)
    if res.status_code == 200:
        return res
    else:
         return None
     
def getjson(url):
    
    temp = get_request(url)
    if temp is None :
        raise ValueError('Wrong response from server')
    
    else :
        try :
            return json.loads(temp.text)
        except Exception as e :         
             raise ValueError('Error during loading Json :',e)

api_url= "https://maps.googleapis.com/maps/api/distancematrix/json?"
# origin ="origins=Washington,DC&destinations=New+York+City,NY
origin ="origins="
destinations="&destinations="

key_access="&key=AIzaSyCWPbjJiSgsL3dX4cXIQNaFCSHWHgx_Tkk"

url_commune="https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"

#soup = getsoup(url_commune)
#selec= soup.find_all('tr',{class:"wikitable sortable jquery-tablesorter"})

#print(selec)


def get_distance (ville1,ville2):
    
#    json_data = getjson(api_url+origin+"mulhouse,fr"+ destinations+"paris,fr"+ key_access)
    json_data = getjson(api_url+origin+ville1+",fr"+ destinations+ville2+",fr"+ key_access)
    return (json_data['rows'][0]['elements'][0]['distance']['value'])




def compute_distance(villes) :
       
    
    #col= ['lyon','paris','marseille','lille','strasbourg','bordeaux']
    df= pd.DataFrame(data=np.zeros((6,6)),index=villes, columns=villes)
    for x in range(0,6) :
        for x1 in range(x,6):
                   
              df.set_value(col[x],col[x1],get_distance(col[x],col[x1]))
    
    print(df)
    df.to_csv('pandas.txt', header=True, index=True, sep=';', mode='a')



compute_distance(['lyon','paris','marseille','lille','strasbourg','bordeaux'])


