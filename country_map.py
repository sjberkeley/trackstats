#
# create spreadsheet for world map showing the number of world records set by athletes from each nation
#

from datetime import datetime
import utils         # my utils

#
# main program
#
#gender, event, field_event = utils.get_args(sys.argv)
def build_country_csv():
    gender = "women"
    #event = "800 metres"

    #build country code map
    start = False
    code_map = {}
    record_counts = {}
    lines = utils.get_lines_from_url("https://www.iban.com/country-codes")
    for line in lines:
        if line == "Afghanistan":
            start = True
            alpha_2_code = ""
        if start:
            if alpha_2_code != "":
                code_map[line] = alpha_2_code
                record_counts[alpha_2_code] = 0
                alpha_2_code = ""
            if len(line) == 2:
                alpha_2_code = line

    # odd ones not in the table. This does result in some duplicates but they don't matter
    code_map["RSA"] = "ZA"     
    record_counts["ZA"] = 0
    code_map["NGR"] = "NG"     
    record_counts["NG"] = 0
    code_map["POR"] = "PT"     
    record_counts["PT"] = 0
    code_map["NED"] = "NL"     
    record_counts["NL"] = 0
    code_map["ALG"] = "DZ"     
    record_counts["DZ"] = 0
    code_map["BUL"] = "BG"      
    record_counts["BG"] = 0
    code_map["CRO"] = "HR"      
    record_counts["HR"] = 0
    code_map["DEN"] = "DK"      
    record_counts["DK"] = 0
    code_map["FRG"] = "DE"      
    record_counts["DE"] = 0
    code_map["GDR"] = "DE"      
    record_counts["DE"] = 0
    code_map["GER"] = "DE"      
    record_counts["DE"] = 0
    code_map["GRE"] = "GR"      
    record_counts["GR"] = 0
    code_map["GUA"] = "GU"     
    record_counts["GU"] = 0
    code_map["TAN"] = "TZ"    
    record_counts["TZ"] = 0

    for gender in ("men", "women"):
        if gender == "men":
            urls = utils.get_urls("http://www.alltime-athletics.com/men.htm")
        else:
            urls = utils.get_urls("http://www.alltime-athletics.com/women.htm")
    
        for url in urls:
            if url == "4x100m relay" or url == "4x400m relay" or url == "mixed 4x400m relay": # or url == "Javelin throw" \
                #or url == "50 km race walk" or url == "half-marathon" or url == "20 km race walk" \
                #or url == "3000m steeplechase" or url == "Pole vault" or url == "Hammer throw" or url == "Triple jump":
                continue
            lines = utils.get_lines_from_url(urls[url])
            # process data
            processing = 0
            last_date = datetime.now()
            for line in lines:
                status, words, processing = utils.strip_preamble(line, processing)
                if status == 0:
                    continue
                elif status == 1:
                    break
    
                # extract performance, name and date (year)
                name, year, performance, nation, this_date, city, position, date = utils.get_stats(words)
                if this_date < last_date:
                    if not nation in code_map:
                        print("missing " + nation)
                        continue
                    alpha_2_code = code_map[nation]
                    record_counts[alpha_2_code] = record_counts[alpha_2_code] + 1
                    last_date = this_date

    # Open csv file
    file_name = "nation_count.csv"
    file1 = open(file_name,"w")
    # write header row
    header = "nation,number"
    file1.write(header + "\n")

    for alpha_3_code in code_map.keys():
        alpha_2_code = code_map[alpha_3_code]
        num_records = record_counts[alpha_2_code]
        if num_records > 0:
            row_str = alpha_2_code + "," + str(num_records)
            file1.write(row_str + "\n")
    
    file1.close


build_country_csv()

