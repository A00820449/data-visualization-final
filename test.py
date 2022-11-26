import matplotlib.pyplot as plt
from matplotlib import cycler
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from pandasql import sqldf 
pysqldf = lambda q: sqldf(q, globals())



colors = cycler('color',
                ['#E8570E', '#FF8730', '#E06E48', '#FFA96B', '#E89D80', '#FACAA5', '#E8C6B7'
                 ]) 
plt.rc('axes', facecolor='#F7F6F6', edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#E6E6E6')
plt.rc('lines', linewidth=1)
plt.rcParams["figure.figsize"] = (10,8)

plt.bar([1,2,3,4,5],[1,2,3,4,5])

#plt.show()

fb_df = pd.read_csv("clean.csv")

print(fb_df["Month"])
print(fb_df["TotalInteract"])

fig = px.bar(fb_df, y="TotalInteract")
fig.show()