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
    if gender == "women":
        continue

    score_maps = {}
    utils.init_score_maps(event_name_map, score_maps)
    urls = data_source.get_urls(gender, False)

    for url in urls:
        if url != "High jump":
            continue
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
        tied_names = []
        tied_sequence = 0    # not in progress
        current_performance = ""
        current_name = ""
        current_city = ""
        current_date = ""
        current_mark = ""
        mark = ""

        positions = []
        performances = []
        names = []
        cities = []
        dates = []
        current_perf = ""

        mfp = []
        while line_num < num_lines:
            status, words, processing, line_num = data_source.strip_preamble(lines, line_num, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, year, performance, nation, this_date, city, position, date, dob, line_num = data_source.get_stats(words, lines, line_num)
            if len(position) == 0:
                pos = 1
            elif not position[0].isdigit():
                pos = 1
            else:
                poslen = len(position)
                string1 = ""
                string2 = ""
                for ii in range(poslen):
                    if position[ii].isdigit():
                        string2 = string1 + position[ii]
                        string1 = string2
                    else:
                        break
                pos = int(string1)

            if pos <= len(mfp):
                data = mfp[pos-1]
                if performance == data[0]:
                    data[1].append(name)
                    data[2].append(city)
                    data[3].append(date)
            else:       # no entries for this position yet
                num_new = pos - len(mfp)
                for ii in range(num_new):
                    data = []
                    perf = ""
                    if ii == num_new - 1:
                        perf = performance
                    data.append(perf)
                    names = []
                    names.append(name)
                    data.append(names)
                    cities = []
                    cities.append(city)
                    data.append(cities)
                    dates = []
                    dates.append(date)
                    data.append(dates)
                    mfp.append(data)
                    mark = performance

            if place > 20:
                break

        for ii in range(len(mfp)):
            data = mfp[ii]
            mark = data[0]
            names = data[1]
            cities = data[2]
            dates = data[3]
            if mark != "":
                print(("%3s %9s %25s %50s %11s") % (ii+1, mark, names[0], cities[0], dates[0]))
            for jj in range(1, len(names)):
                print(("%39s %50s %11s") % (names[jj], cities[jj], dates[jj]))


#            if performance > mark:
#                # best performances
#                num_perfs = len(positions)
#                for ii in range(num_perfs):
#                    for jj in range(num_perfs):
#                        if positions[jj] == place:
#                            print(("%3s %9s %25s %50s %11s") % (positions[jj], performances[jj], names[jj], cities[jj], dates[jj]))
#                    place = place + 1
#                # tied performances
#
#                mark = performance
#            else:
#                if len(performances) > 0:
#                    current_perf = performances[0]
#                if int(this_position) >= place and current_perf == performance:
#                    positions.append(this_position)
#                    performances.append(performance)
#                    names.append(name)
#                    cities.append(city)
#                    dates.append(date)



#            if position[0:num_digits] == str(place+1):
#                place = place + 1
#                current_mark = ""
#
#            if position[0:num_digits] == str(place):
#                if current_mark == "":
#                    print(("%3s %9s %25s %50s %11s") % (position[0:num_digits], performance, name, city, date))
#                    current_mark = performance
#                elif performance == current_mark:
#                    print(("%39s %50s %11s") % (name, city, date))
#            elif position[0:num_digits] == str(place-1):
#                if performance == current_performance and city == current_city and date == current_date:
#                    tied_names.append(name)
#                    tied_sequence = 1       # in progress
#                else:
#                    tied_names = []
#                    tied_names.append(name)
#                    if len(tied_names) > 1:
#                        tied_sequence = 2   # completed
#                current_performance = performance
#                current_name = name
#                current_city = city
#                current_date = date
#            else:
#                if len(tied_names) > 1:
#                    tied_sequence = 2
#
#            if tied_sequence == 2:
#                num_tied = len(tied_names)
#                print(("%3s %9s %25s %50s %11s") % (position[0:num_digits], performance, tied_names[0], city, date))
#                for tied_index in range(1, num_tied):
#                    print(("%39s %50s %11s") % (tied_names[tied_index], city, date))
#                tied_names = []
#                tied_sequence = 0
#                current_performance = ""
#                current_name = ""
#                current_city = ""
#                current_date = ""


            
#file1.close
