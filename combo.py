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

num_events = 3
event_num = 0

for gender in ("men", "women"):
    if gender == "men":
        #urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
        continue
    else:
        urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

    for url in urls:
        if url != "100 metres" and url != "200 metres" and url != "400 metres":
            #and url != "5000 metres" and url != "2000 metres" and url != "2 Miles":
        #if url != "100 metres" and url != "200 metres" and url != "400 metres":
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
            name, year, performance, nation, this_date, city, position, date = utils.get_stats(words)
            score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)

            # populate dictionary
            if name in athletes.keys():
                list = athletes[name]
            else:
                list = []
                for mark in range(num_events * 2):
                    list.append("0")
                athletes[name] = list
            # check if this is the first mark for this athlete
            index = event_num * 2
            if list[index] == "0":
                list[index] = performance
                list[index + 1] = score
        event_num = event_num + 1

# manual updates
if "Usain Bolt" in athletes.keys():
    list = athletes["Usain Bolt"]
    list[4] = "45.28"
    list[5] = "1160"
    list = athletes["Yohan Blake"]
    list[4] = "46.32"
    list[5] = "1090"
    list = athletes["Wallace Spearmon"]
    list[4] = "45.22"
    list[5] = "1165"
    list = athletes["Asafa Powell"]
    list[4] = "45.94"
    list[5] = "1115"
    list = athletes["Obadele Thompson"]
    list[4] = "45.38"
    list[5] = "1154"
    list = athletes["Noah Lyles"]
    list[4] = "47.04"
    list[5] = "1042"
    list = athletes["Frank Fredericks"]
    list[4] = "46.28"
    list[5] = "1093"
    list = athletes["Walter Dix"]
    list[4] = "46.75"
    list[5] = "1061"
    list = athletes["Zharnel Hughes"]
    list[4] = "46.58"
    list[5] = "1073"
    list = athletes["Erriyon Knighton"]
    list[4] = "46.15"
    list[5] = "1101"
    list = athletes["Francis Obikwelu"]
    list[4] = "46.29"
    list[5] = "1092"
    list = athletes["Calvin Smith"]
    list[4] = "46.39"       # Calvin Smith junior ran 44.81
    list[5] = "1085"
    list = athletes["Isaac Makwala"]
    list[0] = "10.22"
    list[1] = "1138"
    list = athletes["Steven Gardiner"]
    list[0] = "10.35"
    list[1] = "1089"
    list = athletes["Jereem Richards"]
    list[0] = "10.19"
    list[1] = "1142"

if "Marita Koch" in athletes.keys():
    list = athletes["Merlene Ottey"]
    list[4] = "51.12"
    list[5] = "1161"
    list = athletes["Evelyn Ashford"]
    list[4] = "51.08"
    list[5] = "1162"
    list = athletes["Veronica Campbell-Brown"]
    list[4] = "52.24"
    list[5] = "1117"
    list = athletes["Sherone Simpson"]
    list[4] = "51.25"
    list[5] = "1156"
    list = athletes["Kerron Stewart"]
    list[4] = "51.83"
    list[5] = "1133"
    list = athletes["Brittany Brown"]
    list[4] = "51.15"
    list[5] = "1160"
    list = athletes["Chandra Cheeseborough"]
    list[0] = "11.13"
    list[1] = "1172"
    list = athletes["Kathy Cook"]
    list[0] = "11.10"
    list[1] = "1178"
    list = athletes["Irena Szewinska"]
    list[0] = "11.13"
    list[1] = "1172"
    list = athletes["Cathy Freeman"]
    list[0] = "11.24"
    list[1] = "1148"
    list = athletes["Salwa Eid Naser"]
    list[0] = "11.24"
    list[1] = "1148"
    list = athletes["Rhasidat Adeleke"]
    list[0] = "11.13"
    list[1] = "1172"
    if num_events == 4:
        list = athletes["Shaunae Miller-Uibo"]
        list[6] = "2:12.86"
        list[7] = "983"
        list = athletes["Irina Privalova"]
        list[6] = "2:09.40"
        list[7] = "1000"
        list = athletes["Christine Mboma"]
        list[6] = "2:03.27"
        list[7] = "1104"
        list = athletes["Aminatou Seyni"]
        list[6] = "2:18.86"
        list[7] = "849"

#if "Hicham El Guerrouj" in athletes.keys():
    #list = athletes["Hicham El Guerrouj"]
    #list[10] = "8:06.61"
    #list[11] = "1274"

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
        if list[0] == "0" or list[2] == "0":  # or list[4] == "0" or list[6] == "0" or list[8] == "0" or list[10] == "0":
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
        if num_events == 2:
            print(("%3d. %4d %27s %8s (%4s) %8s (%4s)") % \
              (count, max_score, max_name, list[0], list[1], list[2], list[3]))
        elif num_events == 3:
            print(("%3d. %4d %27s %8s (%4s) %8s (%4s) %8s (%4s)") % \
              (count, max_score, max_name, list[0], list[1], list[2], list[3], list[4], list[5]))
        elif num_events == 4:
            print(("%3d. %4d %27s %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s)") % \
              (count, max_score, max_name, list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7]))
        elif num_events == 5:
            print(("%3d. %4d %27s %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s)") % \
              (count, max_score, max_name, list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9]))
        else:    # 1500 through 5000 in distance order
            print(("%3d. %4d %27s %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s) %8s (%4s)") % \
              (count, max_score, max_name, list[0], list[1], list[2], list[3], list[8], list[9], list[4], list[5], list[10], list[11], list[6], list[7]))
        done_with[max_name] = True

