#
# Ranking of athletes by how many of their last 10 finals are world records and wins
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

#gender, event, field_event = utils.get_args(sys.argv)

athletes = {}     # dictionary of lists
dates = {}
earliest = {}
all_lines = {}
max_comps = 500
data_source = WA_toplists()

for gender in ("men", "women"):
    urls = data_source.get_urls(gender, False)
    #if gender == "women":
        #continue

    for url in urls:
        if url != "200 metres":
        #if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
            #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
            #or url == "Javelin throw" \
            #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue

        event = url        
        #print(gender, " ", event)
        lines = data_source.get_lines_from_urls(urls[url])

        gender_event = gender + event
        all_lines[gender_event] = lines

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
    # check that at least one date is 1990 or later
    ok = False
    for date in datelist:
        year = date[0:4]
        if year >= "1980":
            ok = True
            break
    if not ok:
        continue

    datelist.sort(reverse=True)
    if len(datelist) < max_comps:
        earliest[name] = datelist[len(datelist)-1]
    else:
        earliest[name] = datelist[max_comps-1]

for gender_event in all_lines.keys():
    lines = all_lines[gender_event]
    wr_date = "9999.99.99"
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

print ("WRs  wins  comps  comps/WRs  comps/wins              name")
for name in athletes.keys():
    list = athletes[name]
    if list[2] > 0: # and list[0] > 10: # and list[0] == max_comps:
        ratio1 = float(list[0]) / float(list[2])
        ratio2 = float(list[0]) / float(list[1])
        print(("%2d   %3d    %3d    %3.3f      %3.3f  %27s") % (list[2], list[1], list[0], ratio1, ratio2, name))

