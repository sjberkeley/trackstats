import pandas as pd
import matplotlib.pyplot as plt
import bar_chart_race2 as bcrace
import numpy as np
import sys
import utils
import requests

def create_bar_chart_race(csv_filename, output_filename, field_event):
    # create bar chart race
    data = pd.read_csv(csv_filename, dtype=float)

    data.set_index('name', inplace=True)

    if (field_event == True):
        sortval = 'desc'
    else:
        sortval = 'asc'
    # Track events: sort='asc', modified bar_chart_race2
    # Field events: sort='desc, original bar_chart_race2
    bcrace.bar_chart_race(
        df=data,
        filename=output_filename,  # Output filename
        title='Average of top 10 marks',  # Chart title
        n_bars=20,
        period_fmt='{x:10.0f}',
        sort=sortval,
        steps_per_period=10,            # Number of steps per year
        period_length=500,              # Length of each year in milliseconds
    )

# main program
#gender, event, field_event = utils.get_args(sys.argv)
gender = "men"
event = "800 metres"
field_event = False

csv_filename = gender + event + ".csv"
output_filename = gender + event + ".mp4"
create_bar_chart_race(csv_filename, output_filename, field_event)


url = "https://example.com"  # Replace with the URL you want to refresh

# Send a GET request to the URL
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    print(f"Successfully refreshed {url}")
else:
    print(f"Failed to refresh {url} (Status Code: {response.status_code})")