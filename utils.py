#
# miscellaneous utilities for content on visualtrackstats.com
#

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys
import pandas as pd

# need to fix bug with Gabby Thomas 400m score (49.68) - 1217 when it should be 1218
def get_WA_score(gender, event, performance, event_name_map, score_maps):
    wa_event = event_name_map[event]
    map = score_maps[wa_event]

    if len(map) == 0:
        filename = "scores/" + wa_event + "." + gender + ".scores"
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
                map[words[0]] = words[1]

    perf_str = performance       # str(performance)
    field_event = is_field_event(event)
    if not field_event and event != "Decathlon" and event != "Heptathlon":
        perf_units, hundredths = hms_to_seconds(perf_str)
        if hundredths:
            perf_units = round(perf_units, 2)
        perf_str = seconds_to_hms(perf_units, hundredths)

    if (perf_str < min(map) or perf_str > max(map)):
        return "0"

    if perf_str[-2] == ".":      # conversion to float may have truncated a trailing zero
        perf_str += "0"
    
    if event == "half-marathon" or event == "marathon" or event == "20 km race walk" or event == "50 km race walk":
        index = perf_str.find(".")
        if index != -1:      # truncate decimal
            perf_str = perf_str[0:index]

    # if the performance does not exist in the map, find the next lower performance that does
    if event == "Decathlon" or event == "Heptathlon":
        perf_units = int(perf_str)
        if perf_units < 1000 or perf_units > 10000:
            return 0
        while map.get(perf_str) == None:       # key does not exist
            perf_units = int(perf_str)
            perf_units = perf_units - 1
            perf_str = str(perf_units)
    elif field_event:
        if perf_str[-4] == ".":   # one too many decimal places, round down
            perf_str = perf_str[:-1]
        perf_units = float(perf_str)
        while map.get(perf_str) == None:       # key does not exist
            perf_units = round(perf_units - 0.01, 2)
            perf_str = str(perf_units)
            if perf_str[-2] == ".":
                perf_str += "0"
    else:            
        while map.get(perf_str) == None:       # key does not exist
            perf_units, hundredths = hms_to_seconds(perf_str)
            if hundredths:
                perf_units = round(perf_units + 0.01, 2)
            else:
                perf_units = perf_units + 1
            perf_str = seconds_to_hms(perf_units, hundredths)

    score = map[perf_str]
    return score

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
        num_chars = len(words[num_words-1])
        date = int(words[num_words-1][num_chars-4:])
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
        if event_name == "60 metres":       # skip special events
            break
        if (event_name == "Back to main page" or event_name == "" or event_name == "Old specs"):
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
    name = words[index]
    index = index + 1
    for iter in range(5):
        nation = words[index]
        if words[index] != "BEl" and words[index] != "EX":      # typo on men marathon and men 20k walk
            wordlen = len(words[index])
            maybe_nation = ""
            if wordlen > 2:
                maybe_nation = words[index][-3:wordlen]
            if maybe_nation.isupper():                          # last word of name runs into nation
                if wordlen > 3:
                    name += " " + words[index][:-3]
                nation = maybe_nation
                break
            elif words[index].isupper() and wordlen == 3:       # nation already set
                break
            else:                                               # another part of name
                name += " " + words[index]
            index = index + 1

    index = index + 2
    position = "*"
    if is_numeric(words[index][0]) or words[index] == "D" or words[index] == "q" or words[index] == "*":
        position = words[index]
        index = index + 1

    if index == num_words - 1:       # no city ?
        city = "unknown"
    else:
        city = words[index]
    if num_words > index + 2:
        index = index + 1
        city += " " + words[index]
        if num_words > index + 2:
            index = index + 1
            city += " " + words[index]

    comma_index = city.find(',')
    if comma_index != -1:
        city = city[0:comma_index] + city[comma_index+1:]

    date = words[num_words-1]
    if len(date) > 10:
        if date[10] == ">":       # Anna Cockrell in 400 hurdles
            date = words[num_words-1][0:10]
        else:
            date = words[num_words-1][-10:]
    if len(date) < 10:
        if date[1] == ".":
            date = "0" + date
        elif date[4] == ".":
            date = date[0:3] + "0" + date[3:9]
    year = int(date[6:10])
    month = int(date[3:5])
    if month < 1:
        month = 1
    if month > 12:
        month = 12
    day = int(date[0:2])
    if day > 31:
        day = 31
    this_date = datetime(year, month, day)

    return name, year, performance, nation, this_date, city, position, date


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

