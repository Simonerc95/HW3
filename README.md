# HW3
## Group-31
Our group consists of these members : 
* Simone Ercolino
* Negin Amininodoushan



you can find an explanation of all files in this repository below :
- collector.py: a python file that contains the lines of code needed to collect our data from the html pages of Wikipedia.

- collector_utils.py: a python file that stores the function we used in collector.py.

* parser.py: a python file that contains the lines of code needed to parse the entire collection of html pages and save those in tsv files.

- parser_utils.py: a python file that stores the function we used in parser.py.

- index.py: a python file that once executed generate the indexes of the Search engines.

- index_utils.py: a python file that contains the functions we used for creating indexes.

- utils.py: a python file that gather functions we used in collector and index files

- main.py: a python file that once executed build up the search engine and execute a query. 

- exercise_4.py: python file that contains the implementation of the algorithm that solves problem 4.

- main.ipynb: a Jupyter notebook explaines the strategies we adopted solving the homework and bonus part.

- databases we used consist of :
    - vocabulary.json : which contains a dictionary that points each term_id to a word
    - doc_words.json : which contains a dictionary that points each document to the words it contains
    - tsvs.json : which contains a dictionary that points each document to intro and section part of it
    -inverted_index.json : which contains a dictionary that poinys each term_id to the documets that have this word
