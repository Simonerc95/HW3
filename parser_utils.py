import os
import csv
from bs4 import BeautifulSoup

def parse(path) :
    for i in range(30000):
        article = open(path+'\\article_'+str(i)+'.html', 'r')
        soup = BeautifulSoup(article, 'html.parser')
        d = {}
        try:
            for x in soup.find('table', class_="infobox vevent").find('th').find_all_next('th'):
                d[x.text] = unicodedata.normalize('NFKD',x.next_sibling.get_text(separator = '<br/>').replace('<br/>', ',').strip())
        except:
             pass
            
            
        title = str(soup.select('h1')[0].text)

        start = soup.find('p')
        intro = start.text.strip()
        while len(intro) == 0:
            start = start.find_next('p')
            intro = start.text.strip()
        for elem in start.next_siblings:
            if elem.name != 'p':
                break
            intro += elem.text.strip()   

        try:
            start = soup.find('h2').find_next('p')
            plot = start.text.strip()
            for elem in start.next_siblings:
                if elem.name != 'p':
                    break
                plot += elem.text.strip()
        except:
            plot = "NA"




        try :
                director = d['Directed by']
        except: 
                director = "NA"

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


        with open(path+"\\TSV\\article_" + str(i) + ".tsv", "w" ,encoding="utf-8") as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(['title', 'intro', 'plot', 'director', 'producer', 'writer' , 'starring', 'music', 'release_date','run_time', 'country' , 'language' , 'budget'])
                tsv_writer.writerow([title, intro, plot, director, producer, writer , starring, music, release_date,run_time, country , language , budget])
                