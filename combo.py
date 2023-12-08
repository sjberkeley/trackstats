#
# create combo tables (e.g. 100/200/400 combo)
#

import requests
from datetime import datetime
import utils         # my utils

event_name_map = {}
score_maps = {}
utils.init_score_maps(event_name_map, score_maps)

#gender, event, field_event = utils.get_args(sys.argv)
this_year = datetime.now().year

earliest_date = this_year
athletes = {}     # dictionary of lists

num_events = 5
event_num = 0

for gender in ("men", "women"):
    if gender == "men":
        urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
    else:
        continue
        #urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

    for url in urls:
        if url != "800 metres" and url != "1500 metres" \
            and url != "5000 metres" and url != "10000 metres" and url != "marathon":
        #if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
            #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
            #or url == "Javelin throw" \
            #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue

        event = url        
        print(gender, " ", event)
        lines = utils.get_lines_from_url(urls[url])
        # process data
        processing = 0
        for line in lines:
            status, words, processing = utils.strip_preamble(line, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, date, performance, nation, this_date, city = utils.get_stats(words)
            score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)

            # populate dictionary
            if name in athletes.keys():
                list = athletes[name]
            else:
                list = []
                athletes[name] = list
            if len(list) == event_num * 2:
                list.append(performance)
                list.append(score)
        event_num = event_num + 1

# now create a map with each athlete's aggregate score as the key
done_with = {}
count = 0
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
        count = count + 1
        print(("%3d. %4d %25s %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s)") % \
              (count, max_score, max_name, list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9]))
        done_with[max_name] = True

