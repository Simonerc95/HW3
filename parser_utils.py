import os
import csv
from bs4 import BeautifulSoup


def parse(path) :       # Path is the path that contains the complete database of the 30000 articles. 
    for i in range(30000):
        article = open(path+'\\article_'+str(i)+'.html', 'r')
        
# Parse will elaborate each article (wiki page) with bs4 BeautilfulSoup package, and all the info needed (title, intro, ..., Language, Budget) are extracted from the bs object
        soup = BeautifulSoup(article, 'html.parser')   
        d = {}
        try:
            for x in soup.find('table', class_="infobox vevent").find('th').find_all_next('th'):  # in order to find the right information from the infobox, we need to first find all the table headers after the fist th of the infobox, that would be the title
                d[x.text] = unicodedata.normalize('NFKD',x.next_sibling.get_text(separator = '<br/>').replace('<br/>', ',').strip()) # and then find the nextsipblings of each th found, that would be the td associated to each th of the infobox 
        except:
             pass # this condition just ignores pages without infobox, for which the information values we are looking for will all be 'NA'
            
            
        title = str(soup.select('h1')[0].text) 

        start = soup.find('p') #finding the first paragraph, that should be the first paragraph of the intro
        intro = start.text.strip()
        while len(intro) == 0:  #some pages had empty paragraph as first p before intro, so we skip it (or them, if they are more than one)
            start = start.find_next('p')
            intro = start.text.strip()
        for elem in start.next_siblings:
            if elem.name != 'p':   #finding all paragraphs after the first, and stopping at the first non paragraph element, so we get all paragraphs of the intro 
                break
            intro += elem.text.strip()  #adding all p's  found to the intro 

        try:                           #if there is an h2, this should be the plot header, so we start looking for paragraphs from there
            start = soup.find('h2').find_next('p')
            plot = start.text.strip() 
            for elem in start.next_siblings:
                if elem.name != 'p':
                    break
                plot += elem.text.strip() #adding all paragraphs to the plot, as for intro
        except: 
            plot = "NA"



#we check if the infobox of each page has the information we are looking for, and if found, it will be assigned to a variable
        try :
                director = d['Directed by']
        except: 
                director = "NA"
#otherwise, an 'NA' will be assigned to that variable for the current page
        try :
                producer = d['Produced by']
        except: 
                producer = "NA"

        try :

                writer = d["Written by"]
        except:
                writer = "NA"


        try :
                starring = d["Starring"].strip()

        except:
                starring = "NA"

        try :

                music = d["Music by"]
        except :
                music = "NA"

        try :
                release_date = d["Release date"]

        except :

                release_date = "NA"

        try :
                run_time = d["Running time"]

        except :
                run_time = "NA"

        try :
                country = d["Country"]

        except :

                country = "NA"

        try :
                language = d["Language"]

        except:
                language = "NA"

        try :
                budget = d["Budget"]

        except :
                budget = "NA"

#all the variables created from the infobox dictionary are used to build one tsv file for each page, just as they are. The actual parsing and cleaning of these informations will be done during the implementation of the search engines, only for informations used in them.
        with open(path+"\\TSV\\article_" + str(i) + ".tsv", "w" ,encoding="utf-8") as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(['title', 'intro', 'plot', 'director', 'producer', 'writer' , 'starring', 'music', 'release_date','run_time', 'country' , 'language' , 'budget'])
                tsv_writer.writerow([title, intro, plot, director, producer, writer , starring, music, release_date,run_time, country , language , budget])
                