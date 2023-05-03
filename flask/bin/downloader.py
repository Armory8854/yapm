import requests
import os

def pathCreator(desired_path):
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    else:
        print(desired_path, " Exists")

def fileChecker(desired_file):
    global file_exists
    if os.path.isfile(desired_file):
        file_exists=True
    else:
        file_exists=False
    return file_exists
        
def mp3Download(podcast_dir, podcast_title, episode_link, episode_title, episode_date):
    global file_path
    r = requests.get(episode_link)
    download_path = str(podcast_dir + "/" + podcast_title + "/")
    file_path = download_path + episode_date + "-" + episode_title + ".mp3"
    pathCreator(download_path)
    file_exists = fileChecker(file_path)
    if file_exists == False:
        if r.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(r.content)
        else:
            print(f"Error downloading {file_path}")
    else:
        print("Episode already downloaded! Moving on...")

    return file_path
