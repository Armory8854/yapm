import time
from .parser import dictCreation, urlPagination
from .util import sanitizeNames
from .db import insertEntry, downloadSearch, gatherPodcastSources, gatherSettings, podcastDownloaded
from .downloader import mp3Download
from .ntfy import * 
def newPodcastDLInputs(db_file):
    settings_dict = gatherSettings(db_file)
    urls_dirty = gatherPodcastSources(db_file)[2]
    return settings_dict, urls_dirty

def newPodcastDLDB(db_file, settings_dict, urls):
    download_dir = settings_dict['download_dir']
    download_all = settings_dict['download_all']
    max_downloads = settings_dict['max_downloads']
    for url in urls:
        if download_all == 1:
            values = urlPagination(url, "all")
        else:
            values = urlPagination(url, max_downloads)
        entries = values[0]
        podcast_title = values[1]
        podcast_dir = str(download_dir + "/" + podcast_title)
        podcast_image = str("static/image/" + podcast_title + ".jpg")
        for i, entry in enumerate(entries):
            episode_link, episode_title, episode_date, episode_description, episode_chapters = dictCreation(entry, i)
            file_path = str(podcast_dir + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".opus")
            insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, podcast_image, episode_description, file_path, episode_chapters) 

    new_podcasts = downloadSearch(db_file)
    return new_podcasts
    

def newPodcastDownload(new_podcasts, download_dir, iteration):
    podcast_title = new_podcasts[iteration][0]
    episode_title = new_podcasts[iteration][2]
    episode_link = new_podcasts[iteration][1]
    episode_date = new_podcasts[iteration][3]
    print(f"{podcast_title} | {episode_title} | {episode_link} | {episode_date}")
    podcast_dir = str(download_dir + "/" + podcast_title)
    file_path = str(podcast_dir + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".mp3")
    print("Downloading " + podcast_title + " - " + episode_title)
    mp3Download(podcast_dir, episode_title, episode_link, episode_date)
    return podcast_title, episode_title, file_path

def downloadNewFunction(db_file):
    print("Attempting new downloads...")
    attempts = 0
    start_time = time.time()
    download_dir = gatherSettings(db_file)['download_dir']
    ntfy_url = gatherSettings(db_file)['ntfy_url']
    while attempts < 3:
        try:
            dl_inputs = newPodcastDLInputs(db_file)
            settings_dict = dl_inputs[0]
            urls_dirty = dl_inputs[1]
            new_podcasts = newPodcastDLDB(db_file, settings_dict, urls_dirty)
            for i in range(len(new_podcasts)):
                downloaded_new = newPodcastDownload(new_podcasts, download_dir, i)
                podcast_title = downloaded_new[0]
                episode_title = downloaded_new[1]
                file_path = downloaded_new[2]
                podcastDownloaded(db_file, episode_title, file_path)
                ntfyDownloadFinished(ntfy_url, podcast_title, episode_title)
            break
        except KeyError as e:
            attempts += 1
            print("Key error occured - let's try again")
            print(f"Error: {e}")
            ntfyDownloadFailed(ntfy_url)
    end_time = time.time()
    duration = end_time - start_time
    print("Duration: " + str(duration)) 
    ntfyMessage(ntfy_url, str("Downloads finished. Total time " + str(duration) + " Seconds"))