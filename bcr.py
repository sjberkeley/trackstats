import pandas as pd
#import matplotlib.pyplot as plt
import bar_chart_race2 as bcrace
#import numpy as np
import sys
import utils
import requests
import scrape
import boto3

def create_bar_chart_race(gender, event, field_event, num_bars, num_to_avg):
    csv_filename = gender + event + ".csv"
    output_filename = gender + event + ".mp4"

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
        title=gender + " " + event + ": average of top " + str(num_to_avg) + " marks",  # Chart title
        n_bars=num_bars,
        period_fmt='{x:10.0f}',
        sort=sortval,
        steps_per_period=10,            # Number of steps per year
        period_length=500,              # Length of each year in milliseconds
    )

# main program
def build_and_upload_bcr():
    gender, event, field_event = utils.get_args(sys.argv)
    #gender = "men"
    #event = "100 metres"
    #field_event = utils.is_field_event(event)
    num_bars = 20
    num_to_avg = 10

    scrape.build_csv(gender, event, num_to_avg)

    create_bar_chart_race(gender, event, field_event, num_bars, num_to_avg)

    # upload to s3
    file_name = gender + event + ".mp4"
    s3 = boto3.client('s3')

    bucket_name = 'trackstats-s3'
    object_key = file_name
    file_path = "./" + file_name

    s3.upload_file(file_path, bucket_name, object_key)


build_and_upload_bcr()

# url = "https://example.com"  # Replace with the URL you want to refresh
# 
# # Send a GET request to the URL
# response = requests.get(url)
# 
# # Check the response status code
# if response.status_code == 200:
#     print(f"Successfully refreshed {url}")
# else:
#     print(f"Failed to refresh {url} (Status Code: {response.status_code})")
