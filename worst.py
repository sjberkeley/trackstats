#
# Ranking of nations by total WA points scored
#

from datetime import datetime
import utils         # my utils
import pandas as pd
import utils
from Alltime import Alltime
from WA_toplists import WA_toplists

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
data_source = WA_toplists()

for gender in ("men", "women"):
    urls = data_source.get_urls(gender, False)

    for url in urls:
        if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
            #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
            #or url == "Javelin throw" \
            #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue

        event = url        
        print(gender, " ", event)
        lines = data_source.get_lines_from_urls(urls[url])
        # process data
        processing = 0
        num_lines = len(lines)
        line_num = 0
        while line_num < num_lines:

            status, words, processing, line_num = data_source.strip_preamble(lines, line_num, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, year, performance, nation, this_date, city, position, date, dob, line_num = data_source.get_stats(words, lines, line_num)
            score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)
            if nation in total_scores.keys():
                total_scores[nation] = total_scores[nation] + int(score)
            else:
                total_scores[nation] = int(score)
            if year < earliest_date:
                earliest_date = year

for nation in total_scores.keys():
    print(("%3s %12d") % (nation, total_scores[nation]))

