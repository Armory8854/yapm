# YAPM - Yet Another (python) Podcast Manager
A self hosted web app to download and manage podcast subscriptions. Soon to include podcasting 2.0 features such as sending lightning payments.

This project started out as a way for me to learn how to make a python application, but has evolved into a full fledged flask application. This project is more of a learning exercise and personal goal of mine, If you want to use something like this, I highly suggest checking out the biggest inspiration to this project [Podgrab](https://www.google.com/search?client=firefox-b-1-d&q=podgrab+github). I have not actually looked at their source code, but the general layout was my inspiration.

**This application is extremely opinionated**. The envisioned workflow for podcast downloading and processing is this:
1. Add podcasts to a database
  - Gather value information (Subscriptions, Lightning Payments mainly) to contribute to the podcasters
2. Download X episodes of said podcast, if not all episodes.
3. Convert the downloaded file to .opus
  - I prefer the file format for multiple reasons that I can explain if anyone cares.
4. Use a web based player to consume the podcasts.
  - The player will feature links to subscribe to the podcast, or send a Lightning Payment.
    + More than likely the Lightning payments will just utilize alby. I want to make this as frictionless as possible for me, and anyone else who decides to use the project.


# Installation
## Container
The easiest way to get going (like always) is by using a container software. First, build the container:

First, clone the repo:

`$ git clone https://github.com/Armory8854/yapm.git && cd yapm`

Then, build the container.

`$ podman build -t yapm .`

Finally, run it

```
$ podman run -p 8000:8000 \
  --volume /path/to/podcast/downloads:/app/static/podcasts:rw \
  --volume /path/to/data:/app/data:rw \
  localhost/yapm:latest
```

## Virtual Environment
Follow typical python virutal environment creation steps

```
$ git clone https://github.com/Armory8854/yapm.git && cd yapm
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Once in your virtual environment, start the app like so:

```
$ cd flask
$ gunicorn --bind "0.0.0.0:8000 \
  --workers 2 \
  --worker-class gevent \
  --log-level info wsgi:app
```

# TODO
- [x] Implement proper playback of local files instead of streaming files.
- [x] Store image files locally instead of pulling high res copies online
- [ ] Docker/Podman compose
  - Kind of overkill due to how basic the app is. However, compose is much more friendlier in general.

# Special Thanks
This program utilizes many different libraries, and I wanted to give them a special mention here. Without them, this project would have taken a lot longer to get where it is today:

1. The Podcast Index, for providing an API and helping to push the Value 4 Value model.
2. feedparser for making handling RSS feeds a breeze.
3. Flask for making web applications easy.
4. Jupiter Broadcasting for inspiring me to use nixos, and pushing for giving back to developers and creators when possible
