import podcastindex
import config
import requests
import time
import hashlib
import json
from parser import jsonPrettyPrint

api_key = config.api_key
api_secret = config.api_secret


api_config = {
    "api_key": api_key,
    "api_secret": api_secret
}

index = podcastindex.init(api_config)
podcast_title = "Linux Unplugged"

def getPodcastID(podcast_title):
    print("Searching...")
    results = index.search(query=podcast_title)
    pod_id = results['feeds'][0]['id']
    print(pod_id)
    return pod_id

def getPodValue(pod_id):
    current_time = int(time.time())
    data_to_hash = api_key + api_secret + str(current_time)
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
    api_headers = {
        "User-Agent": "YAPM - Yet Another Podcast Manager",
        "X-Auth-Key": api_key,
        "X-Auth-Date": str(current_time), 
        "Authorization": sha_1 
    }
    r = requests.get(url=f"https://api.podcastindex.org/api/1.0/value/byfeedid?id={pod_id}&pretty", headers=api_headers)
    response = r.content.decode("utf-8")
    json_response = json.loads(response)
    ln_address = json_response['value']['destinations'][0]['address']

def getValueTag(podcast_url):
    print("something will go here soon")

pod_id = getPodcastID(podcast_title)
getPodValue(pod_id)