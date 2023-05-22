import podcastindex
import requests
import time
import hashlib
import json
import configparser

# Set static variables that will always be used. Mainly, config file.
## TODO: Mve to data/
config_file = "bin/api_config.ini"

# For testing purposes
podcast_title = "Linux Unplugged"

def getConfigKeys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    api_key = config.get('api', 'api_key')
    api_secret = config.get('api', 'api_secret')
    api_config = {
        "api_key": api_key,
        "api_secret": api_secret
    }
    return api_config

def setHeaders(api_config):
    api_key = api_config['api_key']
    api_secret = api_config['api_secret']
    current_time = int(time.time())
    data_to_hash = api_key + api_secret + str(current_time)
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
    api_headers = {
        "User-Agent": "YAPM - Yet Another Podcast Manager",
        "X-Auth-Key": api_key,
        "X-Auth-Date": str(current_time), 
        "Authorization": sha_1 
    }
    return api_headers

def setIndex(api_config):
    index = podcastindex.init(api_config)
    return index

def getRequest(r_url):
    api_config = getConfigKeys(config_file)
    api_headers = setHeaders(api_config)
    setIndex(api_config)
    r = requests.get(url=r_url, headers=api_headers)
    response = r.content.decode("utf-8")
    json_response = json.loads(response)
    return json_response

def getPodDesc(podcast_title):
    search_url = str(f"https://api.podcastindex.org/api/1.0/search/bytitle?q={podcast_title}&pretty")
    json_response = getRequest(search_url)
    description = json_response['feeds'][0]['description']
    return description

def getValLink(podcast_title):
    search_url = str(f"https://api.podcastindex.org/api/1.0/search/bytitle?q={podcast_title}&pretty")
    json_response = getRequest(search_url)
    description = json_response['feeds'][0]['description']
    return description

def searchForPodcasts(search_term):
    search_list = []
    search_dict = {}
    max_page_size = 10
    search_url = str(f"https://api.podcastindex.org/api/1.0/search/bytitle?q={search_term}&pretty&max={max_page_size}")
    json_response = getRequest(search_url)
    for feed in json_response['feeds']:
        feed_title = feed['title']
        feed_id = feed['id']
        feed_url = feed['url']
        feed_image = feed['artwork']
        feed_description = feed['description']
        search_dict = {
            'title': feed_title,
            'id': feed_id,
            'feed_url': feed_url,
            'feed_image': feed_image,
            'feed_description': feed_description
        }
        search_list.append(search_dict)
    return search_list

def getPodcastID(podcast_title):
    print(str(f"Searching for {podcast_title} Podcast Index ID..."))
    api_config = getConfigKeys(config_file)
    index = setIndex(api_config)
    results = index.search(query=podcast_title)
    pod_id = results['feeds'][0]['id']
    print(str("Podcast index id: " + str(pod_id)))
    return pod_id

def getPodV4V(pod_id):
    val_url = str(f"https://api.podcastindex.org/api/1.0/value/byfeedid?id={pod_id}&pretty")
    json_response = getRequest(val_url)
    ln_address = json_response['value']['destinations'][0]['address']
    print(str("Podcast main lighting address: " + ln_address))
    return ln_address

def getValLink(podcast_title):
    print(str(f"Searching for {podcast_title} Value Link..."))
    api_config = getConfigKeys(config_file)
    index = setIndex(api_config)
    results = index.search(query=podcast_title)
    print(results['feeds'][0])
    podcast_val_link = results['feeds'][0]['value']
    print(str("Podcast index id: " + str(pod_id)))
    return podcast_val_link 
