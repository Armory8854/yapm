import threading
import multiprocessing
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
        file_exists = True
    else:
        file_exists = False
    print(f"File exists: {file_exists}")
    return file_exists

def fileDownload(input_file, content):
    with open(input_file, "wb") as f:
        f.write(content)
 

def opusConversion(content, input_file, opus_file_path):
    fileDownload(input_file, content)
    audio = AudioSegment.from_mp3(input_file)
    audio.export(opus_file_path, format='opus')
    try:
        os.remove(input_file)
    except FileNotFoundError as fnfe:
        print(f"{input_file} Not Found: {fnfe}")

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
    max_processes = 3
    processes = []
    file_path = str(podcast_dir + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".mp3")
    pathCreator(podcast_dir)
    while retries < max_retries:
        try:
            r = requests.get(episode_link)
            content = r.content
            opus_file_path = str(file_path[:-4] + ".opus")
            if r.status_code == 200:
                for _ in range(max_processes):
                    opusProcess = multiprocessing.Process(target=opusConversion, args=(content, file_path, opus_file_path))
                    opusProcess.start()
                    processes.append(opusProcess)
                for _ in processes:
                    opusProcess.join()
                return opus_file_path
            else:
                print("Error, retrying......")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}. Retrying...")
        retries += 1
        time.sleep(retry_delay)
    print(f"Failed to download {episode_link} after {max_retries} retries.")
    return None