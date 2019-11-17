import os
import csv
from bs4 import BeautifulSoup
import pandas as pd
import requests as rq
import time
import random
import unicodedata
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import *
import string
import re
from math import *
import json
from collections import defaultdict
from scipy import spatial
import heapq

path = os.curdir
with open(path + "\\WORDS\\vocabulary.json", encoding = "utf-8") as fd:
        vocabulary = json.load(fd)
with open(path + "\\WORDS\\Inverted_index.json", encoding = "utf-8") as fd:
        inverted_index = json.load(fd)
reverse_voc = reverse_voc = {v:k for k,v in vocabulary.items()}

with open(path + "\\WORDS\\DocWords.json", encoding = "utf-8") as fd:
        docwords = json.load(fd)
inv_ind_tfIDF= json.loads(open(path + "\\WORDS\\TfIdf_inv_index.json", encoding = 'utf-8').read())

with open(path + "\\tsvs.json", encoding = "utf-8") as fd:
        newdict = json.load(fd)

with open(path+'\\AllMovies.json', encoding = "utf-8") as fd:
        Movies= json.load(fd)
def clean(text, stop_words = set(stopwords.words('english')), stemmer = PorterStemmer()):
    
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

def savetojson(pathfile, obj):
    with open(pathfile, "w" ,encoding="utf-8") as out_file:
        out_file.write(json.dumps(obj, ensure_ascii = False))
        out_file.close()

def get_query_index(query) :
    indexes = []
    for i in range(len(query)) :
        if query[i] in vocabulary.values() : #if the vocab in query exist in vocabulary dataset
            indexes.append(reverse_voc[query[i]]) #add term_id of that vocab to query

        else : #if it does not exist in vocabulary we replace it with 0
            indexes.append('NA')
    return(indexes)


def execute_query(query):
    if len(query) == 0:
        return('Please, insert text in your search')
    query = get_query_index(query)
    docs = []
    for i in query :
        if (i == 'NA') : 
#if there is a vocab in query that does not exist in vocabulary dataset, there isn't a match and we should terminate the function
            return("No match for your query")
        else :
            docs.append(set(inverted_index[i]))
        
    docs = set.intersection(*docs)
    return(docs)

def Linked_URL(val): #we will use this to make the urls in output clickable
        # target _blank to open new window
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)
    
def replacer(val):      #This is used to escape the character $ in the output for Intro,
    return val.replace('$', '\$')      #otherwise it would be interpreted by displayer

def get_results(query):
    results = []
    for file in execute_query(query):
        docid = file.split('_')[1]
        tsv = []
        with open(path2+"article_" + docid + ".tsv", encoding = "utf-8") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for row in rd:
                if row :
                    tsv.append(row)
        data = tsv[1]
        results.append([docid,data[0],data[1],Movies[docid]])  #create movies file before
        opentsv.close()
    result = pd.DataFrame(results, columns = ['Id','Title', 'Intro', 'Wikipedia Url'])
    return result

def cosine_similarity(a,b):
    return 1 - cosine_distance(a,b)

def querytf(query):
    qtf = dict()
    for word in query :
        term_id = reverse_voc[word]
        try :
            qtf[term_id] += 1/len(query)
            
        except :
            
            qtf[term_id] = 1/len(query)
    return(qtf)

def execute_SE2(query) :
    results = get_results(query)
    ids = get_query_index(query)
    wordtf = defaultdict(list)
    for i in results['Id']:
        doc = 'document_'+str(i)
        for term in ids:
            for docs in inv_ind_tfIDF[term]:
                if docs[0] == doc:
                    wordtf[i].append(docs[1])
        
    return(wordtf)