#!/usr/bin/env python3
import urllib
from bs4 import BeautifulSoup

import requests
import webbrowser
import re

text = 'Jeff C. Liu email'
text = urllib.parse.quote_plus(text)

### Google search api
url = 'https://google.ca/search?q=' + text

response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')
for g in soup.find_all(class_='g'):
    description = g.find('span', attrs={'class': 'st'})
    d = description.get_text()
    d = "".join(d.split("\n"))
    m = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', d, re.I)
    if m:
        print(m.group(0))
