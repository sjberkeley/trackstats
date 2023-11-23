from datetime import datetime
import utils         # my utils
import bar_chart_race2 as bcrace
import pandas as pd
import utils

def get_WA_score(gender, event, performance):
    wa_event = event_name_map[event]
    map = score_maps[wa_event]

    if len(map) == 0:
        filename = "scores/" + wa_event + "." + gender + ".scores"
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
                map[words[0]] = words[1]

    perf_str = performance   # str(performance)
    if perf_str[-2] == ".":      # conversion to float may have truncated a trailing zero
        perf_str += "0"
    
    if event == "half-marathon" or event == "marathon" or event == "20 km race walk" or event == "50 km race walk":
        index = perf_str.find(".")
        if index != -1:      # truncate decimal
            perf_str = perf_str[0:index]

    # if the performance does not exist in the map, find the next lower performance that does
    field_event = utils.is_field_event(event)

    if event == "Decathlon" or event == "Heptathlon":
        perf_units = int(perf_str)
        if perf_units < 1000 or perf_units > 10000:
            return 0
        while map.get(perf_str) == None:       # key does not exist
            perf_units = int(perf_str)
            perf_units = perf_units - 1
            perf_str = str(perf_units)
    elif field_event:
        if perf_str[-4] == ".":   # one too many decimal places, round down
            perf_str = perf_str[:-1]
        perf_units = float(perf_str)
        while map.get(perf_str) == None:       # key does not exist
            perf_units = round(perf_units - 0.01, 2)
            perf_str = str(perf_units)
            if perf_str[-2] == ".":
                perf_str += "0"
    else:            
        while map.get(perf_str) == None:       # key does not exist
            perf_units, hundredths = utils.hms_to_seconds(perf_str)
            if hundredths:
                perf_units = round(perf_units + 0.01, 2)
            else:
                perf_units = perf_units + 1
            perf_str = utils.seconds_to_hms(perf_units, hundredths)

    score = map[perf_str]
    return score

#
# main program
#

event_name_map = {}
score_maps = {}
utils.init_score_maps(event_name_map, score_maps)
#
# main program
#
#gender, event, field_event = utils.get_args(sys.argv)
this_year = datetime.now().year

earliest_date = this_year
events = {}
total_scores = {}

for gender in ("men", "women"):
    #event = "800 metres"

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
        last_date = 0
        records = []
        for line in lines:
            status, words, processing = utils.strip_preamble(line, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, date, performance, nation, this_date, city = utils.get_stats(words)
            score = get_WA_score(gender, event, performance)
            if city in total_scores.keys():
                scores = total_scores[city]
                for year in range(date, this_year+1):
                    if year in scores.keys():
                        scores[year] = scores[year] + int(score)
                    else:
                        scores[year] = int(score)
            else:
                scores = {}
                for year in range(date, this_year+1):
                    scores[year] = int(score)
                total_scores[city] = scores
            if date < earliest_date:
                earliest_date = date

num_rows = this_year - earliest_date

# Open csv file
file_name = "city_scores.csv"
file1 = open(file_name,"w")
# write header row
header = "city"
for city in total_scores.keys():
    header += "," + city
file1.write(header + "\n")

year = earliest_date
for row in range(num_rows+1):
    row_str = str(year)
    for city in total_scores.keys():
        scores = total_scores[city]
        row_str += ","
        if year in scores.keys():
            row_str += str(scores[year])
    year += 1
    file1.write(row_str + "\n")
    
file1.close

# create bar chart race
data = pd.read_csv("city_scores.csv", dtype=float)

data.set_index('city', inplace=True)

bcrace.bar_chart_race(
    df=data,
    filename="city_scores.mp4",  # Output filename
    title="Cumulative aggregate World Athletics scoring points by city",
    n_bars=20,
    period_fmt='{x:4.0f}',
    sort='desc_f',
    figsize=(7.5, 5),               # was (6, 3.5)
    steps_per_period=15,            # Number of steps per year
    period_length=750,             # Length of each year in milliseconds
    period_label={'x': .8, 'y': .8, 'ha': 'right', 'va': 'center', 'size': 32},
)

#time.sleep(10)
