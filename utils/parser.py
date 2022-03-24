from tkinter import Entry
from cloud.models import Myword, Link, MapWord
import requests
from bs4 import BeautifulSoup
import re
import utils
from django.db import transaction




URL = "https://google.com"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}
number_of_pages = 10
stoplst = ["google.com", "youtube.com", "twitter.com"]

def new_word(word):
    if Myword.objects.filter(word=word).exists():
        return Myword.objects.get(word=word).map_words.all()
    else:
        print(word)
        Myword.objects.create(word=word)
        parsegoogle(word)

#getting links from google search
def parsegoogle(word):
    global domainlst 
    domainlst = []
    for i in range(number_of_pages):
        url = URL + "/search?hl=en&q=" + word + "&start="+str(i*10)
        parse_google_page(url, word)
        print(f"{i} of {number_of_pages} - {url}")
    parse_links(word)
        

#getting links from a single google result page
def parse_google_page(url, word):
    r = requests.get(url, headers=HEADERS)
    print("requested google search")
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select(r'a')
    urllst = []
    for item in items:
        if isinstance(item.get('href'), str) and item.get('href').startswith("https://"):
            url = item.get("href")
            domain = get_domain(url)
            if domain not in domainlst and domain not in stoplst:
                urllst.append(url)
                domainlst.append(domain)
    urlobjs = [Link(link=url) for url in urllst]
    Link.objects.bulk_create(urlobjs)
    objs = Link.objects.all().order_by("-id")[:len(urlobjs)]
    Myword.objects.last().links.add(*objs)

#parsing li
def parse_links(word):
    dict = {}
    if len(Myword.objects.filter(word=word).all()) > 0:
        links = Myword.objects.filter(word=word)[0].links.all()
    else:
        links = []
    count = 0
    for i in links:
        try:
            #parsing page and saving map_words to the database
            r = requests.get(i.link, headers=HEADERS, timeout=6)
            r.raise_for_status()
            print(f"{count} of {len(links)} - {i.link}") 
            count += 1
            soup = BeautifulSoup(r.text, "html.parser")
            #getting innerhtmls from all headers and paragraphs and counting in a dictionary. Exception for "US" not to confuse with "us"
            for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
                clean = re.sub('\'\’\(\)\"`—”–‘?!.,:\]\[«%', " ",heading.text.strip())
                lst = list(map(str, clean.split()))

                for word in lst:
                    if word == "US":
                        if word in dict:
                            dict[word] +=1
                        else:
                            dict[word] = 1
                    if word.lower() in dict:
                        dict[word.lower()] += 1
                    else:
                        dict[word.lower()] = 1
        except Exception:
            pass
    #saving to database
    from_dict_to_db(dict, word)


def from_dict_to_db(dict, word):
    words = Myword.objects.prefetch_related("map_words").all()
    lst = [MapWord(word=key, frequency=dict[key]) for key in dict]

    MapWord.objects.bulk_create(lst)
    
    print(f"{len(dict)} mapwords created")
    obj = MapWord.objects.all().order_by("-id")[:len(dict)]
    Myword.objects.last().map_words.add(*obj)
    print("mapwords added")

    

    # for key in dict:
    #     print(f"saving word: {key}")
    #     MapWord.objects.create(word=key, frequency=dict[key])
    #     last = MapWord.objects.last()
    #     words.last().map_words.add(MapWord.objects.get(id=last.id))

def show_cloud(word, q):
    words = Myword.objects.filter(word=word).prefetch_related("map_words")
    #for i in Myword.objects.get(word=word).map_words.all():
    lst = []
    for i in words[0].map_words.all():
        lst.append([i.word, i.frequency])
    lst.sort(key=lambda x: x[1], reverse=True)
    minuswords = get_minus_words()
    output = [i for i in lst[:q] if i[0] not in minuswords and i[0] != word]
    minvalue = output[-1][1]
    maxvalue = output[0][1]
    return output, minvalue, maxvalue

# def parse_link(url):
#     r = requests.get(url, headers=HEADERS)
#     return r

def get_words(html):
    pass

def get_minus_words():
    with open("utils/minuswords.txt") as file:
        minuswords = file.read().splitlines()
        return minuswords




def find_nth(haystack, needle, n):
    pos = 0
    for i in range(n):
        pos = haystack.find(needle, pos+1)
    return(pos)

def get_domain(url):
    #start = find_nth(url, "/", 2)
    end = find_nth(url,"/", 3)
    number_of_dots = 0
    symbol = 1
    domain = ""
    while number_of_dots != 2:
        current_symbol = url[end - symbol]
        symbol += 1
        domain += current_symbol
        if current_symbol == "." or current_symbol == "/":
            number_of_dots += 1      
    return domain[::-1][1:]






                
                
               
                
             