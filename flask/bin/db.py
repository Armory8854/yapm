import sqlite3
from pathlib import Path

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
    print("DB INIT STARTED")
    data_path = Path("./data")
    data_path.mkdir(parents=True, exist_ok=True)
    db_path = Path(db_file)
    if not db_path.exists():
        clear_tables = [ "episodes", "podcasts", "settings" ]
        init_podcasts_command = """ CREATE TABLE IF NOT EXISTS podcasts(
        podcast_title TEXT,
        podcast_url TEXT,
        podcast_image TEXT,
        UNIQUE(podcast_url)
        );"""
        init_episodes_command = """ CREATE TABLE IF NOT EXISTS episodes(
        podcast_title TEXT,
        episode_link TEXT,
        episode_title TEXT,
        episode_date TEXT,
        episode_image TEXT,
        episode_description TEXT,
        download_dir TEXT,
        downloaded INTEGER,
        UNIQUE(episode_title),
        FOREIGN KEY(podcast_title) REFERENCES podcasts(podcast_title)
        );"""
        init_settings_command = """ CREATE TABLE IF NOT EXISTS settings(
        max_downloads INT,
        download_all INT,
        download_dir STR
        );"""
        default_settings_command = "INSERT INTO settings(max_downloads, download_all, download_dir) VALUES(10,0,'/Podcasts');"
        init_commands = init_podcasts_command, init_episodes_command, init_settings_command

        for i in clear_tables:
            clear_command = "DROP TABLE IF EXISTS " + i + ";"
            executeDB(db_file, clear_command)

        for i in init_commands:
            executeDB(db_file, i)

        executeDB(db_file, default_settings_command)
    else:
        print("DB ALREADY EXISTS")

# New Podcast functions #
## Inserts new *EPISODES* into the PODCAST table
def insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, episode_image, episode_description):
    command = "INSERT OR IGNORE INTO episodes(podcast_title, episode_link, episode_title, episode_date, episode_image, episode_description, downloaded) VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = podcast_title, episode_link, episode_title, episode_date, episode_image, str(episode_description), "0"
    executeDB(db_file, command, values)

## Checks for new possible downloads    
def downloadSearch(db_file):
    global new_episodes
    command = "SELECT * FROM episodes WHERE downloaded=0;"
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    new_episodes = cur.execute(command).fetchall()
    con.close()
    return new_episodes

## Updates a podcast as downloaded
def podcastDownloaded(db_file, episode_title, download_dir):
    episode_title=str(episode_title)
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    command_downloaded = "UPDATE episodes SET downloaded=1 WHERE episode_title=?"
    command_directory = "UPDATE episodes SET download_dir=? WHERE episode_title=?"
    cur.execute(command_downloaded, (episode_title,))
    cur.execute(command_directory, (download_dir, episode_title,))
    con.commit()
    con.close()
    
## New podcast source
def newPodcastSourceDB(db_file, podcast_title, new_podcast_source, podcast_image):
    command = "INSERT OR IGNORE INTO podcasts(podcast_title, podcast_url, podcast_image) VALUES (?, ?, ?)"
    values = podcast_title, new_podcast_source, podcast_image
    executeDB(db_file, command, (values))

## Gather podcast source info from the DB
def gatherPodcastSources(db_file):
    global podcast_title, podcast_image
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    podcast_title = cur.execute("SELECT podcast_title FROM podcasts;").fetchall()
    podcast_image = cur.execute("SELECT podcast_image FROM podcasts;").fetchall()
    podcast_url = cur.execute("SELECT podcast_url FROM podcasts;").fetchall()
    con.close()
    return podcast_title, podcast_image, podcast_url

def gatherDownloadedPodcasts(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    command = "SELECT * FROM episodes WHERE downloaded=1;"
    cur.execute(command)
    downloaded_podcasts = cur.fetchall()
    con.close()
    return downloaded_podcasts
    
# Settings #
## Gather all settings as a dictionary for use anywhere
def gatherSettings(db_file):
    global settings_dict
    settings_dict = {}
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    column_command = "PRAGMA table_info(settings);"
    rows_command = "SELECT * FROM settings;"
    columns_pre = cur.execute(column_command).fetchall()
    rows_pre = cur.execute(rows_command).fetchall()

    for column in range(len(columns_pre)):
        settings_dict.update({columns_pre[column][1]: rows_pre[0][column]})
    con.close()
    return settings_dict

## Udate db, mainly for settings
def updateDB(db_file, max_downloads, download_all, download_dir):
    command = "UPDATE settings SET max_downloads=?, download_all=?, download_dir=?"
    values = max_downloads, download_all, download_dir
    executeDB(db_file, command, (values))

## Keep in mind this should remove all EPISODES too!
def removePodcastSource(db_file, remove_podcast_source):
    source_command = "DELETE FROM podcasts WHERE podcast_title=?"
    episodes_command = "DELETE FROM episodes WHERE podcast_title=?"
    commands = source_command, episodes_command
    for i in commands:
        executeDB(db_file, i, (remove_podcast_source,))