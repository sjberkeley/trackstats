import pandas as pd
import bar_chart_race as bcr

# create bar chart race
file_name = "covid.csv"
data = bcr.load_dataset('covid')
bcr.bar_chart_race(df=data, filename="output.mp4")


