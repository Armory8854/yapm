from .parser import dictCreation, urlPagination
from .db import initDB, newPodcastSourceDB

def newPodcastSource(db_file, new_podcast_source):
    values = urlPagination(db_file, new_podcast_source)
    entries = values[0]
    podcast_title = values[1]
    podcast_image = values[2]
    newPodcastSourceDB(db_file, podcast_title, new_podcast_source, podcast_image)
    
