#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import csv
from bs4 import BeautifulSoup
import pandas as pd
import requests as rq
import time
import random
import re


# In[ ]:


#for saving wikipedia html files, first we read movie html file and save it as a dataframe, then we get 
#the first column of the dataset and that would be the list of movies urls

def get_movieList (path) :
    movies = pd.DataFrame(pd.read_html(path + "\\movies1.html")[0]) #put the content of html file in a dataframe and get the first column
    movies.drop('Id', inplace=True, axis = 1)
    return movies

def save_html(movies) :
    for i in range(len(movies)):
        try:
            response = rq.get(movies.URL[i])
        except rq.exceptions.RequestException as e: #if we got blocked by wiki we apply a time sleep
            print(e)
            time.sleep(20*60 + 30)
            response = rq.get(movies.URL[i])
        soup = BeautifulSoup(response.text, 'html.parser')
        f = open('article_'+str(i)+'.html','w')
        f.write(str(soup))
        f.close()
        time.sleep(random.choice(range(1,6)) #time sleep between each request
                   
                   
                   

