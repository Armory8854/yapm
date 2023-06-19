#!/bin/bash
## Env variable defaults
### YAPM
YAPM_PORT=8000
YAPM_DATA_PATH="$PWD/flask/data"
YAPM_PODCAST_PATH="$PWD/flask/static/podcasts"

### ntfy.sh
NTFY_PORT=8001
NTFY_DATA_PATH="$PWD/ntfy/data"

## Functions
### Help command
function usage() {
    cat ./usage.txt
    exit 1
}

## build YAPM
function build-yapm() {
    podman build -t yapm .
}

## start YAPM
function start-yapm() {
    podman run -p "$YAPM_PORT":8000 \
    --volume "$YAPM_DATA_PATH":/app/data:rw \
    --volume "$YAPM_PODCAST_PATH":/app/static/podcasts:rw \
    --detach \
    --name podman_yapm \
    localhost/yapm:latest
}

## start ntfy
function start-ntfy() {
    podman run -p "$NTFY_PORT":80 \
    --volume "$NTFY_DATA_PATH":/var/cache/ntfy:rw \
    --detach \
    --name podman_ntfy \
    docker.io/binwiederhier/ntfy:v2.5.0 serve
}

## Stop all images
function stop-all() {
    podman stop podman_yapm 
    podman stop podman_ntfy
    podman rmi -f podman_yapm
    podman rmi -f podman_ntfy
}

## Delete all images
function delete-all() {
    podman rm -f localhost/yapm:latest \
    podman rm -f docker.io/binwiederhier/ntfy:v2.5.0 \
    rm "$YAPM_DATA_PATH"/{database.db,subscriptions.opml} \
    rm -r "$YAPM_PODCAST_PATH"/*
}

## Dev Functions
### Start flask dev server
function dev-server() {
    flask --app flask/yapm run
}
# If no flags, print help
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

# The flags
while [ "$1" != "" ]; do 
    case $1 in
    --start)
        start-yapm
        start-ntfy
        ;;
    --build)
        build-yapm
        ;;
    --stop)
        stop-all
        ;;
    --full-rebuild)
        stop-all
        delete-all
        build-yapm
        start-yapm
        start-ntfy
        ;;
    --delete-all)
        stop-all
        delete-all
        ;;
    --just-ntfy)
        start-ntfy
        ;;
    --help)
        usage
        ;;
    --dev)
        dev-server
        ;;
    esac
    shift
done