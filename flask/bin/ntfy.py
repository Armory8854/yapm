import requests

def ntfyMessage(ntfy_url, message):
    topic_url = str(f"{ntfy_url}/yapm")
    requests.post(topic_url,
        data = message.encode(encoding='utf-8'))

def ntfyDownloadFinished(ntfy_url, podcast_title, episode_title):
    message = str(f"Download finished: {podcast_title} - {episode_title}")
    ntfyMessage(ntfy_url, message)

def ntfyDownloadFailed(ntfy_url):
    message = str(f"Download Failed! Check logs!")
    ntfyMessage(ntfy_url, message)