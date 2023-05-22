# This is god awful and should be regex. No way this is acceptable.
def sanitizeNames(episode_title):
    chars_to_dash = ["/"," ","&"]
    chars_to_del = ["?","!",".",":","'"]
    for i in chars_to_dash:
        episode_title = episode_title.replace(i,"-")

    for i in chars_to_del:
        episode_title = episode_title.replace(i,"")
        
    return episode_title