def seconds_to_hms(total_seconds, hundredths):
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = round(total_seconds % 60, 2)
    if not hundredths:
        s = int(s)
    if h > 0:
        time_str = str(h) + ":"
        if m < 10:
            time_str += "0"
        time_str += str(m) + ":"
        if s < 10:
            time_str += "0"
        time_str += str(s)
    elif m > 0:
        time_str = str(m) + ":"
        if s < 10:
            time_str += "0"
        time_str += str(s)
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
        event == "Decathlon" or event == "Heptathlon":
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
    for event_name in ("HJ", "PV", "LJ", "TJ", "SP", "DT", "HT", "JT", "Decathlon", "Heptathlon", \
        "High jump", "Long jump", "Triple jump", "Pole vault", "Shot put", "Discus throw", "Javelin throw", "Hammer throw"):
        if event == event_name:
            field_event = True
            break

    return field_event

def init_score_maps(event_name_map, score_maps):
    event_name_map["100 metres"] = "100m"
    event_name_map["10000 metres"] = "10000m"
    event_name_map["100m hurdles"] = "100mH"
    event_name_map["110m hurdles"] = "110mH"
    event_name_map["1500 metres"] = "1500m"
    event_name_map["20 km race walk"] = "20kmW"
    event_name_map["200 metres"] = "200m"
    event_name_map["2000 metres"] = "2000m"
    event_name_map["3000 metres"] = "3000m"
    event_name_map["3000m steeplechase"] = "3000m SC"
    event_name_map["400 metres"] = "400m"
    event_name_map["400m hurdles"] = "400mH"
    event_name_map["4x100m relay"] = "4x100m"
    event_name_map["4x400m relay"] = "4x400m"
    event_name_map["50 km race walk"] = "50kmW"
    event_name_map["5000 metres"] = "5000m"
    event_name_map["800 metres"] = "800m"
    event_name_map["Decathlon"] = "Dec."
    event_name_map["Discus throw"] = "DT"
    event_name_map["Hammer throw"] = "HT"
    event_name_map["Heptathlon"] = "Hept."
    event_name_map["High jump"] = "HJ"
    event_name_map["Javelin throw"] = "JT"
    event_name_map["Long jump"] = "LJ"
    event_name_map["1 Mile"] = "Mile"
    event_name_map["2 Miles"] = "2 Miles"
    event_name_map["Pole vault"] = "PV"
    event_name_map["Shot put"] = "SP"
    event_name_map["Triple jump"] = "TJ"
    event_name_map["half-marathon"] = "HM"
    event_name_map["marathon"] = "Marathon"

    score_maps["100m"] = {}
    score_maps["10000m"] = {}
    score_maps["100mH"] = {}
    score_maps["110mH"] = {}
    score_maps["1500m"] = {}
    score_maps["20kmW"] = {}
    score_maps["200m"] = {}
    score_maps["2000m"] = {}
    score_maps["3000m"] = {}
    score_maps["3000m SC"] = {}
    score_maps["400m"] = {}
    score_maps["400mH"] = {}
    score_maps["4x100m"] = {}
    score_maps["4x400m"] = {}
    score_maps["50kmW"] = {}
    score_maps["5000m"] = {}
    score_maps["800m"] = {}
    score_maps["Dec."] = {}
    score_maps["DT"] = {}
    score_maps["HT"] = {}
    score_maps["Hept."] = {}
    score_maps["HJ"] = {}
    score_maps["JT"] = {}
    score_maps["LJ"] = {}
    score_maps["Mile"] = {}
    score_maps["2 Miles"] = {}
    score_maps["PV"] = {}
    score_maps["SP"] = {}
    score_maps["TJ"] = {}
    score_maps["HM"] = {}
    score_maps["Marathon"] = {}


def near(seed, ymd):
    #assume it's the same year
    if seed < ymd:
        first = seed
        last = ymd
    else:
        first = ymd
        last = seed

    if first[5:7] == last[5:7]:    #same month
        total = int(last[8:10]) - int(first[8:10]) + 1
    else:
        month_range = int(last[5:7]) - int(first[5:7]) + 1
        month = int(first[5:7])
        total = 0
        for ii in range(month_range):
            num_days = 31
            if month == 4 or month == 6 or month == 9 or month == 11:
                num_days = 30
            elif month == 2:
                num_days = 28

            start = 0
            end = num_days
            if ii == 0:
                start = int(first[8:10])
            elif ii == month_range - 1:
                end = int(last[8:10])

            total = total + (end - start)
            month = month + 1

    return total

def days_in_month(month):
    num_days = 31
    if month == 4 or month == 6 or month == 9 or month == 11:
        num_days = 30
    elif month == 2:
        num_days = 28
    
    return num_days
