import time
from .parser import dictCreation, urlPagination
from .util import sanitizeNames
from .db import insertEntry, downloadSearch, gatherPodcastSources, gatherSettings, podcastDownloaded
from .downloader import mp3Download

def newPodcastDLInputs(db_file):
    settings_dict = gatherSettings(db_file)
    urls_dirty = gatherPodcastSources(db_file)[2]
    return settings_dict, urls_dirty

def newPodcastDLDB(db_file, settings_dict, urls):
    download_dir = settings_dict['download_dir']
    max_downloads = settings_dict['max_downloads']
    for url in urls:
        values = urlPagination(url, max_downloads)
        entries = values[0]
        podcast_title = values[1]
        podcast_dir = str(download_dir + "/" + podcast_title)
        podcast_image = str("static/image/" + podcast_title + ".jpg")
        for i, entry in enumerate(entries):
            episode_link, episode_title, episode_date, episode_description = dictCreation(entry, i)
            file_path = str(podcast_dir + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".opus")
            insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, podcast_image, episode_description, file_path) 

    new_podcasts = downloadSearch(db_file)
    return new_podcasts
    

def newPodcastDownload(new_podcasts, download_dir, iteration):
    podcast_title = new_podcasts[iteration][0]
    episode_title = new_podcasts[iteration][2]
    episode_link = new_podcasts[iteration][1]
    episode_date = new_podcasts[iteration][3]
    podcast_dir = str(download_dir + "/" + podcast_title)
    file_path = str(podcast_dir + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".mp3")
    print("Downloading " + podcast_title + " - " + episode_title)
    mp3Download(podcast_dir, episode_title, episode_link, episode_date)
    return episode_title, file_path

def downloadNewFunction(db_file):
    print("Attempting new downloads...")
    attempts = 0
    start_time = time.time()
    download_dir = gatherSettings(db_file)['download_dir']
    while attempts < 3:
        try:
            dl_inputs = newPodcastDLInputs(db_file)
            settings_dict = dl_inputs[0]
            urls_dirty = dl_inputs[1]
            new_podcasts = newPodcastDLDB(db_file, settings_dict, urls_dirty)
            for i in range(len(new_podcasts)):
                downloaded_new = newPodcastDownload(new_podcasts, download_dir, i)
                episode_title = downloaded_new[0]
                file_path = downloaded_new[1]
                print(episode_title)
                print(file_path)
                podcastDownloaded(db_file, episode_title, file_path)
            break
        except KeyError:
            attempts += 1
            print("Key error occured - let's try again")
    end_time = time.time()
    duration = end_time - start_time
    print("Duration: " + str(duration)) 