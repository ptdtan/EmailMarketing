#!/usr/bin/env python3
import urllib
from bs4 import BeautifulSoup

import requests
import webbrowser
import re

import sys

"""
Read PMID authors file,
return a dictionary: key = "title", value = "list of authors"
"""
def initNamePool(names_f):
    Names = dict()
    for line in open(names_f):
        names = [n.strip() for n in line.strip().split(",")]
        Names[names[0]] = names[1:]
    return Names

"""
Search email for each titles
"""
def main(Names, number = 15):
    out_f = open("List_Emails.tsv", "w")
    for t, l in Names.items():
        i = 0
        for n in l:
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
                    if i > 0:
                        out_f.write("\t%s\t%s\n" %(n, m.group(0)))
                    else:
                        out_f.write("%s\t%s\t%s\n" %(t, n, m.group(0)))
                    i+=1
if __name__ == "__main__":
    print("Usage: ./demo.py <name_f> <number of result per name>")
    Names = initNamePool(sys.argv[1])
    main(Names, sys.argv[2])
