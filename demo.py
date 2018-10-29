#!/usr/bin/env python3
import urllib
from bs4 import BeautifulSoup

import requests
import webbrowser
import re

import sys

def initNamePool(names_f):
    Names = set()
    for line in open(names_f):
        names = [n.strip() for n in line.strip().split(",")]
        for n in names:
            Names.add(n)
    return Names

def main(Names, number = 15):
    out_f = open("List_Emails.txt", "w")
    for n in Names:
        print("Search for %s" %n)
        text = n + ' edu email'
        text = urllib.parse.quote_plus(text)

        ### Google search api
        url = 'https://google.ca/search?q=' + text + "&num=" + number

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
                out_f.write("%s\t%s\n" %(n, m.group(0)))
if __name__ == "__main__":
    print("Usage: ./demo.py <name_f> <number of result per name>")
    Names = initNamePool(sys.argv[1])
    main(Names, sys.argv[2])
