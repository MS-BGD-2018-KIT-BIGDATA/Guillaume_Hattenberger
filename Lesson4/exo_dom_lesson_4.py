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

def print_type(x) :
    print(type(x))
    


def get_stars_mean_from_name_2(args):
      
    name = args[0]
    queue = args[1]
    
    url="https://api.github.com/users/"+name+"/repos"
    url+="?access_token=a302fa9f5baac580abf0b50b4daecd8354d23f72"
   
    
    json_data = getjson(url)
        
    stars=[]
    [stars.append(x['stargazers_count']) for x in list(json_data)]
    stars= np.asarray(stars)
               
    print(stars.mean())
    queue.put([name, stars.mean()])
    return (name, stars.mean())
    #q.put([name, stars.mean()])
    
    
    
def get_request(url) :
    
    res= requests.get(url)
    if res.status_code == 200:
        return res
    else:
         return None
     
        
def getsoup(url):
    
    temp = get_request(url)
    if temp is None :
        raise ValueError('Wrong response from server')
    
    else :
        return BeautifulSoup(temp.text, 'html.parser')
       
def getjson(url):
    
    temp = get_request(url)
    if temp is None :
        raise ValueError('Wrong response from server')
    
    else :
        try :
            return json.loads(temp.text)
        except Exception as e :         
             raise ValueError('Error during loading Json :',e)


def retrieve_top_users(soup):
    
    users={}
    tr_ = soup.select("div article table tbody tr")
    print (tr_)
    for x in tr_ :
        users[x.select("td a")[0].text.strip()]=0
 
    return users


def test_multi (soup) :
    
    m = multiprocessing.Manager()
    q = m.Queue()
    top_users = retrieve_top_users(soup)
    test_dict={}
    name_queue = [x for x in top_users.keys()]
    name_queue= name_queue[0:20]
    
    pool = multiprocessing.Pool(processes = 6)
    result = pool.map_async(get_stars_mean_from_name_2, [(x, q) for x in name_queue ])
    
    while not q.empty():
        print( q.get())
    print (result.get())
 
    
        

acces_token= "a302fa9f5baac580abf0b50b4daecd8354d23f72"
url_root= "https://gist.github.com/paulmillr/2657075?"


soup = getsoup(url_root+acces_token)

test_multi(soup)