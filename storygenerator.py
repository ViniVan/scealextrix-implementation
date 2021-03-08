from plot import plot
from newsapi import NewsApiClient
from noc import triples
from pprint import pprint
import random
import re
#dict_keys(['status', 'totalResults', 'articles'])
#dict_keys(['source', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content'])

function_words = ['the', 'a', 'an', 'he', 'she', 'him', 'it',  'her', 'they', 'them',
                  'we', 'our', 'and', 'but', 'in', 'on', 'at', 'for', 'from', 'to', 'can',
                 'could', 'through', 'of','as', 'yet', 'who', 'or', 'us', 'his', 'has', 'with'
                 ,'is', 'are', 'up', 'down']

initial_action = [tl["BMP"] for tl in triples]
key = 'aa94c60a6c5d4db18eb76c9931b329f7'
newsapi = NewsApiClient(api_key = key)
data = newsapi.get_top_headlines(language= 'en', page_size= 20)

headlines = [article['description'].lower() for article in data['articles']]
random.shuffle(headlines)
headlines_by_word =  [re.findall(r"[\w']+", hl) for hl in headlines] 


for hl in headlines_by_word:
    for word in hl:
        if(word.lower() in function_words):
            hl.remove(word)


found_action= "no encontre nada"
found_hl = None
is_looping = True
for hlw in headlines_by_word: ## 20   peor caso ~660000
    for word in hlw: ##15
        for action in initial_action: #2200?
            index = action[0].find(word)
            if (index != -1 and len(word) <= len(action[0]) +1 and len(word) >= len(action[0]) -1 ):
                found_action = action[0]
                found_index = headlines_by_word.index(hlw)
                is_looping = False
        if not is_looping:
            break
    if not is_looping:
        break

while (True):
    try:
        size = int(input("Introduzca la longitud de la historia en tripletas\n"))
    except ValueError:
        print("Introduce un número por favor")
        continue
    else:
        break

antagonist_bool = True
while (True):
    antagonist = input("Desea obtener el antagonista de manera inteligente? y -> SÍ, cualquier otra tecla -> NO\n")
    if (antagonist == 'y' or antagonist == 'Y'):
        antagonist_bool = False
        break
    

print("La acción escogida es: " + found_action + "\n"
     "Ya que se encontró el siguiente titular:\n" , headlines[found_index], "\n")

story = plot(found_action, size, antagonist_bool)

print( "La historia producida es la siguiente: \n")
pprint(story["story"])
print("\nEl esqueleto de la trama es: ", story["plot"].replace('.',','))
if (story["Category"] != None):
    print("\nSe escogio a " + story["A"] + " como A porque pertenece a la categoría: " + story["Category"])
else:
    print("\nSe escogio a " + story["A"] + " a l azar ya que no hay una categoría para la primera acción")
print("\nB es "+ story["B"])
print("\n" + story["report"])

