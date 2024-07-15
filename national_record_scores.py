#
# national records ranked by WA score
#
# After running this, run "sort -r scores.sorted"
#

import requests
from datetime import datetime
import utils         # my utils

event_name_map = {}

#gender, event, field_event = utils.get_args(sys.argv)
this_year = datetime.now().year

earliest_date = this_year
athletes = {}     # dictionary of lists

num_events = 3
event_num = 0
country = "IRL"
file1 = open("scores.sorted", "w")

for gender in ("men", "women"):
    score_maps = {}
    utils.init_score_maps(event_name_map, score_maps)
    if gender == "men":
        urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
    else:
        urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

    for url in urls:
        if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
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
            if nation == country:
                score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)
                if len(score) < 4:
                    file1.write(" ")
                file1.write(score + " " + gender + " " + event + " " + name + " " + performance + "\n")
                break

file1.close
