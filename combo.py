import requests
from bs4 import BeautifulSoup
from datetime import datetime
import utils         # my utils

map100 = {}
map200 = {}
map400 = {}
map400H = {}
map110H = {}

def get_score(gender, event, performance):
    if event == "100m":
        map = map100
    elif event == "200m":
        map = map200
    elif event == "400m":
        map = map400
    elif event == "400mH":
        map = map400H
    elif event == "110mH":
        map = map110H
    if len(map) == 0:
        filename = "scores/" + event + "." + gender + ".scores"
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
                map[words[0]] = words[1]

    perf_str = str(performance)
    if perf_str[-2] == ".":      # conversion to float may have truncated a trailing zero
        perf_str += "0"

    # if the performance does not exist in the map, find the next lower performance that does
    field_event = False
    for event_name in ("HJ", "PV", "LJ", "TJ", "SP", "DT", "HT", "JT", "Decathlon", "Heptathlon"):
        if event == event_name:
            field_event = True
            break

    while map.get(perf_str) == None:       # key does not exist
        suffix = int(perf_str[-2:])
        str_len = len(perf_str)
        if str_len == 4:
            prefix = int(perf_str[0])
        else:
            prefix = int(perf_str[-5:-3])
        if perf_str[-3] == ".":            # hundredths
            domain = 100
        else:
            domain = 60                    # seconds or minutes
        if field_event:
            if suffix == 0:
                suffix = domain
                prefix -= 1
            suffix -= 1
        else:
            if suffix == domain - 1:
                suffix = -1
                prefix += 1
            suffix += 1
        if str_len < 6:                    # xx.xx or xx:xx
            perf_str = str(prefix) + perf_str[-3] + str(suffix)
        else:
            perf_str = perf_str[:str_len - 5] + str(prefix) + perf_str[-3] + str(suffix)
        if perf_str[-2] == ".":      # conversion to float may have truncated a trailing zero
            perf_str += "0"

    score = map[perf_str]
    return score

#
# main program
#
gender = "men"
num_events = 2

urls = []

m_urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
w_urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

if gender == "women":
    urls.append(w_urls["100 metres"])
    urls.append(w_urls["200 metres"])
    urls.append(w_urls["400 metres"])
    urls.append(w_urls["100m hurdles"])
    urls.append(w_urls["400m hurdles"])

else:
    urls.append(m_urls["100 metres"])
    urls.append(m_urls["200 metres"])
    urls.append(m_urls["400 metres"])
    urls.append(m_urls["110m hurdles"])
    urls.append(m_urls["400m hurdles"])


athletes = {}     # dictionary of lists
first = 3         # first event on the list
for event in ("100m", "200m", "400m", "110mH", "400mH"):
    if event == "100m":
        continue
    elif event == "200m":
        continue
    elif event == "400m":
        continue
    elif event == "110mH":
        event_num = 0
    elif event == "400mH":
        event_num = 1
    url = urls[first + event_num]
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        exit

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Get the plain text representation of the HTML content
    plain_text = soup.get_text()
    
    # Split the text into lines
    lines = plain_text.splitlines()

    # process data
    processing = 0
    counter = 0
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

        # extract performance, name and date (year)
        counter += 1
        name, date, performance = utils.get_stats(words)
        score = get_score(gender, event, performance)

        # populate dictionary
        if name in athletes.keys():
            list = athletes[name]
        else:
            list = []
            athletes[name] = list
        if len(list) == event_num * 2:
            list.append(performance)
            list.append(score)

# now create a map with each athlete's aggregate score as the key
done_with = {}
for athlete in athletes.keys():
    if done_with.get(athlete) != None:
        continue

    max_score = 0
    for name in athletes.keys():
        if done_with.get(name) != None:
            continue
        list = athletes[name]
        if len(list) < num_events * 2:
            continue
        total_score = 0
        for ii in range(0, num_events):
            total_score = total_score + int(list[ii * 2 + 1])
        if total_score > max_score:
            max_score = total_score
            max_name = name

    if max_score > 0:
        list = athletes[max_name]
        print(max_score, " ", max_name, " ", list[0], " ", list[1], " ", list[2], " ", list[3])  #, " ", list[4], " ", list[5])
        done_with[max_name] = True
