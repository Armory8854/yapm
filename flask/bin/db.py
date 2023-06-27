import sqlite3
import time
import math
from pathlib import Path
from .downloader import imageDownload
from .podcast_index import getPodDesc, getPodcastID, getPodV4V, getFundingLink
import feedparser

sqlite3.enable_callback_tracebacks(True)
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
    # Establish the data path
    data_path = Path("./data")
    data_path.mkdir(parents=True, exist_ok=True)
    # Establish directory to store podcasts
    podcast_path = Path("./static/podcasts")
    podcast_path.mkdir(parents=True, exist_ok=True)
    # Establish directory to store images
    image_path = Path("./static/image")
    image_path.mkdir(parents=True, exist_ok=True)
    # Establish the database file path
    db_path = Path(db_file)
    # Make the DB if it doesn't exist
    if not db_path.exists():
        clear_tables = [ "episodes", "podcasts", "settings", "lightning" ]
        init_podcasts_command = """ CREATE TABLE IF NOT EXISTS podcasts(
            podcast_title TEXT,
            podcast_url TEXT,
            podcast_image TEXT,
            podcast_description TEXT, 
            podcast_index_id INTEGER,
            podcast_value_link TEXT,
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
            file_path TEXT,
            episode_played INT,
            current_progress INT, 
            UNIQUE(episode_title),
            FOREIGN KEY(podcast_title) REFERENCES podcasts(podcast_title)
        );"""
        init_settings_command = """ CREATE TABLE IF NOT EXISTS settings(
            max_downloads INT,
            download_all INT,
            download_dir STR,
            ntfy_url STR
        );"""
        init_lightning_command = """ CREATE TABLE IF NOT EXISTS lightning(
            podcast_title TEXT,
            split_name TEXT,
            type TEXT,
            address TEXT,
            split_percent INTEGER,
            UNIQUE(address),
            FOREIGN KEY(podcast_title) REFERENCES podcasts(podcast_title)
        );"""
        default_settings_command = "INSERT INTO settings(max_downloads, download_all, download_dir, ntfy_url) VALUES(1,0,'static/podcasts','http://127.0.0.1:8001');"
        init_commands = [ init_podcasts_command, init_episodes_command, init_lightning_command, init_settings_command ]

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
def insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, episode_image, episode_description, file_path):
    episode_description = str(episode_description).replace("\n","-")
    command = "INSERT OR IGNORE INTO episodes(podcast_title, episode_link, episode_title, episode_date, episode_image, episode_description, file_path, episode_played, downloaded, current_progress) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = podcast_title, episode_link, episode_title, episode_date, episode_image, str(episode_description), str(file_path), "0", "0", "0"
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
def newPodcastSourceDB(db_file, podcast_title, new_podcast_source):
    con = sqlite3.connect(db_file)
    cur = con.cursor() 
    podcast_image_url = feedparser.parse(new_podcast_source).feed.image['href']
    podcast_image = imageDownload(podcast_title, podcast_image_url)
    podcast_index_id = getPodcastID(podcast_title)
    podcast_description = getPodDesc(podcast_title)
    podcast_funding_link = getFundingLink(podcast_index_id)
    getPodV4V(db_file, podcast_title, podcast_index_id)
    command = "INSERT OR IGNORE INTO podcasts(podcast_title, podcast_url, podcast_image, podcast_description, podcast_index_id, podcast_value_link) VALUES (?, ?, ?, ?, ?, ?)"
    values = [ podcast_title, new_podcast_source, podcast_image, podcast_description, podcast_index_id, podcast_funding_link ]
    cur.execute(command, (values))
    con.commit()
    con.close()

## Gather podcast source info from the DB
def gatherPodcastSources(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    result = cur.execute("SELECT podcast_title, podcast_image, podcast_url FROM podcasts;").fetchall()
    podcast_title = [row[0] for row in result]
    podcast_image = [row[1] for row in result]
    podcast_url = [row[2] for row in result]    
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

## Javascript DB Functions 
def episodePlayedDB(db_file, episode_title):
    # Just make sure the title is read as a string, just in case!
    episode_title = str(episode_title)
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    command = "UPDATE episodes SET episode_played=? WHERE episode_title=?"
    cur.execute(command, (1, episode_title))
    con.commit()
    con.close()

def currentTimeDB(db_file, episode_title, current_time_post):
    episode_title = str(episode_title)
    current_time_post = int(current_time_post) 
    print(f"Current Time: {current_time_post}")
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    command = "UPDATE episodes SET current_progress=? WHERE episode_title=?"
    cur.execute(command, (current_time_post, episode_title))
    con.commit()
    con.close()

def getCurrentTimeDB(db_file, episode_title):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    command = "SELECT current_progress FROM episodes WHERE episode_title=?"
    cur.execute(command, (episode_title,))
    result = cur.fetchone()
    print(result)
    current_time_get = result[0]
    print(current_time_get)
    con.close()
    return current_time_get

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
def updateDB(db_file, max_downloads, download_all, download_dir, ntfy_url):
    command = "UPDATE settings SET max_downloads=?, download_all=?, download_dir=?, ntfy_url=?"
    values = max_downloads, download_all, download_dir, ntfy_url
    executeDB(db_file, command, (values))

## Keep in mind this should remove all EPISODES too!
def removePodcastSource(db_file, remove_podcast_source):
    source_command = "DELETE FROM podcasts WHERE podcast_title=?"
    episodes_command = "DELETE FROM episodes WHERE podcast_title=?"
    commands = source_command, episodes_command
    for i in commands:
        # what is going on here with the comma?
        executeDB(db_file, i, (remove_podcast_source,))