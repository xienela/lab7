import re
import requests
from requests.exceptions import MissingSchema




unions = "а, абы, аж, ан, благо, буде, будто, вроде, да, дабы, -даже, едва, ежели, если, же, зато, затем, и, ибо, или, итак, кабы, как, как то, когда, коли, коль, ли, либо, лишь, нежели, но, пока, покамест, покуда, поскольку, притом, причем, пускай, пусть, раз, разве, ровно, сиречь, словно, так, также, тоже, только, точно, хоть, хотя, чем, чисто, что, чтоб, чтобы, чуть, якобы"

def popular_and_uniq_words(counts_words):
    words = {}
    uniq_words = []
    for i,v in counts_words.items():
        if v == 1:
            uniq_words.append(i)
        else:
            words[i]=v
    
    words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
    
      
    
    return " ".join(words) + " Уникальные слова:" + " ".join(uniq_words)
             

def count_words_from_text(text):
    global unions
    if len(text) == 0:
        return "Пустая строка, введите текст"
    
    words_from_text = list(re.findall(r'[A-zА-я]+', text.lower()))
    
    counts_words = {}
    for word in words_from_text:
        if word not in unions:
            counts_words[word] = words_from_text.count(word)
    return popular_and_uniq_words(counts_words)


def get_url(message):
    ans = ''
    try:
        r = requests.get(message)
        if r.status_code == 200:
            ans = 'Сайт доступен'
        else:
            ans = 'Сайт не доступен'
    except MissingSchema:
        ans = 'Вы ввели не сайт'
        
    return ans

