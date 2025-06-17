#
# Scraping lists from World Athletics site
#

from datetime import datetime
import utils

class WA_toplists:
    #
    # Get the urls of the pages to scrape
    #
    def get_urls(self, gender, bestOnly):
        if bestOnly:
            best = "?bestResultsOnly=true"
        else:
            best = "?bestResultsOnly=false"

        urls = {}
        if gender == "men":
            urls["100 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/100-metres/all/men/senior" + best
            urls["200 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/200-metres/all/men/senior" + best
            urls["400 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/400-metres/all/men/senior" + best
            urls["800 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/800-metres/all/men/senior" + best
            urls["1500 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/1500-metres/all/men/senior" + best
            urls["1 Mile"] = "https://worldathletics.org/records/all-time-toplists/middlelong/one-mile/all/men/senior" + best
            urls["3000 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/3000-metres/all/men/senior" + best
            urls["5000 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/5000-metres/all/men/senior" + best
            urls["10000 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/10000-metres/all/men/senior" + best
            urls["half-marathon"] = "https://worldathletics.org/records/all-time-toplists/road-running/half-marathon/all/men/senior" + best
            urls["marathon"] = "https://worldathletics.org/records/all-time-toplists/road-running/marathon/all/men/senior" + best
            urls["3000m steeplechase"] = "https://worldathletics.org/records/all-time-toplists/middlelong/3000-metres-steeplechase/all/men/senior" + best
            urls["110m hurdles"] = "https://worldathletics.org/records/all-time-toplists/hurdles/110-metres-hurdles/all/men/senior" + best
            urls["400m hurdles"] = "https://worldathletics.org/records/all-time-toplists/hurdles/400-metres-hurdles/all/men/senior" + best
            urls["High jump"] = "https://worldathletics.org/records/all-time-toplists/jumps/high-jump/all/men/senior" + best
            urls["Pole vault"] = "https://worldathletics.org/records/all-time-toplists/jumps/pole-vault/all/men/senior" + best
            urls["Long jump"] = "https://worldathletics.org/records/all-time-toplists/jumps/long-jump/all/men/senior" + best
            urls["Triple jump"] = "https://worldathletics.org/records/all-time-toplists/jumps/triple-jump/all/men/senior" + best
            urls["Shot put"] = "https://worldathletics.org/records/all-time-toplists/throws/shot-put/all/men/senior" + best
            urls["Discus throw"] = "https://worldathletics.org/records/all-time-toplists/throws/discus-throw/all/men/senior" + best
            urls["Hammer throw"] = "https://worldathletics.org/records/all-time-toplists/throws/hammer-throw/all/men/senior" + best
            urls["Javelin throw"] = "https://worldathletics.org/records/all-time-toplists/throws/javelin-throw/all/men/senior" + best
            urls["Decathlon"] = "https://worldathletics.org/records/all-time-toplists/combined-events/decathlon/all/men/senior" + best
            urls["20 km race walk"] = "https://worldathletics.org/records/all-time-toplists/race-walks/20-kilometres-race-walk/all/men/senior" + best
            urls["50 km race walk"] = "https://worldathletics.org/records/all-time-toplists/race-walks/50-kilometres-race-walk/all/men/senior" + best
        else:
            urls["100 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/100-metres/all/women/senior" + best
            urls["200 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/200-metres/all/women/senior" + best
            urls["400 metres"] = "https://worldathletics.org/records/all-time-toplists/sprints/400-metres/all/women/senior" + best
            urls["800 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/800-metres/all/women/senior" + best
            urls["1500 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/1500-metres/all/women/senior" + best
            urls["1 Mile"] = "https://worldathletics.org/records/all-time-toplists/middlelong/one-mile/all/women/senior" + best
            urls["3000 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/3000-metres/all/women/senior" + best
            urls["5000 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/5000-metres/all/women/senior" + best
            urls["10000 metres"] = "https://worldathletics.org/records/all-time-toplists/middlelong/10000-metres/all/women/senior" + best
            urls["half-marathon"] = "https://worldathletics.org/records/all-time-toplists/road-running/half-marathon/all/women/senior" + best
            urls["marathon"] = "https://worldathletics.org/records/all-time-toplists/road-running/marathon/all/women/senior" + best
            urls["3000m steeplechase"] = "https://worldathletics.org/records/all-time-toplists/middlelong/3000-metres-steeplechase/all/women/senior" + best
            urls["100m hurdles"] = "https://worldathletics.org/records/all-time-toplists/hurdles/100-metres-hurdles/all/women/senior" + best
            urls["400m hurdles"] = "https://worldathletics.org/records/all-time-toplists/hurdles/400-metres-hurdles/all/women/senior" + best
            urls["High jump"] = "https://worldathletics.org/records/all-time-toplists/jumps/high-jump/all/women/senior" + best
            urls["Pole vault"] = "https://worldathletics.org/records/all-time-toplists/jumps/pole-vault/all/women/senior" + best
            urls["Long jump"] = "https://worldathletics.org/records/all-time-toplists/jumps/long-jump/all/women/senior" + best
            urls["Triple jump"] = "https://worldathletics.org/records/all-time-toplists/jumps/triple-jump/all/women/senior" + best
            urls["Shot put"] = "https://worldathletics.org/records/all-time-toplists/throws/shot-put/all/women/senior" + best
            urls["Discus throw"] = "https://worldathletics.org/records/all-time-toplists/throws/discus-throw/all/women/senior" + best
            urls["Hammer throw"] = "https://worldathletics.org/records/all-time-toplists/throws/hammer-throw/all/women/senior" + best
            urls["Javelin throw"] = "https://worldathletics.org/records/all-time-toplists/throws/javelin-throw/all/women/senior" + best
            urls["Heptathlon"] = "https://worldathletics.org/records/all-time-toplists/combined-events/heptathlon/all/women/senior" + best
            urls["20 km race walk"] = "https://worldathletics.org/records/all-time-toplists/race-walks/20-kilometres-race-walk/all/women/senior" + best
            urls["50 km race walk"] = "https://worldathletics.org/records/all-time-toplists/race-walks/50-kilometres-race-walk/all/women/senior" + best

        return urls
    
    def get_lines_from_urls(self, url):
        all_lines = []
        page_num = 0
        num_pages = 1
        while page_num < num_pages:
            page_num = page_num + 1
            paged_url = url + "&page=" + str(page_num)
            lines = utils.get_lines_from_url(paged_url)

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
        if index + 35 < len(lines) and len(lines[index+35].strip()) > 40:   # Decathlon/Heptathlon score
            index = index + 4
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
            six_blanks = len(lines[index].strip()) == 0 and len(lines[index+1].strip()) == 0 and \
                len(lines[index+2].strip()) == 0 and len(lines[index+3].strip()) == 0 and \
                len(lines[index+4].strip()) == 0 and len(lines[index+5].strip()) == 0
            # Decathlon/Heptathlon lists have an additional field listing the individual event marks
            if (len(line.strip()) == 0 or len(line.strip()) > 40) and six_blanks:
                status = 1      # quit
                processing = 0
            words = []
    
        return status, words, processing, index

