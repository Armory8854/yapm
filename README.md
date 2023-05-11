# YAPM - Yet Another (python) Podcast Manager
This project is simply a way to download podcasts on a regular timer. Included in the project is a media player with extremely basic functionality, but the goal is mainly to download and store podcasts in an organized fashion for later playback.

Basic usage so far includes:
- Adding new podcast subscriptions
- Playing back podcast episodes
- Downloading podcast subscriptions
- Setting downloads directory
  - Only useful if not running inside a container (I.E. Docker or Podman). Leave as `/Podcasts` if running in a container.

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
  --volume /path/to/podcast/downloads:/Podcasts:rw \
  --volume /path/to/data:/app/data:rw
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
$ gunicorn -c gunicorn_config.py wsgi:app
```

# TODO
- [ ] Implement proper playback of local files instead of streaming files.
- [ ] Store image files locally instead of pulling high res copies online
- [ ] Docker/Podman compose
  - Kind of overkill due to how basic the app is. However, compose is much more friendlier in general.
- [ ] Package for nix
  - [ ] At the very least create a working proof of concept install.nix
  - [ ] Create a service as well
