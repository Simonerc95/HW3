## Parsing the HTML pages

# After creating the function parse, contained in parser_utils, we just run the parser over the path that contains the complete databse of the 30000 articles. The parser elaborates each article (wiki page) with the BeautilfulSoup package, and all the info needed (title, intro, ..., Language, Budget) are extracted from the bs object, and added to a tsv file for each article. The function doesn't return anything in the enviroment, but just creates a tsv file for each article, and stores it in another folder, that we called TSV, in the same path given as input.

import parser_utils

path = '...\\Articles' #The address of directory where all html files exist 
parser_utils.parse(path)