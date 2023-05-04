from bin.parser import dictCreation
from bin.db import initDB, newPodcastSource

db_file = "data/database.db"

def main():
    new_podcast_source = input("Enter the rss feed to your new podcast: ")
    podcast_title = dictCreation(new_podcast_source, 0)[0]
    podcast_image = dictCreation(new_podcast_source, 0)[4]
    newPodcastSource(db_file, podcast_title, new_podcast_source, podcast_image)
    
if __name__ == "__main__":
    main()
    
