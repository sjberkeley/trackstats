import requests
from bs4 import BeautifulSoup
from datetime import datetime
import utils         # my utils

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


map100 = {}
map200 = {}
map400 = {}
map400H = {}
map110H = {}
map1500 = {}
map3000 = {}
map5000 = {}

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
    elif event == "1500m":
        map = map1500
    elif event == "3000m":
        map = map3000
    elif event == "5000m":
        map = map5000
    
    if len(map) == 0:
        filename = "scores/" + event + "." + gender + ".scores"
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
                map[words[0]] = words[1]

    perf_str = performance   # str(performance)
    if perf_str[-2] == ".":      # conversion to float may have truncated a trailing zero
        perf_str += "0"

    # if the performance does not exist in the map, find the next lower performance that does
    field_event = False
    for event_name in ("HJ", "PV", "LJ", "TJ", "SP", "DT", "HT", "JT", "Decathlon", "Heptathlon"):
        if event == event_name:
            field_event = True
            break

    while map.get(perf_str) == None:       # key does not exist
        perf_units, hundredths = hms_to_seconds(perf_str)
        if hundredths:
            perf_units = round(perf_units + 0.01, 2)
        else:
            perf_units = perf_units + 1
        perf_str = seconds_to_hms(perf_units)

    score = map[perf_str]
    return score

#
# main program
#
gender = "men"
num_events = 3

urls = []

m_urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
w_urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

# alltime-athletics event titles
if gender == "women":
    urls.append(w_urls["100 metres"])
    urls.append(w_urls["200 metres"])
    urls.append(w_urls["400 metres"])
    urls.append(w_urls["100m hurdles"])
    urls.append(w_urls["400m hurdles"])
    urls.append(w_urls["1500 metres"])
    urls.append(w_urls["3000 metres"])
    urls.append(w_urls["5000 metres"])

else:
    urls.append(m_urls["100 metres"])
    urls.append(m_urls["200 metres"])
    urls.append(m_urls["400 metres"])
    urls.append(m_urls["110m hurdles"])
    urls.append(m_urls["400m hurdles"])
    urls.append(m_urls["1500 metres"])
    urls.append(m_urls["3000 metres"])
    urls.append(m_urls["5000 metres"])

athletes = {}     # dictionary of lists
first = 0         # first event on the list
for event in ("100m", "200m", "400m", "110mH", "400mH", "1500m", "3000m", "5000m"):
    if event == "100m":
        event_num = 0
    elif event == "200m":
        event_num = 1
    elif event == "400m":
        event_num = 2
    elif event == "110mH":
        continue
    elif event == "400mH":
        continue
    elif event == "1500m":
        continue
    elif event == "3000m":
        continue
    elif event == "5000m":
        continue
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
        if (not words[0].isdigit() and processing == 1):
            break
        if (num_words > 7 and words[0] == "1" and processing == 0):
            processing = 1
        if (processing == 0):
            continue
        if not words[0].isdigit():
            break

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
        print(max_score, " ", max_name, " ", list[0], " ", list[1], " ", list[2], " ", list[3], " ", list[4], " ", list[5])
        done_with[max_name] = True
