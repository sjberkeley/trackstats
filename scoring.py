from curses import pair_number
import PyPDF2
from PyPDF2 import PdfReader

def create_handles(gender):
    file_handles = {}     # map
    sprint_hurdles = "110mH"
    multi = "Decathlon"
    if gender == "women":
        sprint_hurdles = "100mH"
        multi = "Heptathlon"

    for event_name in ("100m", "200m", "300m", "400m", "500m", sprint_hurdles, "400mH", "4x100m", "4x200m", "4x400m"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("600m", "800m", "1000m", "1500m", "Mile", "2000m"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("2000mSC", "3000m", "3000mSC", "2 Miles", "5000m", "10,000m"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("5km", "10km", "15km", "10 Miles", "20km"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("HM", "25km", "30km", "Marathon", "100km"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("3000mW", "5000mW", "10,000mW", "15,000mW"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("20,000mW", "30,000mW", "35,000mW", "50,000mW"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("3kmW", "5kmW", "10kmW", "15kmW", "20kmW", "30kmW", "35kmW", "50kmW"):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    for event_name in ("HJ", "PV", "LJ", "TJ", "SP", "DT", "HT", "JT", multi):
        file_handles[event_name] = open(event_name + "." + gender + ".scores", "w")
    return file_handles

def extract_text_from_pdf(file_path):
    men_handles = create_handles("men")
    women_handles = create_handles("women")

    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    first_column_is_points = True
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text = page.extract_text()
        lines = text.splitlines()
        if len(lines) != 2:
            event_handles = []    # list
            continue
        words = lines[0].split()
        if words[0][:3] == "MEN":
            men = True
        elif words[0][:5] == "WOMEN":
            men = False
            #break     # add women later
        else:
            continue 
        for line in lines:
            words = line.split()
            num_words = len(words)
            if num_words < 20:
                continue
            # process the header
            # assume that the first page of a new set of events has the points in the rightmost column
            first_column_is_points = False
            if words[1] == "Points":
                first_column_is_points = True
                skip_word = False
                col_shift = 0
                num_columns = 0
                for word_num in range(2, 20):
                    if skip_word:
                        skip_word = False
                        continue
                    word = words[word_num]
                    # the only event names consisting of two words are "2 Miles" and "10 Miles"
                    if (word == "2" or word == "10") and words[word_num + 1] == "Miles":
                        word = words[word_num] + " " + words[word_num + 1]
                        skip_word = True
                        num_columns = num_columns - 1
                        col_shift = col_shift + 1
                    if word.isdigit():           # it's a score
                        num_columns = num_columns + word_num - 1
                        break
                    else:
                        if men:
                            event_handles.append(men_handles[word])
                        else:
                            event_handles.append(women_handles[word])

            # process the rest of the page
            col_index = 0
            for word_num in range(num_columns + col_shift + 1, num_words):   # mystery number at the start
                if col_index == 0:
                    if first_column_is_points:
                        score = words[word_num]
                    else:
                        score = words[word_num + num_columns - 1]
                else:
                    word_index = word_num
                    if not first_column_is_points:
                        word_index = word_index - 1
                    if words[word_index] != "-":
                        event_handles[col_index - 1].write(words[word_index] + " " + str(score) + "\n")
                col_index += 1
                if col_index == num_columns:
                    col_index = 0

    return text

pdf_file = "WA_tables.pdf"
extracted_text = extract_text_from_pdf(pdf_file)

#            else:
#                first_column_is_points = False
#                for word_num in range(1, 20):
#                    word = words[word_num]
#                    if word == "Points":
#                        num_columns = word_num - col_decrement
#                        break
#                    else:
#                        # the only event names consisting of two words are "2 Miles" and "10 Miles"
#                        if (word == "2" or word == "10") and words[word_num + 1] == "Miles":
#                            word = words[word_num] + " " + words[word_num + 1]
#                            word_num = word_num + 1
#                            col_decrement = col_decrement + 1
#                        event_handles[word_num - 1] = file_handles[word]
