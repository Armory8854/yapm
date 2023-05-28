import threading
import requests
import os
import time
from pathlib import Path
from .util import sanitizeNames
from pydub import AudioSegment

def pathCreator(desired_path):
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    else:
        print(desired_path, " Exists")

def fileChecker(desired_file):
    if os.path.isfile(desired_file):
        print("File exists")
        file_exists = True
    else:
        print("File no there")
        file_exists = False
    print(file_exists)
    return file_exists

def opusConversion(input_file, output_file):
    audio = AudioSegment.from_mp3(input_file)
    audio.export(output_file, format='opus')
    os.remove(input_file)

def imageDownload(podcast_title, image_url):
    file_name = str("static/image/" + podcast_title + ".jpg")
    save_path = Path(file_name)
    if fileChecker(save_path) == True:
        exit
    else:
        r = requests.get(image_url, stream=True)
        with open(file_name, 'wb') as f:
            f.write(r.content)
    return file_name

def mp3Download(podcast_dir, episode_title, episode_link, episode_date):
    retries = 0
    max_retries = 3
    retry_delay = 10
    file_path = str(podcast_dir + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".mp3")
    pathCreator(podcast_dir)
    while retries < max_retries:
        try:
            r = requests.get(episode_link)
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(r.content)
                opus_file_path = str(file_path[:-4] + ".opus")
                print("Checking file existence...")
                if fileChecker(file_path) == True:
                    opusThread = threading.Thread(target=opusConversion, args=(file_path, opus_file_path))
                    opusThread.start()
                else:
                    print(f"{episode_title} did not download - perhaps its already been processed?")
                return opus_file_path
            else:
                print("Error, retrying......")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}. Retrying...")
        retries += 1
        time.sleep(retry_delay)
    print(f"Failed to download {episode_link} after {max_retries} retries.")
    return None
            

