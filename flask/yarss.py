from flask import Flask, render_template, request, url_for, flash, redirect, abort
from bin.db import getDBConnection, gatherPodcastSources
from bin.parser import indexMetaGathering

app = Flask(__name__, static_url_path='/static', static_folder = 'static')
db_file = "data/database.db"

@app.route("/")
def index(name=None):
    urls = gatherPodcastSources(db_file)
    meta_dict = indexMetaGathering(urls)
    css_url = url_for('static', filename='styles.css')
    return render_template('index.html', name=name, css_url=css_url, urls=urls, meta_dict=meta_dict)
    
if __name__ == "__main__":
    app.run()
