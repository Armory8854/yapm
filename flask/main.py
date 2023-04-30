from bin.settings import gatherURL
from bin.parser import dictCreation
from bin.db import initDB, insertEntry, downloadSearch, podcastDownloaded
from bin.downloader import pathCreator, mp3Download
from bin.audioProcessing import speedUpAudio, trimAudio

settings_file = "settings/config.ini"
db_file = "data/database.db"
podcast_dir = "/home/celer/Podcasts"
def main():
    urls = gatherURL(settings_file)
    # Comment this out or have it be some kind of one time run thing for production
    initDB(db_file)
    print(urls[0])
    for url in urls:
        for i in range(0,50):
            podcast_title, episode_link, episode_title, episode_date, episode_image = dictCreation(url, i)
            insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, episode_image)

    new_podcasts = downloadSearch(db_file)
    for i in range(len(new_podcasts)):
        podcast_title = new_podcasts[i][0]
        episode_title = new_podcasts[i][2]
        episode_link = new_podcasts[i][1]
        episode_date = new_podcasts[i][3]
        file_path = mp3Download(podcast_dir, podcast_title, episode_link, episode_title, episode_date)
        print(file_path)
#        speedUpAudio(file_path)
#        trimAudio(file_path)
        podcastDownloaded(db_file, episode_title)

    new_podcasts = downloadSearch(db_file)
    print("New Podcasts Left: ", str(len(new_podcasts)))
if __name__ == "__main__":
    main()
