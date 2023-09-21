import pandas as pd
import matplotlib.pyplot as plt
import bar_chart_race2 as bcr
import numpy as np

# create bar chart race
data = pd.read_csv('men400 metres.csv') #, dtype=float)

data.set_index('name', inplace=True)

bcr.bar_chart_race(
    df=data,
    filename='men400.mp4',  # Output filename
    title='Average of top 10 marks',  # Chart title
    n_bars=20,
    sort='desc',
    #bar_label_format='{x:.3f}',
    #fig=fig,
    #figsize=(10,8),
    #label_bars=False,
    #precision=2,
    #period_fmt='%b %-d, %Y',
    steps_per_period=10,            # Number of steps per year
    period_length=500,              # Length of each year in milliseconds
)

