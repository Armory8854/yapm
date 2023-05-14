from .parser import urlPagination
from .db import newPodcastSourceDB, gatherSettings

def newPodcastSource(db_file, new_podcast_source):
    settings_dict = gatherSettings(db_file)
    max_downloads = settings_dict['max_downloads']
    values = urlPagination(db_file, new_podcast_source, max_downloads)
    entries = values[0]
    podcast_title = values[1]
    podcast_image = values[2]
    newPodcastSourceDB(db_file, podcast_title, new_podcast_source, podcast_image)
    
