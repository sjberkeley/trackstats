import requests
from datetime import datetime
import sys
import utils         # my utils
#import bcr
#import time
#
# main program
#
gender, event, field_event = utils.get_args(sys.argv)

this_year = datetime.now().year
earliest_num_perfs = this_year
num_perfs = 10         # number of perfs to average
starting_year = 0      # start from this year

#m_urls = {}
#w_urls = {}

m_urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
w_urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

if gender == "women":
    url = w_urls[event]
else:
    url = m_urls[event]

lines = utils.get_lines_from_url(url)

athletes = {}     # dictionary of lists of lists

# find earliest year
earliest = utils.find_earliest_year(lines, this_year)

# process data
processing = 0
counter = 0
for line in lines:
    # Skip empty lines
    if not line.strip():
        continue
    words = line.split()
    num_words = len(words)
    # check for done with outdoor list
    if (num_words < 8 and processing == 1):
        break
    if (num_words > 7 and words[0] == "1" and processing == 0):
        processing = 1
    if (processing == 0):
        continue
    if not words[0].isdigit():
        break
    # extract performance, name and date (year)
    counter += 1
    name, date, performance = utils.get_stats(words)

    # populate dictionary
    if name in athletes.keys():
        list_of_lists = athletes[name]
    else:
        list_of_lists = []
        for yy in range(earliest, this_year):
            list = []
            list_of_lists.append(list)
        athletes[name] = list_of_lists

    for yy in range(date, this_year):
        list = list_of_lists[yy-earliest]
        if len(list) < num_perfs:
            list.append(performance)
        else:
            if date < earliest_num_perfs:
                earliest_num_perfs = date

if earliest_num_perfs < starting_year:
    earliest_num_perfs = starting_year
array_2d = []
header = []
header.append("name")
for year in range(earliest_num_perfs, this_year):
    header.append(str(year))
array_2d.append(header)
for name in athletes.keys():
    array_1d = []
    array_1d.append(name)
    list_of_lists = athletes[name]
    any_marks = False
    for year in range(earliest_num_perfs, this_year):    
        list = list_of_lists[year-earliest]
        if len(list) < num_perfs:
            array_1d.append("0.0")
        else:
            perf_sum = 0.0
            for perf in range(0,num_perfs):
                perf_in_seconds, hundredths = utils.hms_to_seconds(list[perf])
                perf_sum += perf_in_seconds    # 800 times not handled
            perf_average = perf_sum / num_perfs
            array_1d.append(str(perf_average * 1000.0))  # * 100.0
            any_marks = True
    if (any_marks):
        array_2d.append(array_1d)

# transpose and write to file
# data is transposed for bar_chart_race versus Flourish
# Open csv file
file_name = gender + event + ".csv"
file1 = open(file_name,"w")

num_rows = len(array_2d)
num_cols = len(array_2d[0])

for ii in range(num_cols):
    if ii > 0:
        any_values = False
        for jj in range(num_rows):
            if ii > 0 and jj > 0 and array_2d[jj][ii] != "0.0":
                any_values = True
        if not any_values:
            continue
    for jj in range(num_rows):
        if array_2d[jj][ii] != "0.0":
            if ii > 0 and jj > 0:
                mark = "{:.3f}".format(float(array_2d[jj][ii]))
                file1.write(mark)
            else:
                if ii > 0 and jj == 0:
                    file1.write(array_2d[jj][ii] + '-01-01')
                else:
                    file1.write(array_2d[jj][ii])
        if jj < num_rows-1:
            file1.write(",")
    file1.write("\n")
file1.close

#time.sleep(10)

#bcr.create_bar_chart_race('menHigh jump.csv', 'menHJ.mp4', field_event)
