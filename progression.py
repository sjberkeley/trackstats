#
# spreadsheet to create graph of world record progressions in all events, comparing relative advances
#

from datetime import datetime
import utils         # my utils

#
# main program
#
#gender, event, field_event = utils.get_args(sys.argv)
def build_record_csv():
    gender = "men"
    #event = "800 metres"

    this_year = datetime.now().year

    if gender == "men":
        urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
    else:
        urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")

    latest_earliest_date = 0
    events = {}
    for url in urls:
        if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay" or url == "Javelin throw" \
            or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk" \
            or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
            continue
        lines = utils.get_lines_from_url(urls[url])
        # process data
        processing = 0
        last_date = 0
        records = []
        for line in lines:
            status, words, processing = utils.strip_preamble(line, processing)
            if status == 0:
                continue
            elif status == 1:
                break

            # extract performance, name and date (year)
            name, date, performance, nation, this_date, city, position, full_date = utils.get_stats(words)
            if last_date == 0:
                last_date = this_year
                records.append(performance)
            if date < last_date:
                for year in range(last_date, date, -1):
                    records.append(performance)
                last_date = date

        events[url] = records
        if last_date > latest_earliest_date:
            latest_earliest_date = last_date

    num_rows = this_year - latest_earliest_date
    # Open csv file
    file_name = "record_progression.csv"
    file1 = open(file_name,"w")
    # write header row
    header = "year"
    for event in events.keys():
        header += "," + event
    file1.write(header + "\n")

    year = latest_earliest_date
    for row in range(num_rows+1):
        row_str = str(year)
        for event in events.keys():
            field_event = utils.is_field_event(event)
            records = events[event]
            record = records[num_rows - row]
            start_mark = records[this_year - latest_earliest_date]
            record_seconds, hundredths = utils.hms_to_seconds(record)
            start_seconds, hundredths = utils.hms_to_seconds(start_mark)
            mark = float(record_seconds) / float(start_seconds)
            if not field_event:
                mark = 1.0 / mark
            mark = mark ** 10
            row_str += "," + str(mark)
        year += 1
        file1.write(row_str + "\n")
    
    file1.close


build_record_csv()
#time.sleep(10)

