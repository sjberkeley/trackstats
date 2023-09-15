import requests
from bs4 import BeautifulSoup
from datetime import datetime
import utils         # my utils

#
# main program
#
this_year = datetime.now().year
earliest_num_perfs = this_year
num_perfs = 10
field_event = True
gender = "men"
event = "400 metres"

#m_urls = {}
#w_urls = {}

m_urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
w_urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

if gender == "women":
    url = w_urls[event]
else:
    url = m_urls[event]

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Get the plain text representation of the HTML content
    plain_text = soup.get_text()
    
    # Split the text into lines
    lines = plain_text.splitlines()
    
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

                # the following lines are not necessary assuming the list is ordered by performance
                # 
                # check if this performance is better than one of the existing
                #if (field_event):
                #    worst = 1000000
                #else:
                #    worst = 0
                #worst_index = 0
                #for ii in range(0, num_perfs):    # index 0 is the year
                #    if worse_than(field_event, list[ii], worst):
                #        worst = list[ii]
                #        worst_index = ii

                #if worse_than(field_event, worst, performance):      #change for field events
                #    list[worst_index] = performance

    # Open csv file
    file_name = gender + event + ".csv"
    file1 = open(file_name,"w")
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
                    perf_sum += float(list[perf])
                perf_average = perf_sum / num_perfs
                array_1d.append(str(perf_average * 100.0))
                any_marks = True
        if (any_marks):
            array_2d.append(array_1d)

    # transpose and write to file
    # data is transposed for bar_chart_race versus Flourish
    num_rows = len(array_2d)
    num_cols = len(array_2d[0])

    for ii in range(num_cols):
        for jj in range(num_rows):
            if array_2d[jj][ii] != "0.0":
                file1.write(array_2d[jj][ii])
            if jj < num_rows-1:
                file1.write(",")
        file1.write("\n")
    file1.close

else:
    print("Error:", response.status_code)
