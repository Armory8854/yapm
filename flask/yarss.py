from flask import Flask, request, render_template, url_for

app = Flask(__name__, static_url_path='/static', static_folder = 'static')

@app.route("/")
def index(name=None):
    css_url = url_for('static', filename='styles.css')
    return render_template('index.html', name=name, css_url=css_url)
    
if __name__ == "__main__":
    app.run()
