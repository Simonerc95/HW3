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

# getting query from user

def get_query_SE3():
    query = input("insert your query : ")
    query = clean(query)
    q = dict()
    
    year = input("Do you want to specify the release year ? [Y/N] : ").lower()
    if year == "y" :
        year = input("Please, specify the release date : ") 
        q["year"] = year
    else:
        q["year"] = 'NA'
    



    Runtime = input("Do you want to specify the length of the movie? [Y/N] : ").lower()
    if Runtime == "y" :
        Runtime = input("Please, specify the length of the movie : ")
        if re.search('\d', Runtime):
            q['Runtime'] = Runtime
        else:
            return 'Please, enter a valid runtime.'
    else :
        q["Runtime"] = 'NA'


    starring = input("Is number of stars an important factor for you? [Y/N] : ").lower()
    if starring == "y" :
        starring = input("Please, specify if you're looking for a big or small cast [B/S]: ")
        q["starring"] = starring
    else :
        q["starring"] = 'NA'


    budget = input("Is movie budget an important factor for you? [Y/N] : ").lower()
    if budget == "y" :
        q['Budget'] = input("Please, specify the budget of the movie you're looking for : ")
    else :
        q['Budget'] = 'NA'
        
    return query,q

def search_engine3(query, q) :
    
    results = execute_query(query) #running the first search engine to get all query_related documents 
    # Now we should define variables that we want to use to give a new score
    d = defaultdict(dict)
    result_variables = dict() # A dictionary that assigns each document to a dictionary of variables in that document
     # A dictionary that
    for i in results :
        docId = i.split("_")[1] 
        tsv = newdict[docId]


        d[i] = dict()

        if tsv[6] == 'NA':
            d[i]['Starring'] = '-10000'
        else:
            d[i]['Starring'] = str(len(tsv[6].replace('\n', '').strip(',').split(',,')))

        try:
            d[i]['Release Year'] = re.search(r'\d{4}', tsv[8]).group(0)
        except:
            d[i]['Release Year'] = '-10000'

        try:
            d[i]['Runtime']    = re.search(r'\d+.*',tsv[9]).group(0)
        except:
            d[i]['Runtime']    = '-10000'

        #some movies have running time expressed in reels, and the conversion in minutes is not univoque, so we'll just ignore those info
        if re.search(r'min', d[i]['Runtime']):
            d[i]['Runtime'] = re.search(r'\d+[\.|\,|:]*\d*', d[i]['Runtime']).group(0)
            d[i]['Runtime'] = re.search(r'\d+', d[i]['Runtime']).group(0)
        else:
            d[i]['Runtime'] = '-10000'

        try:
            d[i]['Budget']   = re.findall(r'\$.*', tsv[12])[0]
        except:
            d[i]['Budget']  = '-10000'


        if re.search(r'mil', d[i]['Budget']):
            d[i]['Budget']  = str(int(float(re.search(r'\d+[\.|\,]*\d*', d[i]['Budget']).group(0).replace(',', '.'))*10**6))

        elif re.search(r'\,', d[i]['Budget']) or re.search(r'\.', d[i]['Budget']):
            d[i]['Budget'] = re.search(r'(\d+[\,!\.])+\d+', d[i]['Budget']).group(0).replace(',', '').replace('.', '')


        result_variables[docId] = d[i]

        Runtimes = []

    Release_year = []
    Starring = []
    Budget = []

    for i in result_variables.keys() :
        i = 'document_'+str(i)
        Runtimes.append(int(d[i]["Runtime"]))
        Release_year.append(int(d[i]["Release Year"]))
        Starring.append(int(d[i]["Starring"]))
        Budget.append(int(d[i]["Budget"]))
    scores = dict()
    for i in result_variables :
        # calculating score for Running time
        i = 'document_'+ str(i)
        minrun = min(Runtimes)
        maxrun = max(Runtimes)
        if re.search('\d', q['Runtime']):
            run_score = exp(-(int(re.search('\d+', q['Runtime']).group(0)) -int(d[i]['Runtime']))**2/100)
        else:
            run_score = 0


       # calculating score for quantitative Release_year query
        if re.search('\d', q['year']):
            distance = abs(int(d[i]['Release Year']) - int(re.search('\d+',q["year"]).group(0)))
            year_score = exp(-distance/10)
        else:
            year_score = 0


      # calculating score for budget

        if re.search('\d', q['Budget']):
            if re.search(r'mil', q['Budget']):
                Budget  = int(float(re.search(r'\d+[\.|\,]*\d*', q['Budget']).group(0).replace(',', '.'))*10**6)

            elif re.search(r'\,', q['Budget']) or re.search(r'\.', q['Budget']):
                Budget = int(re.search(r'(\d+[\,!\.])+\d+', q['Budget']).group(0).replace(',', '').replace('.', ''))


            budget_score = exp(-abs(int(Budget) - int(d[i]['Budget'])) / 10**5)
        else:
            budget_score = 0

    # calculating score for starring
        maxstar = max(Starring)
        minstar = min(Starring)
        if q['starring'] == 'B':
            starring_score = (maxstar - int(d[i]['Starring']))/(maxstar-minstar)
        elif q['starring'] == 'S':
            starring_score = (int(d[i]['Starring']) - minstar)/(maxstar-minstar)
        else:
            starring_score = 0

        mean_score = 1/4 * (run_score + year_score + budget_score + starring_score)
        scores[i] = (mean_score, i)

    heap = []
    for doc in scores:
        heapq.heappush(heap, scores[doc])
    heap_result = heapq.nlargest(10, heap)
    df = dict()
    for x,z in heap_result:
        y = z.split('_')[1]
        df[y] = newdict[y][0:2]
        df[y].append(Movies[y])
        df[y].append(x)

    df = pd.DataFrame.from_dict(df, orient = 'index', columns=['Title', 'Intro', 'URL', 'Score'])
    return df

