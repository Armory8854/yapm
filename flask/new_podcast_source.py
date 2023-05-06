from bin.parser import dictCreation
from bin.db import initDB, newPodcastSourceDB

def newPodcastSource(db_file, new_podcast_source):
    podcast_title = dictCreation(new_podcast_source, 0)[0]
    podcast_image = dictCreation(new_podcast_source, 0)[4]
    newPodcastSourceDB(db_file, podcast_title, new_podcast_source, podcast_image)
    
if __name__ == "__main__":
    main()
    
