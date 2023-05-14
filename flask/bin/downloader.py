import requests
import os
import time
from .parser import sanitizeNames

def pathCreator(desired_path):
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    else:
        print(desired_path, " Exists")

def fileChecker(desired_file):
    if os.path.isfile(desired_file):
        file_exists=True
    else:
        file_exists=False
    return file_exists

def mp3Download(podcast_dir, podcast_title, episode_link, episode_title, episode_date):
    retries = 0
    max_retries = 3
    retry_delay = 10
    episode_title = sanitizeNames(episode_title)
    download_path = str(podcast_dir + "/" + podcast_title + "/")
    file_path = download_path + episode_date + "-" + episode_title + ".mp3"
    pathCreator(download_path)
    while retries < max_retries:
        try:
            r = requests.get(episode_link)
            file_exists = fileChecker(file_path)
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(r.content)
                return file_path
            else:
                print("Error, retrying......")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}. Retrying...")
        retries += 1
        time.sleep(retry_delay)
    print(f"Failed to download {episode_link} after {max_retries} retries.")
    return None
            
