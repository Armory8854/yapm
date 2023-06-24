#!/bin/bash
## Env variable defaults
### YAPM
YAPM_PORT=8000
YAPM_DATA_PATH="flask/data"
YAPM_PODCAST_PATH="flask/static/podcasts"

### ntfy.sh
NTFY_PORT=8001
NTFY_DATA_PATH="ntfy/data"

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
    --restart on-failure \
    --health-cmd 'curl http://localhost || exit 1' \
    --health-interval '1m' \
    --name podman_yapm \
    localhost/yapm:latest
}

## start ntfy
function start-ntfy() {
    podman run -p "$NTFY_PORT":80 \
    --volume "$NTFY_DATA_PATH":/var/cache/ntfy:rw \
    --detach \
    --restart on-failure \
    --name podman_ntfy \
    docker.io/binwiederhier/ntfy:v2.5.0 serve
}

## Stop all images
function stop-all() {
    podman stop podman_yapm 
    podman stop podman_ntfy
    podman rm podman_yapm
    podman rm podman_ntfy
}

## Delete all images
function delete-all() {
    podman rm "localhost/yapm:latest" 
    podman rm "docker.io/binwiederhier/ntfy:v2.5.0" 
    rm "$YAPM_DATA_PATH"/{database.db,subscriptions.opml} 
    for podcast in $(ls "$YAPM_PODCAST_PATH");
    do
        rm -r "$podcast" 
    done
    for image in $(ls $"YAPM_IMAGE_PATH");
    do
        rm "$image"
    done
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
