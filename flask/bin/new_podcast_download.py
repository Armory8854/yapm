from .parser import dictCreation, sanitizeNames, urlPagination
from .db import initDB, insertEntry, downloadSearch, podcastDownloaded, gatherPodcastSources, gatherSettings
from .downloader import pathCreator, mp3Download

attempts = 0

def newPodcastDownload(db_file):
    settings_dict = gatherSettings(db_file)
    podcast_dir = settings_dict['download_dir']
    max_downloads = settings_dict['max_downloads']
    urls_dirty = gatherPodcastSources(db_file)[2]
    urls = [x[0] for x in urls_dirty]
    for url in urls:
        entries = urlPagination(db_file, url)
        for i in entries: 
            podcast_title, episode_link, episode_title, episode_date, episode_image = dictCreation(url, i)
            insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, episode_image)

    new_podcasts = downloadSearch(db_file)

    for i in range(len(new_podcasts)):
        podcast_title = new_podcasts[i][0]
        episode_title = new_podcasts[i][2]
        episode_link = new_podcasts[i][1]
        episode_date = new_podcasts[i][3]
        file_path = str(podcast_dir + "/" + podcast_title + "/" + episode_date + "-" + sanitizeNames(episode_title) + ".mp3")
        print("Downloading " + podcast_title + " - " + episode_title)
        mp3Download(podcast_dir, podcast_title, episode_link, episode_title, episode_date)
        podcastDownloaded(db_file, episode_title, file_path)

    new_podcasts = downloadSearch(db_file)
    print("New Podcasts Left: ", str(len(new_podcasts)))

