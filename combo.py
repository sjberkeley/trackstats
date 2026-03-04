#
# create combo tables (e.g. 100/200/400 combo)
#
from datetime import datetime
import utils         # my utils
from Alltime import Alltime
from WA_toplists import WA_toplists

event_name_map = {}
score_maps = {}
utils.init_score_maps(event_name_map, score_maps)

#gender, event, field_event = utils.get_args(sys.argv)
this_year = datetime.now().year

earliest_date = this_year
athletes = {}     # dictionary of lists

num_events = 3
event_num = 0
data_source = WA_toplists()
source_type = type(data_source)

for gender in ("men", "women"):
    urls = data_source.get_urls(gender, True)
    if gender == "women":
        continue

    for url in urls:
        if url != "100 metres" and url != "200 metres"  and url != "400 metres":
        #if url != "800 metres" and url != "1500 metres":
        #and url != "10000 metres" and url != "half-marathon" and url != "marathon":
        #if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay":
            #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
            #or url == "Javelin throw" \
            #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue

        event = url        
        #print(gender, " ", event)
        lines = data_source.get_lines_from_urls(urls[url])
        # process data
        processing = 0
        index = 0
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
            #if nation != "IRL":
            #    continue
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
            if list[index] == "0":    # crash here may mean num_events not updated
                list[index] = performance
                list[index + 1] = score
        event_num = event_num + 1

# manual updates for marks below the performance cutoff of alltime-athletics
utils.manual_updates(source_type, athletes)

# now create a map with each athlete's aggregate score as the key
done_with = {}
count = 0

html_page = False   # HTML table or plain text list
if html_page:
    file1 = open("combo.html", "w")
    html = "<table border='1' style='border-collapse:collapse;'>\n"

for athlete in athletes.keys():
    if done_with.get(athlete) != None:
        continue

    max_score = 0
    for name in athletes.keys():
        if done_with.get(name) != None:
            continue
        list = athletes[name]
        total_score = 0
        skip = False
        for ii in range(0, num_events):
            if list[ii * 2 + 1] == "0":
                skip = True
            total_score = total_score + int(list[ii * 2 + 1])
        if skip:
            continue
        if total_score > max_score:
            max_score = total_score
            max_name = name

    if max_score > 0:
        list = athletes[max_name]
        count = count + 1

        if html_page:
            html += "  <tr>\n"
            html += "    <td style='padding:5px;'>" + str(count) + "</td>\n"
            html += "    <td style='padding:5px;'>" + str(max_score) + "        </td>\n"
            html += "    <td style='padding:5px;'>" + max_name + "        </td>\n"
            for mark in range(0, num_events*2, 2):
                html += "    <td style='padding:5px;'>" + list[mark] + "(" + list[mark+1] + ")        </td>\n"
            html += "  </tr>\n"
        else:
            print(("%3d. %4d %27s") % \
              (count, max_score, max_name), end="")
            for mark in range(0, num_events*2, 2):
                print(("%8s (%4s)") % \
                  (list[mark], list[mark+1]), end="")
            print("")
        done_with[max_name] = True

if html_page:
    html += "</table>"
    file1.write(html)
    file1.close

