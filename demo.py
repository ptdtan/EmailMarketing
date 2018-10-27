#!/usr/bin/env python3
import urllib
from bs4 import BeautifulSoup

import requests
import webbrowser
import re

import sys
text = sys.argv[1] + ' email'
text = urllib.parse.quote_plus(text)

### Google search api
url = 'https://google.ca/search?q=' + text + "&num=100"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
for g in soup.find_all(class_='g'):
    description = g.find('span', attrs={'class': 'st'})
    if not description:
        continue
    d = description.get_text()
    d = "".join(d.split("\n"))
    m = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', d, re.I)
    if m:
        print(m.group(0))
