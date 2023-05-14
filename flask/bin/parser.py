#from bin.settings import gatherURL
from datetime import datetime
from bs4 import BeautifulSoup
import feedparser
import json
import re
from .db import gatherPodcastSources, gatherSettings

def jsonPrettyPrint(data):
    json_object = data
    json_pretty = json.dumps(json_object, indent=2)
    print(json_pretty)    

def htmlPrettyPrint(html):
    soup = BeautifulSoup(html, 'html.parser')
    html_pretty = soup.get_text()
    return html_pretty

def dateParser(date):
    date_string = date
    date_obj = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
    parsed_date = date_obj.strftime('%Y-%m-%d')
    return parsed_date

def maxDownloadsCheck(feed_len, max_downloads):
    if feed_len < max_downloads:
        max_downloads = feed_len
        print("New max Downloads: " + str(max_downloads))
    return max_downloads

def urlPagination(db_file, url, max_downloads, page_number=1):
    settings_dict = gatherSettings(db_file)
    max_downloads = settings_dict['max_downloads']
    d = feedparser.parse(url)
    feed_len = len(d['entries'])
    max_downloads = maxDownloadsCheck(feed_len, max_downloads)
    page_size = max_downloads
    podcast_title = d['feed']['title']
    podcast_image = d.feed.image['href']
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    entries = d.entries[start_index:end_index]
    return entries, podcast_title, podcast_image

def dictCreation(entry, iteration):
    episode_link = entry['links'][1]['href']
    print(episode_link)
    episode_title = entry['title']
    print(episode_title)
    episode_date = dateParser(entry['published'])
    print(episode_date)
    return episode_link, episode_title, episode_date
    
def indexMetaGathering(db_file):
    # First define ARRAYS / LISTS to insert together later
    meta_array = []
    titles = []
    images = []
    db_titles, db_images, db_url = gatherPodcastSources(db_file)    
    # Define the DICT to store all values
    meta_dict = {}
    for i in range(len(db_titles)):
        # First gather the VALUES
        podcast_title = db_titles[i][0]
        podcast_image = db_images[i][0]
        # Then, append these to the proper arrays
        titles.append(podcast_title)
        images.append(podcast_image)
    # Finally, add them to the final dict
    for i in range(len(titles)):
        meta_dict = {
            'title':titles[i],
            'image':images[i]
        }
        meta_array.append(meta_dict)
    return meta_array

def sanitizeNames(episode_title):
    chars_to_dash = ["/",":"]
    chars_to_del = ["?","!","."]
    for i in chars_to_dash:
        episode_title = episode_title.replace(i,"-")

    for i in chars_to_del:
        episode_title = episode_title.replace(i,"")
        
    return episode_title
