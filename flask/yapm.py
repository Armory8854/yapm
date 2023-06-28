import time
import schedule
from flask import Flask, render_template, request, url_for, flash, redirect, send_file, request, jsonify
from bin.new_podcast_download import downloadNewFunction
from bin.new_podcast_source import newPodcastSource
from bin.db import initDB, gatherSettings, updateDB, gatherDownloadedPodcasts, removePodcastSource, episodePlayedDB, currentTimeDB, getCurrentTimeDB, getChaptersDB
from bin.parser import indexMetaGathering, exportToOPML, initOPML, importOPML
from bin.podcast_index import searchForPodcasts

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder = 'static')

    db_file = "data/database.db"
    opml_file = "data/subscriptions.opml"

    initDB(db_file)
    initOPML(opml_file)

    def downloadSchedule():
        schedule.every().hour.do(downloadNewFunction, db_file)

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

    # Post and get could be used here for searching and indexing
    @app.route("/search")
    def search(name=None):
        css_url = url_for('static', filename='styles.css')
        return render_template('search.html', name=name, css_url=css_url)

    @app.route("/search-index", methods=["POST"])
    def search_index(name=None):
        css_url = url_for('static', filename='styles.css')
        rfg = request.form.get
        search_term = rfg('search-index')
        search_list = searchForPodcasts(search_term) 
        return render_template('search.html', name=name, css_url=css_url, search_list=search_list)

    @app.route("/podcasts")
    def podcasts(name=None):
        downloaded_podcasts = gatherDownloadedPodcasts(db_file)
        css_url = url_for('static', filename='styles.css')
        media_player_url = url_for('static', filename='js/media-player.js')
        podcast_dir = gatherSettings(db_file)['download_dir']
        ntfy_url = gatherSettings(db_file)['ntfy_url']
        print(downloaded_podcasts)
        return render_template('podcasts.html', podcasts=downloaded_podcasts, css_url=css_url, media_player_url=media_player_url, podcast_dir=podcast_dir, ntfy_url=ntfy_url)

    # Could get a GET request to change how settings are queried
    # Not as urgent though compared to other sections
    @app.route("/settings-update", methods=[ 'POST' ])
    def settings_update(name=None):
        rfg = request.form.get
        max_downloads = rfg('max_downloads')
        download_all = rfg('download_all')
        download_dir = rfg('download_dir')
        ntfy_url = rfg('ntfy_url')
        updateDB(db_file, max_downloads, download_all, download_dir, ntfy_url)
        return redirect(url_for('settings'))

    @app.route("/download-new")
    def download_new(name=None):
        downloadNewFunction(db_file)
        return redirect(url_for('index'))

    @app.route("/episode-played",methods=['POST'])
    def episode_played(name=None):
        data = request.json.get
        episode_title = data('episode_title')
        episodePlayedDB(db_file, episode_title)
        return(podcasts())

    @app.route("/current-time", methods=['POST', 'GET'])
    def current_time(name=None):
        if request.method == 'POST':
            data = request.json.get
            episode_title = data('episode_title')
            current_time_post = data('current_time')
            print(episode_title, current_time_post)
            currentTimeDB(db_file, episode_title, current_time_post)
            return jsonify(current_time_post=current_time_post)
        if request.method == 'GET':
            episode_title = request.args.get('episode_title')
            current_time_get = getCurrentTimeDB(db_file, episode_title)
            print(current_time_get)
            return jsonify(current_time_get=current_time_get)

    # I need to combine new & remove source to use a method variable
    # That said method should be "add" or "remove", with the method changing logic
    @app.route("/new-source",methods=['POST'])
    def new_source(name=None):
        new_podcast_source = request.form.get('podcast-rss-entry')
        newPodcastSource(db_file, new_podcast_source)
        return redirect(url_for('index'))

    @app.route("/remove-source",methods=['POST'])
    def remove_source(name=None):
        remove_podcast_source = request.form.get('podcast-source-removal')
        removePodcastSource(db_file, remove_podcast_source)
        return redirect(url_for('index'))

    # I need to compbine opml export & import
    # Export could be a GET request
    @app.route("/opml-export")
    def opml_export(name=None):
        exportToOPML(db_file, opml_file)
        mimetype = "application/octet-stream" 
        return send_file(opml_file, mimetype=mimetype, as_attachment=True)

    @app.route("/opml-import",methods=['POST'])
    def opml_import(name=None):
        uploaded_opml_file = request.files['uploaded_opml_file']
        uploaded_opml_file.save(opml_file)
        importOPML(db_file, opml_file)
        return redirect(url_for('index'))

    # Future proofing this for any possible future additions
    @app.route("/episode-metadata",methods=['GET'])
    def episode_metadata(name=None):
        if request.method == 'GET':
            metadata_query = request.args.get('query')
            episode_title = request.args.get('episode-title')
            if metadata_query == 'chapters': 
                chapters = getChaptersDB(db_file, episode_title)
                return jsonify(episode_title=episode_title, episode_chapters=chapters)
    
    ## Hourly Downloads ##
    # Initiate the hourly scheduler here
    downloadSchedule()

    # Define how to run the scheduler here
    def runScheduled():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Start the scheduler here
    import threading
    threading.Thread(target=runScheduled).start()

    return app
