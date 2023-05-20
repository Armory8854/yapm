from .parser import dictCreation, sanitizeNames, urlPagination
from .db import insertEntry, downloadSearch, gatherPodcastSources, gatherSettings
from .downloader import mp3Download

def newPodcastDLInputs(db_file):
    settings_dict = gatherSettings(db_file)
    urls_dirty = gatherPodcastSources(db_file)[2]
    return settings_dict, urls_dirty

def newPodcastDLDB(db_file, settings_dict, urls_dirty):
    download_dir = settings_dict['download_dir']
    max_downloads = settings_dict['max_downloads']
    urls = [x[0] for x in urls_dirty]
    for url in urls:
        values = urlPagination(db_file, url, max_downloads)
        entries = values[0]
        podcast_title = values[1]
        podcast_dir = str(download_dir + "/" + podcast_title)
        podcast_image = values[2]
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