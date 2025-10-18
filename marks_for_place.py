#
# Best marks for place in each event. Output option plain text or html table.
#

import utils         # my utils
from Alltime import Alltime
from WA_toplists import WA_toplists

data_source = WA_toplists()

event_name_map = {}

#gender, event, field_event = utils.get_args(sys.argv)

#file1 = open("marks_for_place", "w")
html_page = False   # HTML table or plain text list
if html_page:
    file1 = open("marks_for_place.html", "w")
    html = "<table border='1' style='border-collapse:collapse;'>\n"

for gender in ("men", "women"):
    #if gender == "women":
    #    continue

    score_maps = {}
    utils.init_score_maps(event_name_map, score_maps)
    urls = data_source.get_urls(gender, False)

    for url in urls:
        #if url != "200 metres":
        #    continue
        if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
            #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
            #or url == "Javelin throw" \
            #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue

        event = url
        if html_page:
            html += "  <tr>\n"
            html += "    <td colspan='5' style='padding:5px; background-color:lightblue;'><b>" + event + " - " + gender + "</b></td>\n"
            html += "  </tr>\n"    
        print(" ")
        #print(("\033[1m%20s %6s\033[0m") % (event, gender))
        print(("%20s %6s") % (event, gender))
        print(" ")
        lines = data_source.get_lines_from_urls(urls[url])
        # process data
        processing = 0
        num_lines = len(lines)
        line_num = 0
        place = 1
        mfp = []
        tied = []
        num_tied = 0
        prev_data = []
        in_sequence = False
        while line_num < num_lines:
            status, words, processing, line_num = data_source.strip_preamble(lines, line_num, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, year, performance, nation, this_date, city, position, date, dob, line_num = data_source.get_stats(words, lines, line_num)
            # filter out non-digit characters in the position (h, sf, etc.), except f (final)
            final = True
            if len(position) == 0:
                pos = 1
            elif not position[0].isdigit():
                pos = 1
            else:
                #if not position.isdigit():
                #    print(position)
                poslen = len(position)
                string1 = ""
                string2 = ""
                for ii in range(poslen):
                    if position[ii].isdigit():
                        string2 = string1 + position[ii]
                        string1 = string2
                    elif position[ii] != "f":
                        final = False
                        break
                    else:
                        break
                pos = int(string1)

            if not final:
                continue
            # groups of tied athletes
            if len(prev_data) == 0:
                prev_data.append(pos)
                prev_data.append(performance)
                prev_data.append(name)
                prev_data.append(city)
                prev_data.append(date)
            else:
                if pos == prev_data[0] and performance == prev_data[1] and city == prev_data[3] and date == prev_data[4]:
                    tied.append(prev_data)
                    in_sequence = True
                elif in_sequence:
                    tied.append(prev_data)
                    in_sequence = False
                prev_data = []
                prev_data.append(pos)
                prev_data.append(performance)
                prev_data.append(name)
                prev_data.append(city)
                prev_data.append(date)
            # best marks for place
            if pos <= len(mfp):
                data = mfp[pos-1]
                if data[0] == "":
                    data[0] = performance
                if performance == data[0]:
                    data[1].append(name)
                    data[2].append(city)
                    data[3].append(date)
            else:       # no entries for this position yet
                num_new = pos - len(mfp)
                for ii in range(num_new):
                    data = []
                    if ii == num_new - 1:
                        data.append(performance)
                        names = []
                        names.append(name)
                        data.append(names)
                        cities = []
                        cities.append(city)
                        data.append(cities)
                        dates = []
                        dates.append(date)
                        data.append(dates)
                    else:
                        data.append("")
                        names = []
                        data.append(names)
                        cities = []
                        data.append(cities)
                        dates = []
                        data.append(dates)
                    mfp.append(data)
                    mark = performance
        # output
        prev_range_label = ""
        for ii in range(len(mfp)):
            if ii >= 20:        # discard places higher than 20
                break
            data = mfp[ii]
            mark = data[0]
            names = data[1]
            cities = data[2]
            dates = data[3]

            # Insert tied groups
            skip = 0
            for jj in range(len(tied)):
                if skip > 0:
                    skip -= 1
                    continue
                data = tied[jj]
                pos2 = data[0]
                mark2 = data[1]
                if pos2 == ii and mark2 == mark:
                    # construct range label
                    range_label = ""
                    count = 0
                    for kk in range(jj+1, len(tied)):
                        if tied[kk][0] == pos2:
                            count += 1
                        else:
                            range_label = str(pos2) + "-" + str(pos2 + count)
                            break
                    for kk in range(jj, len(tied)):
                        if tied[kk][0] != pos2:
                            break
                        data = tied[kk]
                        if kk == jj and range_label != prev_range_label:
                            if html_page:
                                html += "  <tr>\n"
                                html += "    <td style='padding:5px;'>" + range_label + "</td>\n"
                                for mm in range(1, 5):
                                    html += "    <td style='padding:5px;'>" + data[mm] + "</td>\n"
                                html += "  </tr>\n"
                            else:
                                print(("%5s %9s %25s %50s %11s") % (range_label, data[1], data[2], data[3], data[4]))
                        else:
                            if html_page:
                                html += "  <tr>\n"
                                html += "    <td style='padding:5px;'> </td>\n"
                                html += "    <td style='padding:5px;'> </td>\n"
                                for mm in range(2, 5):
                                    html += "    <td style='padding:5px;'>" + data[mm] + "</td>\n"
                                html += "  </tr>\n"
                            else:
                                print(("%41s %50s %11s") % (data[2], data[3], data[4]))
                    skip = count
                    prev_range_label = range_label
            # print regular mark/group of marks 
            if mark != "":
                if html_page:
                    html += "  <tr>\n"
                    html += "    <td style='padding:5px;'>" + str(ii+1) + "</td>\n"
                    html += "    <td style='padding:5px;'>" + str(mark) + "</td>\n"
                    html += "    <td style='padding:5px;'>" + names[0] + "</td>\n"
                    html += "    <td style='padding:5px;'>" + cities[0] + "</td>\n"
                    html += "    <td style='padding:5px;'>" + dates[0] + "</td>\n"
                    html += "  </tr>\n"
                else:
                    print(("%5s %9s %25s %50s %11s") % (ii+1, mark, names[0], cities[0], dates[0]))
                for jj in range(1, len(names)):
                    if html_page:
                        html += "  <tr>\n"
                        html += "    <td style='padding:5px;'> </td>\n"
                        html += "    <td style='padding:5px;'> </td>\n"
                        html += "    <td style='padding:5px;'>" + names[jj] + "</td>\n"
                        html += "    <td style='padding:5px;'>" + cities[jj] + "</td>\n"
                        html += "    <td style='padding:5px;'>" + dates[jj] + "</td>\n"
                        html += "  </tr>\n"
                    else:
                        print(("%41s %50s %11s") % (names[jj], cities[jj], dates[jj]))

        if html_page:
            html += "<br>\n"

if html_page:
    html += "</table>"
    file1.write(html)
    file1.close

#file1.close
