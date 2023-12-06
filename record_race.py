#
# generate bar chart race showing the relative advance of world records measured by World Athletics scores
#

from datetime import datetime
import utils         # my utils
import bar_chart_race2 as bcrace
import pandas as pd
import utils


def build_scores_csv(file_name):
    event_name_map = {}
    score_maps = {}
    utils.init_score_maps(event_name_map, score_maps)
    
    #gender, event, field_event = utils.get_args(sys.argv)
    this_year = datetime.now().year
    
    earliest_date = this_year
    events = {}
    
    for gender in ("men", "women"):
    
        if gender == "men":
            continue
            #gender_name = "men"
            #urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
        else:
            #continue
            gender_name = "women"
            urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")
    
        for url in urls:
            if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay" \
                or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk":
                continue
    
            event = url
            scores = []
            events[event] = scores        
            print(gender, " ", event)
            lines = utils.get_lines_from_url(urls[url])
            # process data
            processing = 0
            current_date = this_year + 1
            for line in lines:
                status, words, processing = utils.strip_preamble(line, processing)
                if status == 0:
                    continue
                elif status == 1:
                    break
    
                # extract performance, name and date (year)
                name, date, performance, nation, this_date, city = utils.get_stats(words)
                score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)
                if date < current_date:
                    num_years = current_date - date
                    for year in range(num_years):
                        scores.append(score)
                    current_date = date
    
                if current_date < earliest_date:
                    earliest_date = current_date
    
    num_rows = this_year - earliest_date
    
    # Open csv file
    file1 = open(file_name + ".csv","w")
    # write header row
    header = "event"
    for this_event in events.keys():
        header += "," + this_event
    file1.write(header + "\n")
    
    year = earliest_date
    for row in range(num_rows+1):
        row_str = str(year)
        for this_event in events.keys():
            scores = events[this_event]
            index = num_rows - row
            row_str += ","
            if index < len(scores):
                row_str += str(scores[index])
        year += 1
        file1.write(row_str + "\n")
        
    file1.write(row_str + "\n")
    file1.close

#
# main program
#
file_name = "record_race"

build_scores_csv(file_name)

# create bar chart race
data = pd.read_csv(file_name + ".csv", dtype=float)

data.set_index('event', inplace=True)

bcrace.bar_chart_race(
    df=data,
    filename=file_name + ".mp4",  # Output filename
    title="World records by World Athletics scoring points - women",
    n_bars=20,
    period_fmt='{x:4.0f}',
    sort='desc_f',
    figsize=(7.5, 5),               # was (6, 3.5)
    steps_per_period=30,            # Number of steps per year
    period_length=1500,             # Length of each year in milliseconds
    period_label={'x': .8, 'y': .8, 'ha': 'right', 'va': 'center', 'size': 32},
)
