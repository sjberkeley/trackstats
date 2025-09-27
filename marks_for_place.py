#
# Best marks for place in each event
#

import utils         # my utils
from Alltime import Alltime
from WA_toplists import WA_toplists

data_source = WA_toplists()

event_name_map = {}

#gender, event, field_event = utils.get_args(sys.argv)

#file1 = open("marks_for_place", "w")

for gender in ("men", "women"):
    #if gender == "men":
        #continue

    score_maps = {}
    utils.init_score_maps(event_name_map, score_maps)
    urls = data_source.get_urls(gender, False)

    for url in urls:
        if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
            #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
            #or url == "Javelin throw" \
            #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue

        event = url     
        print("")   
        print(("%20s %6s") % (event, gender))
        print("")
        lines = data_source.get_lines_from_urls(urls[url])
        # process data
        processing = 0
        num_lines = len(lines)
        line_num = 0
        place = 1
        while line_num < num_lines:
            status, words, processing, line_num = data_source.strip_preamble(lines, line_num, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, year, performance, nation, this_date, city, position, date, dob, line_num = data_source.get_stats(words, lines, line_num)
            if position[0:1] == str(place):
                print(("%3s %9s %25s %50s %11s") % (position[0:1], performance, name, city, date))
                place = place + 1
                if place > 20:
                    break

#file1.close
