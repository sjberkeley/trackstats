import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys

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
        if not words[0].isdigit():
            break
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


# TODO: Doesn't support the no-hundredths case yet ...
def hms_to_seconds(perf_str):
    ch = -1
    cm = -1
    hundredths = False
    for ii in range(len(perf_str)):
        if (perf_str[ii] == ":"):
            if ch > 0:
                cm = ii
            else:
                ch = ii
        elif (perf_str[ii] == "."):
            hundredths = True
    # if only one colon, then it's minutes
    if ch > 0 and cm == -1:
        cm = ch
        ch = -1

    h = 0
    m = 0
    if ch > 0:
        h = int(perf_str[0:ch])
        m = int(perf_str[ch+1:cm])
        s = float(perf_str[cm+1:len(perf_str)])
    elif cm > 0:
        m = int(perf_str[0:cm])
        s = float(perf_str[cm+1:len(perf_str)])
    else:
        s = float(perf_str[0:len(perf_str)])

    total_seconds = (h * 3600) + (m * 60) + s
    return total_seconds, hundredths

def seconds_to_hms(total_seconds):
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = round(total_seconds % 60, 2)
    if h > 0:
        time_str = str(h) + ":" + str(m) + ":" + str(s)
    elif m > 0:
        time_str = str(m) + ":" + str(s)
    else:
        time_str = str(s)
    return time_str

def get_args(argv):
    num_args = len(argv)
    if num_args < 3:
        print("Error: must have at least 2 arguments")
        exit
    gender = argv[1]
    event = argv[2]
    for ii in range(3, num_args):
        event = event + " " + argv[ii]
    if event == "High jump" or event == "Long jump" or event == "Triple jump" or event == "Pole vault" or \
        event == "Shot put" or event == "Discus throw" or event == "Hammer throw" or event == "Javelin throw" or\
        event == "Decathon" or event == "Heptathon":
        field_event = True
    else:
        field_event = False

    return gender, event, field_event

def get_lines_from_url(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print("Error:", response.status_code)
        exit

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Get the plain text representation of the HTML content
    plain_text = soup.get_text()
    
    # Split the text into lines
    lines = plain_text.splitlines()

    return lines

def strip_preamble(line, processing):
    status = 2
    # Skip empty lines
    if not line.strip():
        status = 0
        words = []
    else:
        words = line.split()
        num_words = len(words)
        # check for done with outdoor list
        if (num_words < 8 and processing == 1):
            status = 1
        elif (num_words > 7 and words[0] == "1" and processing == 0):
            processing = 1
        elif (processing == 0):
            status = 0
        elif not words[0].isdigit():
            status = 1

    return status, words, processing

def is_field_event(event):
    field_event = False
    for event_name in ("HJ", "PV", "LJ", "TJ", "SP", "DT", "HT", "JT", "Decathlon", "Heptathlon"):
        if event == event_name:
            field_event = True
            break

    return field_event
