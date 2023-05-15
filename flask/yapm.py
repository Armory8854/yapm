import schedule
import time
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from bin.new_podcast_download import newPodcastDownload, newPodcastDLDB, newPodcastDLInputs
from bin.new_podcast_source import newPodcastSource
from bin.db import initDB, gatherSettings, updateDB, gatherDownloadedPodcasts, podcastDownloaded
from bin.parser import indexMetaGathering

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder = 'static')

    db_file = "data/database.db"
    initDB(db_file)

    def scheduleDownloadJob():
        newPodcastDownload(db_file)

    @app.route("/")
    def index(name=None):
        meta_dict = indexMetaGathering(db_file)
        css_url = url_for('static', filename='styles.css')
        return render_template('index.html', name=name, css_url=css_url, meta_dict=meta_dict)

    @app.route("/settings")
    def settings(name=None):
        settings_dict = gatherSettings(db_file)
        print(settings_dict)
        css_url = url_for('static', filename='styles.css')
        return render_template('settings.html', name=name, css_url=css_url, settings=settings_dict)

    @app.route("/podcasts")
    def podcasts(name=None):
        downloaded_podcasts = gatherDownloadedPodcasts(db_file)
        print(downloaded_podcasts)
        css_url = url_for('static', filename='styles.css')
        media_player_url = url_for('static', filename='js/media-player.js')
        print(downloaded_podcasts)
        return render_template('podcasts.html', podcasts=downloaded_podcasts, css_url=css_url, media_player_url=media_player_url)

    @app.route("/settings-update", methods=[ 'POST' ])
    def settings_update(name=None):
        rfg = request.form.get
        max_downloads = rfg('max_downloads')
        download_all = rfg('download_all')
        download_dir = rfg('download_dir')
        updateDB(db_file, max_downloads, download_all, download_dir)
        return redirect(url_for('settings'))

    @app.route("/download-new")
    def download_new(name=None):
        attempts = 0
        start_time = time.time()
        while attempts < 3:
            try:
                dl_inputs = newPodcastDLInputs(db_file)
                settings_dict = dl_inputs[0]
                urls_dirty = dl_inputs[1]
                db_inputs = newPodcastDLDB(db_file, settings_dict, urls_dirty)
                podcast_dir = db_inputs[0]
                new_podcasts = db_inputs[1]
                for i in range(len(new_podcasts)):
                    downloaded_new = newPodcastDownload(new_podcasts, podcast_dir, i)
                    episode_title = downloaded_new[0]
                    file_path = downloaded_new[1]
                    podcastDownloaded(db_file, episode_title, file_path)
                break
            except KeyError:
                attempts += 1
                print("Key error occured - let's try again")
        end_time = time.time()
        duration = end_time - start_time
        print("Duration: " + str(duration)) 
        return redirect(url_for('index'))

    @app.route("/new-source",methods=['POST'])
    def new_source(name=None):
        new_podcast_source = request.form.get('podcast-rss-entry')
        newPodcastSource(db_file, new_podcast_source)
        return redirect(url_for('index'))

    # Schedule the download job to run every hour
    schedule.every().hour.do(scheduleDownloadJob)

    # Define a function to run the scheduler in a separate thread
    def runScheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    import threading
    scheduler_thread = threading.Thread(target=runScheduler)
    scheduler_thread.start()

    return app
