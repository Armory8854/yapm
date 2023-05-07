from flask import Flask, render_template, request, url_for, flash, redirect, abort
from new_podcast_download import newPodcastDownload
from new_podcast_source import newPodcastSource
from bin.db import gatherPodcastSources, gatherSettings, updateDB
from bin.parser import indexMetaGathering

app = Flask(__name__, static_url_path='/static', static_folder = 'static')

db_file = "data/database.db"

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
    newPodcastDownload(db_file)
    return redirect(url_for('index'))

@app.route("/new-source",methods=['POST'])
def new_source(name=None):
    new_podcast_source = request.form.get('podcast-rss-entry')
    newPodcastSource(db_file, new_podcast_source)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
