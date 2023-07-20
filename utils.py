import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def is_numeric(string):
    pattern = r'^[-+±]?[0-9]*\.?[0-9]+$'
    return bool(re.match(pattern, string))
#
# find the earliest year in which a mark is posted
#
def find_earliest_year(lines, this_year):
    # find earliest year
    earliest = this_year
    processing = 0
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        words = line.split()
        num_words = len(words)
        # check for done with outdoor list
        if (num_words < 8 and processing == 1):
            break
        if (num_words > 7 and words[0] == "1" and processing == 0):
            processing = 1
        if (processing == 0):
            continue
        date = int(words[num_words-1][6:])
        if date < earliest:
            earliest = date

    return earliest

#
# check if one performance is worse than another
#
def worse_than(field_event, perf1, perf2):
    is_worse = True
    if (field_event):
        is_worse = (perf1 < perf2)
    else:
        is_worse = (perf1 > perf2)

    return is_worse

#
# Get the urls of the pages to scrape
#
def get_urls(links_url):
    response = requests.get(links_url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print("Error:", response.status_code)
        exit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract all the links on the page
    links = soup.find_all("a")
    urls = {}

    for link in links:
        event_name = link.text
        if (event_name == "Back to main page" or event_name == ""):
            continue
        if event_name not in urls.keys():
            urls[event_name] = "http://www.alltime-athletics.com/" + link.get("href")

    return urls

#
# extract the name, date and performance
#
def get_stats(words):
    num_words = len(words)
    perf = words[1]
    if not perf[-1].isnumeric():       # trailing A denotes altitude, y yards
        if not perf[-2].isnumeric():
            performance = perf[:-2]
        else:
            performance = perf[:-1]
    else:
        performance = perf  # float(perf)

    index = 2
    if is_numeric(words[index]):       # wind reading for straightaway and runway
        index = index + 1
    name = words[index] + " " + words[index+1]
    index = index + 2
    if not words[index].isupper() or len(words[index]) != 3:
        name += " " + words[index]
        index = index + 1
        if not words[index].isupper() or len(words[index]) != 3:
            name += " " + words[index]

    date = words[num_words-1]
    if len(date) > 10:
        date = words[num_words-1][-10:]
    year = int(date[6:])
    return name, year, performance

