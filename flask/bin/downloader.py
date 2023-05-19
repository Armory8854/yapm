import requests
import os
import time
from .parser import sanitizeNames
from pydub import AudioSegment

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

def opusConversion(input_file, output_file):
    audio = AudioSegment.from_mp3(input_file)
    audio.export(output_file, format='opus')

def mp3Download(podcast_dir, episode_title, episode_link, episode_date):
    retries = 0
    max_retries = 3
    retry_delay = 10
    file_path = str(podcast_dir + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".mp3")
    pathCreator(podcast_dir)
    while retries < max_retries:
        try:
            r = requests.get(episode_link)
            fileChecker(file_path)
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(r.content)
                opus_file_path = str(file_path[:-4] + ".opus")
                opusConversion(file_path, opus_file_path)
                os.remove(file_path)
                return opus_file_path
            else:
                print("Error, retrying......")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}. Retrying...")
        retries += 1
        time.sleep(retry_delay)
    print(f"Failed to download {episode_link} after {max_retries} retries.")
    return None
            
