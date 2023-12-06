#
# generate bar chart race showing city rankings according to total WA scores
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
score_maps = {}
utils.init_score_maps(event_name_map, score_maps)

#gender, event, field_event = utils.get_args(sys.argv)
this_year = datetime.now().year

earliest_date = this_year
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
        for line in lines:
            status, words, processing = utils.strip_preamble(line, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, date, performance, nation, this_date, city = utils.get_stats(words)
            score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)
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
    steps_per_period=30,            # Number of steps per year
    period_length=1500,             # Length of each year in milliseconds
    period_label={'x': .8, 'y': .8, 'ha': 'right', 'va': 'center', 'size': 32},
)

#time.sleep(10)
