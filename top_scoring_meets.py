#
# generate sorted list of meets according to total WA scores
# two-day meets counted (e.g. Diamond League finals) but not multi-day championships
#

from datetime import datetime
import utils         # my utils
import bar_chart_race2 as bcrace
import pandas as pd
import utils

#
# main program
#

event_name_map = {}
all_years = {}
all_year_dates = {}

max_range = 12

for gender in ("men", "women"):
    score_maps = {}
    utils.init_score_maps(event_name_map, score_maps)

    if gender == "men":
        urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
    else:
        urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

    for url in urls:
        #if url != "110m hurdles" and url != "100 metres" and url != "400 metres":
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
            # exclude heats and semis
            if len(position) == 3 and (position[1]=="h" or position[1]=="s"):
                continue
            if len(position) == 4 and (position[1]=="h" or position[1]=="s" or position[2]=="h" or position[2]=="s"):
                continue
            
            score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)

            ymd = full_date[6:10] + "." + full_date[3:5] + "." + full_date[0:2]
            city_year = city + "." + str(date)
            if city_year in all_years.keys():
                scores = all_years[city_year]
                year_dates = all_year_dates[city_year]
                if ymd in scores.keys():
                    scores[ymd] = scores[ymd] + int(score)
                else:
                    scores[ymd] = int(score)
                    year_dates.append(ymd)
                
            else:
                scores = {}
                scores[ymd] = int(score)
                all_years[city_year] = scores
                year_dates = []
                year_dates.append(ymd)
                all_year_dates[city_year] = year_dates

# Open file
file_name = "meets.unsorted"
file1 = open(file_name,"w")
file_name = "championships.unsorted"
file2 = open(file_name,"w")
for city_year in all_years.keys():
    scores = all_years[city_year]
    year_dates = all_year_dates[city_year]
    year_dates.sort(reverse=False)

    first = 0
    last = 0
    total_score = 0
    num_dates = len(year_dates)
    for ii in range(num_dates):
        done = False
        total_score = total_score + scores[year_dates[ii]]
        if ii == num_dates - 1:
            gap = 999               # write before exiting
        else:
            gap = utils.near(year_dates[ii], year_dates[ii+1]) - 2

        if last - first < 2:        # one or two day meet
            max_gap = 0
        else:
            max_gap = 2             # championship meet

        if gap > max_gap:
            done = True
        elif last - first + gap + 1 > max_range:   # done with championship meet
            done = True

        if done:
            duration = last - first + 1
            if duration <= 2:
                file1.write(("%8d  %30s  %3d  %10s %10s") % (total_score, city_year, duration, year_dates[first], year_dates[last]))
                file1.write("\n")
            else:
                file2.write(("%8d  %30s  %3d  %10s %10s") % (total_score, city_year, duration, year_dates[first], year_dates[last]))
                file2.write("\n")                

            total_score = 0
            first = last + 1
            last = first
        else:
            last = last + 1

file1.close
file2.close