import pandas as pd
import bar_chart_race as bcr

# create bar chart race

#data = pd.DataFrame({
#    'Year': [2000, 2001, 2002, 2003],
#    'Category A': [10, 15, 20, 25],
#    'Category B': [15, 10, 5, 30],
#    'Category C': [5, 30, 25, 10]
#})

data = pd.read_csv('men400 metres.csv')

data.set_index('name', inplace=True)
# Sort the data in descending order
#sorted_data = data.sort_values(by=data.columns, ascending=False)

bcr.bar_chart_race(
    df=data,
    filename='men400.mp4',  # Output filename
    title='Mens 400m average of top 10 marks',  # Chart title
    #n_bars=20,
    sort='asc',
    #precision=2,
    #period_fmt='%Y',
    steps_per_period=10,            # Number of steps per year
    period_length=500,              # Length of each year in milliseconds
)

# file_name = "covid.csv"
# data = bcr.load_dataset('covid')
# bcr.bar_chart_race(df=data, filename="output.mp4")


