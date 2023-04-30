import requests
import os

def pathCreator(desired_path):
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    else:
        print(desired_path, " Exists")

def mp3Download(podcast_dir, podcast_title, episode_link, episode_title, episode_date):
    global file_path
    r = requests.get(episode_link)
    download_path = str(podcast_dir + "/" + podcast_title + "/")
    file_path = download_path + episode_date + "-" + episode_title + ".mp3"
    pathCreator(download_path)
    if r.status_code == 200:
        with open(file_path, "wb") as f:
            print(f"Downloading {file_path}...")
            f.write(r.content)
    else:
        print(f"Error downloading {file_path}")

    return file_path
