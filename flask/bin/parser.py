#from bin.settings import gatherURL
from datetime import datetime
import dateutil.parser
from bs4 import BeautifulSoup
import feedparser
import json
from opml import OpmlDocument
from pathlib import Path
from .db import gatherPodcastSources, newPodcastSourceDB

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
    date_obj = dateutil.parser.parse(date_string) 
    parsed_date = date_obj.strftime('%Y-%m-%d')
    return parsed_date

def maxDownloadsCheck(feed_len, max_downloads):
    if feed_len < max_downloads:
        max_downloads = feed_len
        print("New max Downloads: " + str(max_downloads))
    return max_downloads

# Looks ugly at first glance. How could I streamline this?
def urlPagination(url, max_downloads, page_number=1):
    d = feedparser.parse(url)
    print(url)
    feed_len = len(d['entries'])
    print(str(f"Max DL: {max_downloads}"))
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
    episode_title = entry['title']
    episode_date = dateParser(entry['published'])
    episode_description = htmlPrettyPrint(entry['description'])
    return episode_link, episode_title, episode_date, episode_description

# This may need looked over again, it seems a lot more complicated than needed. 
def indexMetaGathering(db_file):
    # First define ARRAYS / LISTS to insert together later
    meta_array = []
    titles = []
    images = []
    # Should be made into entries. Also db_urls is not used as of 2023-05-16
    sources = gatherPodcastSources(db_file)
    db_titles = sources[0]
    db_images = sources[1]
    print(db_titles)
    print(db_images)
    # Define the DICT to store all values
    meta_dict = {}
    for i in range(len(db_titles)):
        # First gather the VALUES
        podcast_title = db_titles[i]
        podcast_image = db_images[i]
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


def initOPML(opml_file):
    print("INIT OPML STARTED")
    opml = OpmlDocument(title='YAPM Podcast Subscriptions')
    data_path = Path("./data")
    data_path.mkdir(parents=True, exist_ok=True)
    if not Path(opml_file).exists():
        opml.dump(opml_file, pretty=True)
    else:
        print('OPML FILE EXISTS')

def exportToOPML(db_file, opml_file):
    opml = OpmlDocument() 
    data = gatherPodcastSources(db_file)
    titles = data[0]
    urls = data[2]
    pod_range = range(len(titles))
    if pod_range == 0:
        print("No podcasts to add - try adding some!")
    else:
        for i in pod_range:
            opml.add_rss(
                title=titles[i], 
                text=titles[i],
                xml_url=urls[i]
            )
            opml.dump(opml_file, pretty=True)

def importOPML(db_file, opml_file):
    with open(opml_file, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, features='xml')
    items = soup.find_all("outline")
    for item in items:
        podcast_url = item.get("xmlUrl")
        print(podcast_url)
        podcast_title = item.get("title")
        print(podcast_title)
        newPodcastSourceDB(db_file, podcast_title, podcast_url) 
