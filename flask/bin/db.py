import sqlite3

# General DB Functions, mainly executeDB #
## Generic sql query function
def executeDB(db_file,command,values=None,):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    if values == None:
        cur.execute(command)
    else:
        cur.execute(command, (values))
    con.commit()
    con.close()    

## The init DB for first runs / testing purposes
def initDB(db_file):
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
    default_settings_command = "INSERT INTO settings(max_downloads, download_all, download_dir) VALUES(10,0,'/home/celer/Podcasts');"
    init_commands = init_podcasts_command, init_episodes_command, init_settings_command

    for i in clear_tables:
        clear_command = "DROP TABLE IF EXISTS " + i + ";"
        executeDB(db_file, clear_command)

    for i in init_commands:
        executeDB(db_file, i)

    executeDB(db_file, default_settings_command)

# New Podcast functions #
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
    con.close()
    return new_episodes

## Updates a podcast as downloaded
def podcastDownloaded(db_file, episode_title, download_dir):
    command_posted = "UPDATE episodes SET downloaded=?, download_dir=? WHERE episode_title=?"
    values = "1", download_dir, episode_title
    executeDB(db_file, command_posted, values)

## New podcast source
def newPodcastSourceDB(db_file, podcast_title, new_podcast_source, podcast_image):
    command = "INSERT OR IGNORE INTO podcasts(podcast_title, podcast_url, podcast_image) VALUES (?, ?, ?)"
    values = podcast_title, new_podcast_source, podcast_image
    executeDB(db_file, command, values)

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
    executeDB(db_file, command, values)
