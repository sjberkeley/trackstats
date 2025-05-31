#
# miscellaneous utilities for content on visualtrackstats.com
#

import requests
from bs4 import BeautifulSoup
from datetime import datetime
#import re
#import sys
#import pandas as pd
import utils

# need to fix bug with Gabby Thomas 400m score (49.68) - 1217 when it should be 1218
class Alltime:
    #
    # Get the urls of the pages to scrape
    #
    def get_urls(self, links_url):
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
            if event_name == "60 metres":       # skip special events
                break
            if (event_name == "Back to main page" or event_name == "" or event_name == "Old specs"):
                continue
            if event_name not in urls.keys():
                urls[event_name] = "http://www.alltime-athletics.com/" + link.get("href")
    
        return urls

    def strip_preamble(self, line, processing):
        status = 2
        # Skip empty lines
        if not line.strip():
            status = 0
            words = []
        else:
            words = line.split()
            num_words = len(words)
            # check for done with outdoor list
            if (num_words < 8 and processing == 1):
                status = 1
            elif (num_words > 7 and words[0] == "1" and processing == 0):
                processing = 1
            elif (processing == 0):
                status = 0
            elif not words[0].isdigit():
                status = 1
    
        return status, words, processing
    
    #
    # extract the name, date and performance
    #
    def get_stats(self, words):
        num_words = len(words)
        perf = words[1]
        if not perf[-1].isnumeric():       # trailing A denotes altitude, y yards
            if not perf[-2].isnumeric():
                performance = perf[:-2]
            else:
                performance = perf[:-1]
        else:
            performance = perf  # float(perf)
    
        index = 2
        if utils.is_numeric(words[index]):       # wind reading for straightaway and runway
            index = index + 1
        name = words[index]
        index = index + 1
        for iter in range(5):
            nation = words[index]
            if words[index] != "BEl" and words[index] != "EX":      # typo on men marathon and men 20k walk
                wordlen = len(words[index])
                maybe_nation = ""
                if wordlen > 2:
                    maybe_nation = words[index][-3:wordlen]
                if maybe_nation.isupper():                          # last word of name runs into nation
                    if wordlen > 3:
                        name += " " + words[index][:-3]
                    nation = maybe_nation
                    break
                elif words[index].isupper() and wordlen == 3:       # nation already set
                    break
                else:                                               # another part of name
                    name += " " + words[index]
                index = index + 1
    
        index = index + 2
        position = "*"
        if utils.is_numeric(words[index][0]) or words[index] == "D" or words[index] == "q" or words[index] == "*":
            position = words[index]
            index = index + 1
    
        if index == num_words - 1:       # no city ?
            city = "unknown"
        else:
            city = words[index]
        if num_words > index + 2:
            index = index + 1
            city += " " + words[index]
            if num_words > index + 2:
                index = index + 1
                city += " " + words[index]
    
        comma_index = city.find(',')
        if comma_index != -1:
            city = city[0:comma_index] + city[comma_index+1:]
    
        date = words[num_words-1]
        if len(date) > 10:
            if date[10] == ">":       # Anna Cockrell in 400 hurdles
                date = words[num_words-1][0:10]
            else:
                date = words[num_words-1][-10:]
        if len(date) < 10:
            if date[1] == ".":
                date = "0" + date
            elif date[4] == ".":
                date = date[0:3] + "0" + date[3:9]
        year = int(date[6:10])
        month = int(date[3:5])
        if month < 1:
            month = 1
        if month > 12:
            month = 12
        day = int(date[0:2])
        if day > 31:
            day = 31
        this_date = datetime(year, month, day)
    
        return name, year, performance, nation, this_date, city, position, date

