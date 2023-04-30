import configparser

def gatherURL(env_file):
    global urls
    urls = []
    config = configparser.ConfigParser()
    config.read(env_file)
    for url_section in config.sections():
        for (url_key, url_val) in config.items(url_section):
            urls.append(url_val)

    print(urls)
    return urls
        
