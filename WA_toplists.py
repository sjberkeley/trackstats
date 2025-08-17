#
# Scraping lists from World Athletics site
#

from datetime import datetime
import utils
from Alltime import Alltime

class WA_toplists(Alltime):
    #
    # Get the urls of the pages to scrape
    #
    def get_urls(self, gender, bestOnly):
        root = "https://worldathletics.org/records/all-time-toplists/"
        if bestOnly:
            best = "?bestResultsOnly=true&ageCategory=senior"
        else:
            best = "?bestResultsOnly=false"

        age = "/senior"                       # senior, u20 or u18

        urls = {}
        if gender == "men":
            urls["100 metres"] = root + "sprints/100-metres/all/men" + age + best
            urls["200 metres"] = root + "sprints/200-metres/all/men" + age + best
            urls["400 metres"] = root + "sprints/400-metres/all/men" + age + best
            urls["800 metres"] = root + "middlelong/800-metres/all/men" + age + best
            urls["1500 metres"] = root + "middlelong/1500-metres/all/men" + age + best
            urls["1 Mile"] = root + "middlelong/one-mile/all/men" + age + best
            urls["3000 metres"] = root + "middlelong/3000-metres/all/men" + age + best
            urls["5000 metres"] = root + "middlelong/5000-metres/all/men" + age + best
            urls["10000 metres"] = root + "middlelong/10000-metres/all/men" + age + best
            urls["half-marathon"] = root + "road-running/half-marathon/all/men" + age + best
            urls["marathon"] = root + "road-running/marathon/all/men" + age + best
            urls["3000m steeplechase"] = root + "middlelong/3000-metres-steeplechase/all/men" + age + best
            urls["110m hurdles"] = root + "hurdles/110-metres-hurdles/all/men" + age + best
            urls["400m hurdles"] = root + "hurdles/400-metres-hurdles/all/men" + age + best
            urls["High jump"] = root + "jumps/high-jump/all/men" + age + best
            urls["Pole vault"] = root + "jumps/pole-vault/all/men" + age + best
            urls["Long jump"] = root + "jumps/long-jump/all/men" + age + best
            urls["Triple jump"] = root + "jumps/triple-jump/all/men" + age + best
            urls["Shot put"] = root + "throws/shot-put/all/men" + age + best
            urls["Discus throw"] = root + "throws/discus-throw/all/men" + age + best
            urls["Hammer throw"] = root + "throws/hammer-throw/all/men" + age + best
            urls["Javelin throw"] = root + "throws/javelin-throw/all/men" + age + best
            urls["Decathlon"] = root + "combined-events/decathlon/all/men" + age + best
            urls["20 km race walk"] = root + "race-walks/20-kilometres-race-walk/all/men" + age + best
            urls["50 km race walk"] = root + "race-walks/50-kilometres-race-walk/all/men" + age + best
        else:
            urls["100 metres"] = root + "sprints/100-metres/all/women" + age + best
            urls["200 metres"] = root + "sprints/200-metres/all/women" + age + best
            urls["400 metres"] = root + "sprints/400-metres/all/women" + age + best
            urls["800 metres"] = root + "middlelong/800-metres/all/women" + age + best
            urls["1500 metres"] = root + "middlelong/1500-metres/all/women" + age + best
            urls["1 Mile"] = root + "middlelong/one-mile/all/women" + age + best
            urls["3000 metres"] = root + "middlelong/3000-metres/all/women" + age + best
            urls["5000 metres"] = root + "middlelong/5000-metres/all/women" + age + best
            urls["10000 metres"] = root + "middlelong/10000-metres/all/women" + age + best
            urls["half-marathon"] = root + "road-running/half-marathon/all/women" + age + best
            urls["marathon"] = root + "road-running/marathon/all/women" + age + best
            urls["3000m steeplechase"] = root + "middlelong/3000-metres-steeplechase/all/women" + age + best
            urls["100m hurdles"] = root + "hurdles/100-metres-hurdles/all/women" + age + best
            urls["400m hurdles"] = root + "hurdles/400-metres-hurdles/all/women" + age + best
            urls["High jump"] = root + "jumps/high-jump/all/women" + age + best
            urls["Pole vault"] = root + "jumps/pole-vault/all/women" + age + best
            urls["Long jump"] = root + "jumps/long-jump/all/women" + age + best
            urls["Triple jump"] = root + "jumps/triple-jump/all/women" + age + best
            urls["Shot put"] = root + "throws/shot-put/all/women" + age + best
            urls["Discus throw"] = root + "throws/discus-throw/all/women" + age + best
            urls["Hammer throw"] = root + "throws/hammer-throw/all/women" + age + best
            urls["Javelin throw"] = root + "throws/javelin-throw/all/women" + age + best
            urls["Heptathlon"] = root + "combined-events/heptathlon/all/women" + age + best
            urls["20 km race walk"] = root + "race-walks/20-kilometres-race-walk/all/women" + age + best
            urls["50 km race walk"] = root + "race-walks/50-kilometres-race-walk/all/women" + age + best

        return urls
    
    def get_lines_from_urls(self, url):
        all_lines = []
        page_num = 0
        num_pages = 1
        while page_num < num_pages:
            page_num = page_num + 1
            paged_url = url + "&page=" + str(page_num)
            #paged_url = "https://mastersrankings.com/rankings/"
            lines = utils.get_lines_from_url(paged_url)

            processing = 0
            num_lines = len(lines)
            line_num = 0

            #for line in range(num_lines):
            #    print(lines[line])

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

            print("page ",page_num," of ",num_pages)
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
        if len(lines[index+5]) == 0:            # no wind, so one line is missing
            index = index - 1
        name = lines[index+9].strip()
        if len(lines[index+13]) == 0:           # no date of birth, so one line is missing
            index = index - 1
            date = "05 JAN 1961"
        else:
            date = lines[index+13].strip()
        if len(date) == 11:
            year = int(date[7:11])
            month = utils.month_num(date[3:6])
            day = int(date[0:2])
            dob = datetime(year, month, day)
        elif len(date) == 4:
            dob = datetime(int(date), 1, 5)
        else:
            dob = datetime(1961, 1, 5)
        nation = lines[index+17].strip()
        if len(lines[index+20]) == 0:           # no position, so one line is missing
            index = index - 1
            position = ""
        else:
            position = lines[index+20].strip()
        city = lines[index+24].strip()

        date = lines[index+27].strip()
        year = int(date[7:11])
        month = utils.month_num(date[3:6])
        day = int(date[0:2])
        this_date = datetime(year, month, day)

        # transform date into alltime-athletics format
        day_zero = ""
        if day < 10:
            day_zero = "0"
        month_zero = ""
        if month < 10:
            month_zero = "0"
        date = day_zero + str(day) + "." + month_zero + str(month) + "." + str(year)

        if index + 35 < len(lines) and len(lines[index+35].strip()) > 40:   # Decathlon/Heptathlon score
            index = index + 4
        index = index + 35
    
        return name, year, performance, nation, this_date, city, position, date, dob, index
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
            six_blanks = len(lines[index].strip()) == 0 and len(lines[index+1].strip()) == 0 and \
                len(lines[index+2].strip()) == 0 and len(lines[index+3].strip()) == 0 and \
                len(lines[index+4].strip()) == 0 and len(lines[index+5].strip()) == 0
            # Decathlon/Heptathlon lists have an additional field listing the individual event marks
            if (len(line.strip()) == 0 or len(line.strip()) > 40) and six_blanks:
                status = 1      # quit
                processing = 0
            words = []
    
        return status, words, processing, index

