# This script basically takes as first input a number from 1 to 3, by which the search engine is selected:
# 1 for conjunctive query
# 2 for pages ranked with cosine similarity over TfIdf of query and documents
# 3 for the custom one, that computes a score given by the average distances between the query and documents over the variables Run-time, Release Year, Budget, and number of starring actors.
#Both search engine 2 and 3 run on the set of documents given by the conjunctive query.
#Then, it requires the text input and, for search engine 3, additional inputs for budget, runtime, release year and starring actors.
#The output will be an html file (display.html) saved in the current path (given in Functions.py), and automatically opened in a new tab of the browser.

from utils import *

search_engine = input('Choose the search engine model [1-3] (default is 2) : ')

if search_engine == '1':
    Run_SE1()
    
elif search_engine == '3':
    search_engine3()
else:
    Run_SE2()
    