#
# rank Raheny Shamrock club records by WA scoring points
#

from datetime import datetime
import utils         # my utils
import pandas as pd
import utils

#
# main program
#

event_name_map = {}

#gender, event, field_event = utils.get_args(sys.argv)
this_year = datetime.now().year

earliest_date = this_year
total_scores = {}

sorted_file_name = "raheny.sorted"
file2 = open(sorted_file_name,"w")

for gender in ("men", "women"):
    score_maps = {}
    utils.init_score_maps(event_name_map, score_maps)

    record_file_name = "raheny." + gender
    file1 = open(record_file_name,"r")
    text = file1.read()
    lines = text.splitlines()
    for line in lines:
        words = line.split()
        index = 0
        if words[index] == "Decathlon" or words[index] == "marathon":
            event = words[index]
            index = 1
        else:
            event = words[0] + " " + words[1]
            index = 2

        performance = words[index]
        name = words[index+1] + " " + words[index+2]
        score = utils.get_WA_score(gender, event, performance, event_name_map, score_maps)
        if int(score) < 1000:
            file2.write(" ")
        file2.write(score + " " + gender + " " + event + " " + performance + " " + name + "\n")
    file1.close

file2.close
