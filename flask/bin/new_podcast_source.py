from .parser import urlPagination
from .db import newPodcastSourceDB, gatherSettings

def newPodcastSource(db_file, new_podcast_source):
    # Change url pagination to make 
    # max_downloads=1
    # by default - this is not needed at all here
    settings_dict = gatherSettings(db_file)
    max_downloads = settings_dict['max_downloads']
    values = urlPagination(db_file, new_podcast_source, max_downloads)
    podcast_title = values[1]
    print(podcast_title)
    newPodcastSourceDB(db_file, podcast_title, new_podcast_source)
    
