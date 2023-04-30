import sqlite3

# General DB Functions, mainly executeDB #
## Generic sql query function
def executeDB(db_file,command,values=None,):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    if values == None:
        cur.execute(command)
    else:
        cur.execute(command, values)
    con.commit()
    con.close()    

## The init DB for first runs / testing purposes
def initDB(db_file):
    clear_tables = [ "episodes", "podcasts" ]
    init_podcasts_command = """ CREATE TABLE IF NOT EXISTS podcasts (
        podcast_title TEXT,
        podcast_url TEXT,
        UNIQUE(podcast_url)
    );"""
    init_episodes_command = """ CREATE TABLE IF NOT EXISTS episodes (
        podcast_title TEXT,
        episode_link TEXT,
        episode_title TEXT,
        episode_date TEXT,
        episode_image TEXT,
        downloaded INTEGER,
        UNIQUE(episode_title),
        FOREIGN KEY(podcast_title) REFERENCES podcasts(podcast_title)
    );"""
    for i in clear_tables:
        clear_command = "DROP TABLE IF EXISTS " + i + ";"
        executeDB(db_file, clear_command)

    executeDB(db_file, init_podcasts_command)
    executeDB(db_file, init_episodes_command)


# New Podcast functions #
## Search for all podcast URLS to gather as an array
def gatherPodcastSources(db_file):
    global podcast_sources
    command = "SELECT podcast_url FROM podcasts;"
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    podcast_sources = [row[0] for row in cur.execute(command).fetchall()]
    return podcast_sources

## Inserts new *EPISODES* into the PODCAST table
def insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, episode_image):
    command = "INSERT OR IGNORE INTO episodes(podcast_title, episode_link, episode_title, episode_date, episode_image, downloaded) VALUES (?, ?, ?, ?, ?, ?)"
    values = podcast_title, episode_link, episode_title, episode_date, episode_image, "0"
    executeDB(db_file, command, values)

## Checks for new possible downloads    
def downloadSearch(db_file):
    global new_episodes
    command = "SELECT * FROM episodes WHERE downloaded=0;"
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    new_episodes = cur.execute(command).fetchall()
    return new_episodes

## Updates a podcast as downloaded
def podcastDownloaded(db_file, episode_title):
    command_posted = "UPDATE episodes SET downloaded=1 WHERE episode_title=?"
    executeDB(db_file, command_posted, [episode_title])

## New podcast source
def newPodcastSource(db_file, podcast_title, new_podcast_source):
    command = "INSERT OR IGNORE INTO podcasts(podcast_title, podcast_url) VALUES (?, ?)"
    values = podcast_title, new_podcast_source
    executeDB(db_file, command, values)
