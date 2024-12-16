#
# generate the bar chart races showing 10-performance averages for all events
#

import pandas as pd
#import matplotlib.pyplot as plt
import bar_chart_race2 as bcrace
#import numpy as np
import sys
import utils
import requests
import scrape
import boto3
from datetime import datetime

def create_bar_chart_race(gender, event, field_event, num_bars, num_to_avg):
    csv_filename = gender + event + ".csv"
    output_filename = gender + event + ".mp4"

    # create bar chart race
    data = pd.read_csv(csv_filename, dtype=float)

    data.set_index('name', inplace=True)

    if (field_event == True):
        sortval = 'desc_f'
    else:
        sortval = 'desc'

    bcrace.bar_chart_race(
        df=data,
        filename=output_filename,  # Output filename
        title=gender + " " + event + ": average of top " + str(num_to_avg) + " performances (last updated " + str(datetime.now().date()) + ")",  # Chart title
        n_bars=num_bars,
        period_fmt='{x:4.0f}',
        sort=sortval,
        figsize=(7.5, 5),               # was (6, 3.5)
        steps_per_period=30,            # Number of steps per year
        period_length=1500,             # Length of each year in milliseconds
        period_label={'x': .8, 'y': .8, 'ha': 'right', 'va': 'center', 'size': 32},
        #scale="log",
    )

# main program
def build_and_upload_bcr(gender, event):
    #gender, event, field_event = utils.get_args(sys.argv)
    #gender = "men"
    #event = "100 metres"
    field_event = utils.is_field_event(event)
    num_bars = 20
    num_to_avg = 10

    scrape.build_csv(gender, event, num_to_avg)

    create_bar_chart_race(gender, event, field_event, num_bars, num_to_avg)

    # upload to s3
    #file_name = gender + event + ".mp4"
    #s3 = boto3.client('s3')

    #bucket_name = 'trackstats-s3'
    #object_key = file_name
    #file_path = "./" + file_name

    #s3.upload_file(file_path, bucket_name, object_key)


#build_and_upload_bcr("men", "100 metres")
#build_and_upload_bcr("men", "200 metres")
#build_and_upload_bcr("men", "400 metres")
#build_and_upload_bcr("men", "800 metres")
#build_and_upload_bcr("men", "1500 metres")
#build_and_upload_bcr("men", "3000 metres")
#build_and_upload_bcr("men", "3000m steeplechase")
#build_and_upload_bcr("men", "5000 metres")
#build_and_upload_bcr("men", "10000 metres")
#build_and_upload_bcr("men", "marathon")
#build_and_upload_bcr("men", "110m hurdles")
#build_and_upload_bcr("men", "400m hurdles")
#build_and_upload_bcr("men", "High jump")
#build_and_upload_bcr("men", "Long jump")
#build_and_upload_bcr("men", "Triple jump")
#build_and_upload_bcr("men", "Pole vault")
#build_and_upload_bcr("men", "Shot put")
#build_and_upload_bcr("men", "Discus throw")
#build_and_upload_bcr("men", "Javelin throw")
#build_and_upload_bcr("men", "Hammer throw")
build_and_upload_bcr("men", "Decathlon")
#
#build_and_upload_bcr("women", "100 metres")
#build_and_upload_bcr("women", "200 metres")
#build_and_upload_bcr("women", "400 metres")
#build_and_upload_bcr("women", "800 metres")
#build_and_upload_bcr("women", "1500 metres")
#build_and_upload_bcr("women", "3000 metres")
#build_and_upload_bcr("women", "3000m steeplechase")
#build_and_upload_bcr("women", "5000 metres")
#build_and_upload_bcr("women", "10000 metres")
#build_and_upload_bcr("women", "marathon")
#build_and_upload_bcr("women", "100m hurdles")
#build_and_upload_bcr("women", "400m hurdles")
#build_and_upload_bcr("women", "High jump")
#build_and_upload_bcr("women", "Long jump")
#build_and_upload_bcr("women", "Triple jump")
#build_and_upload_bcr("women", "Pole vault")
#build_and_upload_bcr("women", "Shot put")
#build_and_upload_bcr("women", "Discus throw")
#build_and_upload_bcr("women", "Javelin throw")
#build_and_upload_bcr("women", "Hammer throw")
#build_and_upload_bcr("women", "Heptathlon")

# url = "https://example.com"  # Replace with the URL you want to refresh
 
# # Send a GET request to the URL
# response = requests.get(url)
# 
# # Check the response status code
# if response.status_code == 200:
#     print(f"Successfully refreshed {url}")
# else:
#     print(f"Failed to refresh {url} (Status Code: {response.status_code})")
