#
# create combo tables (e.g. 100/200/400 combo)
#

import requests
from datetime import datetime
import utils         # my utils

map100 = {}
map200 = {}
map400 = {}
map800 = {}
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
    elif event == "800m":
        map = map800
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
    field_event = utils.is_field_event(event)

    while map.get(perf_str) == None:       # key does not exist
        perf_units, hundredths = utils.hms_to_seconds(perf_str)
        if hundredths:
            perf_units = round(perf_units + 0.01, 2)
        else:
            perf_units = perf_units + 1
        perf_str = utils.seconds_to_hms(perf_units, hundredths)

    score = map[perf_str]
    return score

#
# main program
#
gender = "women"
num_events = 2

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
    urls.append(w_urls["800 metres"])
    urls.append(w_urls["1500 metres"])
    urls.append(w_urls["3000 metres"])
    urls.append(w_urls["5000 metres"])

else:
    urls.append(m_urls["100 metres"])
    urls.append(m_urls["200 metres"])
    urls.append(m_urls["400 metres"])
    urls.append(m_urls["110m hurdles"])
    urls.append(m_urls["400m hurdles"])
    urls.append(m_urls["800 metres"])
    urls.append(m_urls["1500 metres"])
    urls.append(m_urls["3000 metres"])
    urls.append(m_urls["5000 metres"])

athletes = {}     # dictionary of lists
first = 5         # first event on the list
for event in ("100m", "200m", "400m", "110mH", "400mH", "800m", "1500m", "3000m", "5000m"):
    if event == "100m":
        continue
    elif event == "200m":
        continue
    elif event == "400m":
        continue
    elif event == "110mH":
        continue
    elif event == "400mH":
        continue
    elif event == "800m":
        event_num = 0
    elif event == "1500m":
        event_num = 1
    elif event == "3000m":
        continue
    elif event == "5000m":
        continue
    url = urls[first + event_num]

    lines = utils.get_lines_from_url(url)

    # process data
    processing = 0
    counter = 0
    for line in lines:
        status, words, processing = utils.strip_preamble(line, processing)
        if status == 0:
            continue
        elif status == 1:
            break

        # extract performance, name and date (year)
        counter += 1
        name, date, performance, nation, day, city = utils.get_stats(words)
        #if nation != "USA":
            #continue
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
        print(max_score, " ", max_name, " ", list[0], " ", list[1], " ", list[2], " ", list[3])
        done_with[max_name] = True
