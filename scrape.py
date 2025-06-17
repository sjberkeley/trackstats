#
# scrape alltime-athletics event page and create csv file for input to bar chart race generator
#

#import requests
from datetime import datetime
import sys
import utils         # my utils
from Alltime import Alltime
from WA_toplists import WA_toplists

#
# main program
#
#gender, event, field_event = utils.get_args(sys.argv)
def build_csv(gender, event, num_perfs):
    data_source = Alltime()
    #gender = "men"
    #event = "800 metres"
    field_event = utils.is_field_event(event)

    this_year = datetime.now().year
    earliest_num_perfs = this_year
    starting_year = 0      # start from this year

    m_urls = data_source.get_urls("men", False)
    w_urls = data_source.get_urls("women", False)

    if gender == "women":
        url = w_urls[event]
    else:
        url = m_urls[event]

    lines = data_source.get_lines_from_urls(url)

    athletes = {}     # dictionary of lists of lists
    active = {}       # earliest and latest year active
    nations = {}      # first country represented

    # find earliest year
    earliest = utils.find_earliest_year(lines, this_year)

    # process data
    processing = 0
    counter = 0
    num_lines = len(lines)
    line_num = 0
    while line_num < num_lines:

        status, words, processing, line_num = data_source.strip_preamble(lines, line_num, processing)
        if status == 0:
            continue
        elif status == 1:
            break

        # extract performance, name and date (year)
        counter += 1
        name, year, performance, nation, this_date, city, position, date, line_num = data_source.get_stats(words, lines, line_num)

        # populate dictionary
        if name in athletes.keys():
            list_of_lists = athletes[name]
            active_range = active[name]
        else:
            list_of_lists = []
            for yy in range(earliest, this_year+1):
                list = []
                list_of_lists.append(list)
            athletes[name] = list_of_lists
            active_range = [this_year, 0]
            active[name] = active_range
            nations[name] = nation
        
        for yy in range(year, this_year+1):
            list = list_of_lists[yy-earliest]
            if len(list) < num_perfs:
                list.append(performance)
            else:
                if year < earliest_num_perfs:
                    earliest_num_perfs = year

        if year < active_range[0]:
            active_range[0] = year
        if year > active_range[1]:
            active_range[1] = year

    if earliest_num_perfs < starting_year:
        earliest_num_perfs = starting_year
    array_2d = []
    header = []
    header.append("name")
    for year in range(earliest_num_perfs, this_year+1):
        header.append(str(year))
    array_2d.append(header)

    for name in athletes.keys():
        active_range = active[name]
        name_str = name + " (" + nations[name] + ") " + str(active_range[0]) + "-" + str(active_range[1])
        array_1d = []
        array_1d.append(name_str)
        list_of_lists = athletes[name]
        any_marks = False
        for year in range(earliest_num_perfs, this_year+1):    
            list = list_of_lists[year-earliest]
            if len(list) < num_perfs:
                array_1d.append("0.0")
            else:
                perf_sum = 0.0
                for perf in range(0,num_perfs):
                    perf_in_seconds, hundredths = utils.hms_to_seconds(list[perf])
                    perf_sum += perf_in_seconds    # 800 times not handled
                perf_average = perf_sum / num_perfs
                array_1d.append(str(perf_average))  # * 1000.0
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
        line = ""
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
                    # mark = utils.seconds_to_hms(float(array_2d[jj][ii]))
                    mark = "{:.3f}".format(float(array_2d[jj][ii]))
                    line += mark
                else:
                    line += array_2d[jj][ii]
            if jj < num_rows-1:
                line += ","
        line += "\n"
        file1.write(line)

    file1.write(line)     # add an extra copy of the last year to make it easier to pause there
    file1.close


#build_csv("men", "800 metres", 10)
#time.sleep(10)

