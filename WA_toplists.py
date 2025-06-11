#
# Scraping lists from World Athletics site
#

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import utils

class WA_toplists:
    #
    # Get the urls of the pages to scrape
    #
    def get_urls(self, links_url):
        best = "?bestResultsOnly=true"
        page = "&page=2"

        urls = {}
        urls["100 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/100-metres/all/men/senior" #+ best
        urls["200 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/200-metres/all/men/senior" #+ best
        urls["400 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/400-metres/all/men/senior" #+ best

        return urls
    
    def get_lines_from_urls(self, url):
        all_lines = []
        page_num = 0
        num_pages = 1
        while page_num < num_pages:
            page_num = page_num + 1
            paged_url = url + "?page=" + str(page_num)
            lines = utils.get_lines_from_url(paged_url)
            #for ii in range(len(lines)):
            #    print(lines[ii])

            processing = 0
            num_lines = len(lines)
            line_num = 0
            while line_num < num_lines:
                if lines[line_num] == "                >>":
                    if lines[line_num-3] == "                >":
                        num_pages = int(lines[line_num-5])

                status, words, processing, line_num = self.strip_one_page_preamble(lines, line_num, processing)
                if status == 0:
                    continue
                elif status == 1:
                    all_lines.append(lines[line_num])
                    all_lines.append(lines[line_num])
                    all_lines.append(lines[line_num])
                    break

                all_lines.append(lines[line_num])

            #print("page ",page_num," of ",num_pages)
            if page_num == num_pages:
                break

        return all_lines
    #
    # strip preamble from the compiled multi-page WA list (it has already been stripped)
    #
    def strip_preamble(self, lines, index, processing):
        status = 2
        processing = 1
        words = lines[index].split()
        return status, words, processing, index
    #
    # extract the name, date and performance
    #
    def get_stats(self, words, lines, index):
        performance = lines[index+2].strip()
        if len(lines[index+5]) == 0:           # no wind, so one line is missing
            index = index - 1
        name = lines[index+9].strip()
        if len(lines[index+13]) == 0:           # no date of birth, so one line is missing
            index = index - 1
        nation = lines[index+17].strip()
        if len(lines[index+20]) == 0:           # no position, so one line is missing
            index = index - 1
            position = ""
        else:
            position = lines[index+20]
        city = lines[index+24].strip()
        date = lines[index+27].strip()
        year = int(date[7:11])
        month = utils.month_num(date[3:6])
        day = int(date[0:2])
        this_date = datetime(year, month, day)

        index = index + 35

        return name, year, performance, nation, this_date, city, position, date, index
    #
    # strip the preamble from a single page of WA performances
    #
    def strip_one_page_preamble(self, lines, index, processing):
        line = lines[index]
        status = 2     # process the line
        if line == "                                            Results Score":
            index = index + 7
            status = 2
            words = line        # not used in WA_toplists derived class
            processing = 1
        elif processing == 0:
            index = index + 1
            status = 0          # skip
            words = []
        else:
            index = index + 1
            if len(line.strip()) == 0 and len(lines[index].strip()) == 0 and len(lines[index+1].strip()) == 0 and \
                len(lines[index+2].strip()) == 0 and len(lines[index+3].strip()) == 0 and \
                len(lines[index+4].strip()) == 0 and len(lines[index+5].strip()) == 0:
                status = 1      # quit
                processing = 0
            words = []
    
        return status, words, processing, index
    