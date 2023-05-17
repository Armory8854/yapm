from bs4 import BeautifulSoup

opml_file = "/home/celer/Downloads/subscriptions.opml"
with open(opml_file, 'r') as f:
    contents = f.read()

soup = BeautifulSoup(contents, features='xml')
items = soup.find_all("outline")
for item in items:
    print(item.get('xmlUrl'))
