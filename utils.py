#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


import csv
from bs4 import BeautifulSoup
import pandas as pd
import requests as rq
import time
import random
import re
import os
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import *
import string
from collections import defaultdict


# In[ ]:


# collector functions 

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


# In[2]:


# creating index functions
stop_words = set(stopwords.words('english')) 
stemmer = PorterStemmer()

def clean(text):
    text = text.lower()
    words = word_tokenize(text) #devide the text into substrings
    filtered1 = [w for w in words if not w in stop_words] #remove stop words
    filtered2 = list(filter(lambda word: word not in string.punctuation, filtered1))
    filtered3 = []
    for word in filtered2:
        try:
            filtered3 += re.findall(r'\w+', word) 
        except:
            pass
    
    filtered3 = [stemmer.stem(w) for w in filtered3] #stemming
    filtered4 = [c.replace("''", "").replace("``", "") for c in filtered3 ] #removing useless '' and  `` characters
    filtered4 = [f for f in filtered4 if len(f)>1]
    return filtered4


# In[ ]:


def savetojson(pathfile, obj):
    with open(pathfile, "w" ,encoding="utf-8") as out_file:
        out_file.write(json.dumps(obj, ensure_ascii = False))
        out_file.close()


# In[ ]:


#this function gives us 3 json files, first the vocabulary which contains a dictionary of term ids and words
#second the tsvs which containd a dictionary of cleared text of intro and plot for each document
#third docwords which contains a dictionary of tokens of each document
def get_vocab_index(path) :
    allwords = list()
    docwords = dict()
    tsvs = dict()
    vocabulary = dict()
    for i in range(0,30000):
        with open(path+"\\TSV\\article_" + str(i) + ".tsv", encoding = "utf-8") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for row in rd:
                if row :
                    tsv = row
        text = ' '.join([tsv[1],tsv[2]])
        tsvs[i] = tsv
        cleared = clean(text)

        docwords['document_'+str(i)] = cleared
        allwords += cleared
        
        
    allwords = list(set(allwords))
        for i in range(len(allwords)):
            vocabulary[str(i)] = allwords[i]
            
            
            
    savetojson(path+"\\tsvs.json", tsvs)
    savetojson(path + "\\WORDS\\DocWords.json", docwords)
    savetojson(path + "\\WORDS\\vocabulary.json", vocabulary)


# In[ ]:


def get_inverted_index(path) :
    inverted = defaultdict(list)
    
    with open(path + "\\WORDS\\vocabulary.json", encoding = "utf-8") as fd:
        vocabulary = json.load(fd)
        
    reverse_voc = {v:k for k,v in vocabulary.items()} # we need to inverse keys and values of our dictionary
    
# we check for each document and for each word in that doument whether that document exist in inverted dictionary
#or not, and if it didn't exist we add the document number
    for doc in docwords.keys():
        for word in docwords[doc]:
            if not doc in inverted[reverse_voc[word]]:
                inverted[reverse_voc[word]].append(doc)
                
    savetojson(path + "\\WORDS\\Inverted_index.json", inverted)

