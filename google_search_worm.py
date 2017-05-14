from urllib.request import urlopen,Request
import os
import urllib.parse as parse
from bs4 import BeautifulSoup
import re


def url_parser(query):
    edited = parse.quote_plus(query+' site:anidb.net')
    return 'https://www.google.com.tw/search?q='+edited+'&oq='+edited+'&filter=0&aqs=chrome..69i57j69i64.1558j0j9&sourceid=chrome&ie=UTF-8'


def get_content(url):
    req = Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
    try:
        page = BeautifulSoup(urlopen(req).read().decode('utf-8'),"html.parser")
        link = []
        link = page.find(class_='srg').find_all('a',href=re.compile('anidb'),class_=False)
        if link == None:
            link = find(class_='g').find('a',href=re.compile('anidb'),class_=False)
    except AttributeError as e:
        print(e)
    return link

def search(query):
    url = url_parser(query)
    link = get_content(url)
    return link

basedir = './'

for fd in os.listdir(basedir):
    if not os.path.isdir(os.path.join(basedir,fd)):
        print(fd+' is not a dir')
        continue
    if 'anidb' in fd:
        print(fd+' has been tagged')
        continue
    success = False
    results = search(fd)
    for links in results:
        link = links['href']
        print(link)
        if 'anidb.net/a' in link:
            success = True
            print(fd+' Fetched!')
            index=re.findall('(?<=anidb.net/a)[0-9]*',link)
            os.rename(os.path.join(basedir,fd),os.path.join(basedir,fd+'[anidb-'+index[0]+']'))
            break
        elif 'aid=' in link:
            success = True
            print(fd+' Fetched!')
            index=re.findall('(?<=aid=)[0-9]*',link)
            os.rename(os.path.join(basedir,fd),os.path.join(basedir,fd+'[anidb-'+index[0]+']'))
    if not success:
        print(fd+' fetching failed')

