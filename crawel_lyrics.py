import pandas as pd
import numpy as np
import requests
import time
import random
import requests
from bs4 import BeautifulSoup
import re
# artists
pagename = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '19']
aname = ['adel','aj','arianagrande','alexander23','avicii','avamax','alessiacara','ashtonirwin','adamlevine']
bname = ['billieeilish','birdy','brunomars','beberexha','bsb','beforeyouexit','beatles']
cname = ['charlieputh','coldplay','clarkson','cleanbandit','cheatcodes','carlyraejepsen']
dname=['dualipa','demilovato','drake']

urll = "https://www.azlyrics.com"
# print ("Default request (it will fail)...")

head =['singer','song','lyrics']
dataset = pd.DataFrame(columns=head)

# make the default request
try:
    r = requests.get(urll)
except requests.exceptions.RequestException as e:
    print (e)

print( "User-Agent request (it will pass)...")
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'cookie': 'cf_clearance=dbae418fe0c6a07fe6280635e7057f44f0c5aeca-1576140663-0-150; __cfduid=de4411bb1db85959721be2c90e1ed0a721576140663;ASP.NET_SessionId=mxu4rworc32oovw3ftckcuo1; _ga=GA1.3.241510402.1576140666; _gid=GA1.3.640675067.1576140666; _gat=1'
    }

lyrics = []
song = []
def get_lyrics(link):
    time.sleep(1)
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    # get the lyrics
    for goods in soup.find_all("div", {"class": None}):
        if len(goods.text) == 0: pass
        lyrics.append(goods.text)

# songs name
for i in range(len(zname)):
    url = "https://www.azlyrics.com/"+pagename[25]+"/"+zname[i]+".html"
    # print(url)
    # make a request for the data
    r = requests.get(url, headers=headers)
    # convert the response text to soup
    soup = BeautifulSoup(r.text, "lxml")
    songs = soup.find_all('div', class_='listalbum-item') #  song name
    singer = []
    for title in songs:
        if title.a != None:
            song.append(title.a.string)
            singer.append(zname[i])

    for url in soup.findAll('a', class_=None):
        address = url.get('href')
        if "www" in address or "https" in address or "../"in address or "#" in address:
            non = 0
        else :
            non = 0
            # print(urll+address)
            get_lyrics(urll+address)

dataset['singer'] = singer
dataset['song'] = song
dataset['lyrics'] = lyrics
dataset.to_csv(r'D:/qiongyun/desktop/crawl/lyrics/data.csv', index = False)
