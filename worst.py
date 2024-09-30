#
# Ranking of nations by total WA points scored
#

from datetime import datetime
import utils         # my utils
import pandas as pd
import utils

#
# main program
#

event_name_map = {}
score_maps = {}
utils.init_score_maps(event_name_map, score_maps)

#gender, event, field_event = utils.get_args(sys.argv)
this_year = datetime.now().year

earliest_date = this_year
total_scores = {}

for gender in ("men", "women"):

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
            name, date, performance, nation, this_date, city, position, full_date = utils.get_stats(words)
            score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)
            if nation in total_scores.keys():
                total_scores[nation] = total_scores[nation] + int(score)
            else:
                total_scores[nation] = int(score)
            if date < earliest_date:
                earliest_date = date

for nation in total_scores.keys():
    print(("%3s %12d") % (nation, total_scores[nation]))

