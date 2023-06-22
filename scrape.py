import requests
from bs4 import BeautifulSoup
from datetime import datetime

#
# find the earliest year in which a mark is posted
#
def find_earliest_year(lines, this_year):
    # find earliest year
    earliest = this_year
    processing = 0
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
        date = int(words[num_words-1][6:])
        if date < earliest:
            earliest = date

    return earliest

#
# check if one performance is worse than another
#
def worse_than(field_event, perf1, perf2):
    is_worse = True
    if (field_event):
        is_worse = (perf1 < perf2)
    else:
        is_worse = (perf1 > perf2)

    return is_worse

#
# Get the urls of the pages to scrape
#
def get_urls(links_url):
    response = requests.get(links_url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print("Error:", response.status_code)
        exit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract all the links on the page
    links = soup.find_all("a")
    urls = {}

    for link in links:
        event_name = link.text
        if (event_name == "Back to main page" or event_name == ""):
            continue
        if event_name not in urls.keys():
            urls[event_name] = "http://www.alltime-athletics.com/" + link.get("href")

    return urls

#
# extract the name, date and performance
#
def get_stats(words):
    perf = words[1]
    if not perf[-1].isnumeric():       # trailing A denotes altitude, y yards
        if not perf[-2].isnumeric():
            performance = float(perf[:-2])
        else:
            performance = float(perf[:-1])
    else:
        performance = float(perf)

    name = words[2] + " " + words[3]
    if not words[4].isupper() or len(words[4]) != 3:
        name += " " + words[4]
        if not words[5].isupper() or len(words[5]) != 3:
            name += " " + words[5]

    date = int(words[num_words-1][6:])
    return name, date, performance

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

m_urls = get_urls("http://www.alltime-athletics.com/men.htm")
w_urls = get_urls("http://www.alltime-athletics.com/women.htm")

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
    earliest = find_earliest_year(lines, this_year)

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
        name, date, performance = get_stats(words)

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
    header = "name"
    for year in range(earliest_num_perfs, this_year):
        header += ","
        header += str(year)
    file1.write(header)
    file1.write("\n")
    for name in athletes.keys():
        marks = name
        list_of_lists = athletes[name]
        any_marks = False
        for year in range(earliest_num_perfs, this_year):    
            list = list_of_lists[year-earliest]
            if len(list) < num_perfs:
                marks += ","
            else:
                perf_sum = 0
                for perf in range(0,num_perfs):
                    perf_sum += list[perf]
                perf_average = perf_sum / num_perfs
                marks += ","
                marks += str(perf_average)
                any_marks = True
        if (any_marks):
            file1.write(marks)
            file1.write("\n")
    file1.close

else:
    print("Error:", response.status_code)
