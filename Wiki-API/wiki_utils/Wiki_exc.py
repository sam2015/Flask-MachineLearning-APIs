from bs4 import BeautifulSoup
import requests
import re
import operator
import json
#from tabulate import tabulate
import sys
from stop_words import get_stop_words
import numpy as np



def getWordList(url):
    word_list = []
    #raw data
    source_code = requests.get(url)
    #convert to text
    plain_text = source_code.text
    #lxml format
    soup = BeautifulSoup(plain_text,'lxml')

    #find the words in paragraph tag
    for text in soup.findAll('p'):
        if text.text is None:
            continue
        #content
        content = text.text
        #lowercase and split into an array
        words = content.lower().split()

        #for each word
        for word in words:
            #remove non-chars
            cleaned_word = clean_word(word)
            #if there is still something there
            if len(cleaned_word) > 0:
                #add it to our word list
                word_list.append(cleaned_word)

    return word_list





def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', ' ', word)
    return cleaned_word


def createFrquencyTable(word_list):
    #word count
    word_count = {}
    for word in word_list:
        #index is the word
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

#remove stop words
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')

    temp_list = []
    for key,value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list




wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki/"



def wiki_title_extractor(title= "love"):
    url = wikipedia_api_link + title
    response = requests.get(url)
    data = json.loads(response.content.decode("utf-8"))
    titles = [data['query']['search'][i]['title'] for i in range(len(data['query']['search']))]
    return titles



def wiki_content_extractor(title="JK rowling"):
    titles = wiki_title_extractor(title=title)
    bucket = []
    for title in range(len(titles)):
        url = wikipedia_link + titles[title]
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,'lxml')
        for text in soup.findAll('p'):
            bucket.append(text.text.lower())
        moreLine = [clean_word(bucket[i].split('.')[0]) for i in range(len(bucket))]
        spli = [np.array(moreLine[i].split(' ')) for i in range(len(moreLine))]
        frq = createFrquencyTable(np.concatenate(spli))
        sort = sorted(frq.items(), key=operator.itemgetter(1), reverse=True)
        frequency = remove_stop_words(sort)[:30]
    return frequency



