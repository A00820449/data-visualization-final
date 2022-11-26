# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

from pandasql import sqldf 
pysqldf = lambda q: sqldf(q, globals())

app = Dash(__name__)

fb_df = pd.read_csv("clean.csv")

months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    
    html.Div([
        "Group by: ",
            dcc.Dropdown(id="slct_group",
                 options=["Month", "Weekday", "Hour"],
                 multi=False,
                 value="Month",
                 style={'width': "40%"}
                 ),

    ]),

    html.H2(["Total Interactions"]),

    dcc.Graph(
        id='main_graph',
        figure={}
    )
])

@app.callback(
    Output(component_id='main_graph', component_property='figure'),
    Input(component_id='slct_group', component_property='value')
)
def update_graph(option_slctd):
    print("Option selected:", option_slctd)

    ddf = pysqldf("""
    SELECT {0}, SUM(TotalInteract) as "TotalInteract"
    from fb_df
    GROUP BY {0}
    """.format(option_slctd))

    return px.bar(ddf, x=option_slctd, y="TotalInteract")

if __name__ == '__main__':
    app.run_server(debug=True)
