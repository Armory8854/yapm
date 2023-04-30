from bin.settings import gatherURL
from datetime import datetime
from bs4 import BeautifulSoup
import feedparser
import json


def jsonPrettyPrint(data):
    json_object = data
    json_pretty = json.dumps(json_object, indent=2)
    print(json_pretty)    

def htmlPrettyPrint(html):
    global html_pretty
    soup = BeautifulSoup(html, 'html.parser')
    html_pretty = soup.get_text()
    return html_pretty

def dateParser(date):
    global parsed_date
    date_string = date
    date_obj = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
    parsed_date = date_obj.strftime('%Y-%m-%d')
    return parsed_date
    
def dictCreation(url, iteration):
    global podcast_dict
    podcast_dict = {}
    d = feedparser.parse(url)
    global podcast_title, episode_link, episode_title, episode_date, episode_image
    podcast_title = d['feed']['title']
    episode_link = d.entries[iteration].enclosures[0]['href']
    episode_title = d['entries'][iteration]['title']
    episode_date = dateParser(d['entries'][iteration]['published'])
#        episode_description = htmlPrettyPrint(d['entries'][iteration]['summary'])
    episode_image = d.feed.image['href']
    return podcast_title, episode_link, episode_title, episode_date, episode_image
