#
# Ranking of athletes by how many of their last 10 finals are world records and wins
#

from datetime import datetime
import utils         # my utils
import bar_chart_race2 as bcrace
import pandas as pd
import utils

#
# main program
#

#gender, event, field_event = utils.get_args(sys.argv)

athletes = {}     # dictionary of lists
dates = {}
earliest = {}
all_lines = {}
max_comps = 10

for gender in ("men", "women"):

    if gender == "men":
        urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
    else:
        urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

    for url in urls:
        #if url != "100 metres":
        if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
            #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
            #or url == "Javelin throw" \
            #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue

        event = url        
        #print(gender, " ", event)
        lines = utils.get_lines_from_url(urls[url])

        gender_event = gender + event
        all_lines[gender_event] = lines

        # process data
        processing = 0
        for line in lines:
            status, words, processing = utils.strip_preamble(line, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, year, performance, nation, this_date, city, position, date = utils.get_stats(words)
            if not position.isnumeric():    # not a final
                continue
            # populate dictionary
            if name in dates.keys():
                datelist = dates[name]
            else:
                datelist = []
                dates[name] = datelist
            ymd = date[6:10] + "." + date[3:5] + "." + date[0:2]
            datelist.append(ymd)

for name in dates.keys():
    datelist = dates[name]
    datelist.sort(reverse=True)
    if len(datelist) < max_comps:
        earliest[name] = datelist[len(datelist)-1]
    else:
        earliest[name] = datelist[max_comps-1]

for gender_event in all_lines.keys():
    lines = all_lines[gender_event]
    wr_date = "9999.99.99"
    processing = 0
    for line in lines:
        status, words, processing = utils.strip_preamble(line, processing)
        if status == 0:
            continue
        elif status == 1:
            break

        # extract performance, name and date (year)
        name, year, performance, nation, this_date, city, position, date = utils.get_stats(words)
        ymd = date[6:10] + "." + date[3:5] + "." + date[0:2]
        WR = False
        if ymd < wr_date:     # it's a world record
            WR = True
            wr_date = ymd

        if not name in earliest.keys():    # fewer than max_comps performances
            continue
        if ymd < earliest[name]:
            continue
        # populate dictionary
        if name in athletes.keys():
            list = athletes[name]
        else:
            list = []
            for mark in range(3):
                list.append(0)
            athletes[name] = list
        
        if list[0] < max_comps:
            list[0] = list[0] + 1
            if position == "1":
                list[1] = list[1] + 1
            if WR:
                list[2] = list[2] + 1

print ("WRs wins comps name")
for name in athletes.keys():
    list = athletes[name]
    if list[2] > 0 and list[0] == max_comps:
        print(("%2d   %2d    %2d %27s") % (list[2], list[1], list[0], name))

