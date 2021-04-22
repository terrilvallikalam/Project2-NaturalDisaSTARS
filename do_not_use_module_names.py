import os
import csv
csvpath = os.path.join('Resources', 'tornado_clean.csv')

with open(csvpath) as csvfile:

     # CSV reader specifies delimiter and variable that holds contents
     csvreader = csv.reader(csvfile, delimiter=',')

     print(csvreader)

     # Read the header row first (skip this step if there is now header)
     csv_header = next(csvreader)
     print(f"CSV Header: {csv_header}")

      # Read each row of data after the header
     for row in csvreader:
         print(row)


import plotly.graph_objects as go
import numpy as np

state = []
year = []
with open(csvpath, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        # Add title
        state.append(row[3])
        year.append(row[1])
x = state
y = year

fig = go.Figure(go.Histogram2d(x=x, y=y, histnorm='probability',
         autobinx=False,
         xbins=dict(start=0, end=53, size=0.1),
         autobiny=False,
         ybins=dict(start=0, end=69, size=0.1),
         colorscale=[[0, 'rgb(12,51,131)'], [0.25, 'rgb(10,136,186)'], [0.5, 'rgb(242,211,56)'], [0.75, 'rgb(242,143,56)'], [1, 'rgb(217,30,30)']]
     ))
fig.show()
# need to figure out how to change colorscale and reorder y