import sqlite3

def executeDB(db_file,command,values=None,):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    if values == None:
        cur.execute(command)
    else:
        cur.execute(command, values)
    con.commit()
    con.close()    

def initDB(db_file):
    clear_command = "DROP TABLE IF EXISTS podcasts;"
    init_command = """ CREATE TABLE IF NOT EXISTS podcasts (
        podcast_title TEXT,
        episode_link TEXT,
        episode_title TEXT,
        episode_date TEXT,
        episode_image TEXT,
        downloaded INTEGER,
        UNIQUE(episode_title)
    );"""
    executeDB(db_file, clear_command)
    executeDB(db_file, init_command)

def insertEntry(db_file, podcast_title, episode_link, episode_title, episode_date, episode_image):
    command = "INSERT OR IGNORE INTO podcasts(podcast_title, episode_link, episode_title, episode_date, episode_image, downloaded) VALUES (?, ?, ?, ?, ?, ?)"
    values = podcast_title, episode_link, episode_title, episode_date, episode_image, "0"
    executeDB(db_file, command, values)
    
def downloadSearch(db_file):
    global new_podcasts
    command = "SELECT * FROM podcasts WHERE downloaded=0;"
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    new_podcasts = cur.execute(command).fetchall()
    return new_podcasts

def podcastDownloaded(db_file, episode_title):
    command_posted = "UPDATE podcasts SET downloaded=1 WHERE episode_title=?"
    executeDB(db_file, command_posted, [episode_title])
