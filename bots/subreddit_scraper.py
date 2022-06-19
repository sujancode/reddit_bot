from os import link
import requests
from bs4 import BeautifulSoup
from dependency.database.index import getDatabaseWrapperInstance

db=getDatabaseWrapperInstance()
url="http://redditlist.com/nsfw?page=1"

def run():

    res=requests.get(url)
    soup=BeautifulSoup(res.content,'html.parser')
    div=soup.select('div#listing-parent')

    divs=(div[0].select('div.listing-item a'))

    subreddits=[]
    for links in divs:
        subreddits.append(links.text)

    db.insert("subreddits",{
        "subreddits":subreddits,
        "type":"nsfw"
    })
