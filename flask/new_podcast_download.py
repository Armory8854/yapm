from bin.parser import dictCreation
from bin.db import initDB, insertEntry, downloadSearch, podcastDownloaded, gatherPodcastSources, gatherSettings
from bin.downloader import pathCreator, mp3Download
from bin.audioProcessing import speedUpAudio, trimAudio

def newPodcastDownload(db_file):
    settings_dict = gatherSettings(db_file)
    podcast_dir = settings_dict['download_dir']
    max_downloads = settings_dict['max_downloads']
    urls_dirty = gatherPodcastSources(db_file)[2]
    urls = [x[0] for x in urls_dirty]
    print(urls)
    for url in urls:
        for i in range(0,max_downloads):
            podcast_title, episode_link, episode_title, episode_date, episode_image = dictCreation(url, i)
            insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, episode_image)

    new_podcasts = downloadSearch(db_file)

    for i in range(len(new_podcasts)):
        podcast_title = new_podcasts[i][0]
        episode_title = new_podcasts[i][2]
        episode_link = new_podcasts[i][1]
        episode_date = new_podcasts[i][3]
        file_path = mp3Download(podcast_dir, podcast_title, episode_link, episode_title, episode_date)
        podcastDownloaded(db_file, episode_title)

    new_podcasts = downloadSearch(db_file)
    print("New Podcasts Left: ", str(len(new_podcasts)))

