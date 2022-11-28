# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

from pandasql import sqldf 
pysqldf = lambda q: sqldf(q, globals())

app = Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("clean.csv")

months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
colors = ['#E8570E', '#FF8730', '#E06E48', '#FFA96B', '#E89D80', '#FACAA5', '#E8C6B7']


### Ana Paula ###

ydf1 = df.groupby(['Paid']).mean()
ydf1=ydf1.reset_index()
ydf1[['Paid','Reach','EngagedUsers']]

ana_fig1 =  px.pie(ydf1, names='Paid', values='EngagedUsers', hole=0.5, color_discrete_sequence=colors)

data0 = go.Bar(
    x = ydf1["Paid"],
    y = ydf1["EngagedUsers"],
    name = 'EngagedUsers',
    textposition = 'outside',
)
data1 = go.Bar(
    x = ydf1["Paid"],
    y = ydf1["Reach"],
    name = 'Reach',
    textposition = 'outside',
    
)

data = [data0, data1]

layout = go.Layout(title = 'Publicidad pagada', barmode="stack", colorway=(colors))

ana_fig2 = go.Figure(data = data, layout = layout)

ana_fig2 = ana_fig2.update_xaxes(fixedrange=True, gridcolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.2)")
ana_fig2 = ana_fig2.update_yaxes(fixedrange=True, gridcolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.2)")
ana_fig2 = ana_fig2.update_layout({"plot_bgcolor": "#F7F6F6"})

#Aquí se muestran el porcentaje de los usuarios que han dado click del total de alcance

adf2 = df.groupby(['Type', 'Category']).mean()
adf2=adf2.reset_index()
adf2['EngagedUsers%']= (adf2['EngagedUsers']/adf2['Reach'])*100
adf2.sort_values(by=['EngagedUsers%'], inplace = True, ascending = False)
adf2[['Type','Category','EngagedUsers%']]

#En esta tabla se muestra que la mayorías de los clicks son realizados por los followers y mayores que usuarios 
#nuevos usuarios que han dado click. 
adf2['EngagedNew']= adf2['EngagedUsers']-adf2['EngagedFollowers']
adf2['EngagedNew%'] = (adf2['EngagedNew']/adf2['EngagedUsers'])*100
adf2['EngagedFollowers%'] = (adf2['EngagedFollowers']/adf2['EngagedUsers'])*100
adf2.sort_values(by=['EngagedFollowers'], inplace = True, ascending = False)
adf3 = adf2.groupby(['Type', 'Category']).sum()
adf3=adf3.reset_index()

#Creo una nueva columna para saber cuántos usuarios que no han dado like a la página dan click a cualquier cosa del 
#post
adf3[['Type','Category','EngagedNew%','EngagedFollowers%']]

#Esta tabla nos ayuda a identificar qué tipo de categoría de promocionar un producto, genera más interacción del
#usuario en el post
adf4 = adf2.groupby(['Type']).sum()
adf4=adf4.reset_index()
adf4.sort_values(by=['EngagedUsers'], inplace = True, ascending = False)
adf4[['Type','EngagedUsers']]

ana_fig3 = px.pie(adf4, names='Type', values='EngagedUsers', color_discrete_sequence=colors)

ana_tab1 = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dcc.Graph(figure=ana_fig1),
        ]
    )
)

ana_tab2 = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dcc.Graph(figure=ana_fig2),
        ]
    )
)

ana_tab3 = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 3!", className="card-text"),
            dcc.Graph(figure=ana_fig3),
        ]
    )
)

ana_tabs = dbc.Tabs(
    [
        dbc.Tab(ana_tab1, label="Tab 1"),
        dbc.Tab(ana_tab2, label="Tab 2"),
        dbc.Tab(ana_tab3, label="Tab 3"),
    ]
)

###  Ana Pula Fin  ###

### Yuyu ###

#En esta tabla se muestra la diferencia de alcance de pagar o no en la plataforma de facebook
ydf1 = df.groupby(['Paid']).mean()
ydf1=ydf1.reset_index()
ydf1[['Paid','Reach','EngagedUsers']]

#Aquí se muestran el porcentaje de los usuarios que han dado click del total de alcance

ydf2 = df.groupby(['Type', 'Category']).mean()
ydf2=ydf2.reset_index()
ydf2['EngagedUsers%']= (ydf2['EngagedUsers']/ydf2['Reach'])*100
ydf2.sort_values(by=['EngagedUsers%'], inplace = True, ascending = False)
ydf2[['Type','Category','EngagedUsers%']]

#En esta tabla se muestra que la mayorías de los clicks son realizados por los followers y mayores que usuarios 
#nuevos usuarios que han dado click. 
ydf2['EngagedNew']= ydf2['EngagedUsers']-ydf2['EngagedFollowers']
ydf2['EngagedNew%'] = (ydf2['EngagedNew']/ydf2['EngagedUsers'])*100
ydf2['EngagedFollowers%'] = (ydf2['EngagedFollowers']/ydf2['EngagedUsers'])*100
ydf2.sort_values(by=['EngagedFollowers'], inplace = True, ascending = False)
ydf3 = ydf2.groupby(['Type', 'Category']).sum()
ydf3=ydf3.reset_index()
#Creo una nueva columna para saber cuántos usuarios que no han dado like a la página dan click a cualquier cosa del 
#post
ydf3[['Type','Category','EngagedNew%','EngagedFollowers%']]

#Esta tabla nos ayuda a identificar qué tipo de categoría de promocionar un producto, genera más interacción del
#usuario en el post
ydf4 = ydf2.groupby(['Type']).sum()
ydf4=ydf4.reset_index()
ydf4.sort_values(by=['EngagedUsers'], inplace = True, ascending = False)
ydf4[['Type','EngagedUsers']]

#Mientras las impresiones son mayores, el porcentaje de clicks es mayor?
ydf2.sort_values(by=['Impressions'], inplace = True, ascending = False)
ydf2[['Type','Category','Impressions','EngagedUsers%']]

yfig = px.sunburst(ydf2, path=["Category", "Type"], values="Impressions", color_discrete_sequence=colors)
yfig = yfig.update_traces(textinfo="label+percent parent")

print(ydf2["Category"])

ygraph = dcc.Graph(figure=yfig)

### Yuyu Fin ##

graph_1 = html.Div([
    html.H2(["Interactions"]),

    html.Div(className="dropdowns" , children=[
        html.Div([
            "Group by: ",
            dcc.Dropdown(id="slct_group",
                 options=["Month", "Weekday", "Hour"],
                 multi=False,
                 value="Month",
                 className="dropdown",
                 clearable=False
                 #,style={'width': "min(400px, 90vw)"}
                 ),
            ]),

        html.Div([
            "Select: ",
            dcc.Dropdown(id="slct_unit",
                 options=[{"label": "Total", "value": "TotalInteract"}, {"label": "Likes", "value": "like"}, {"label": "Shares", "value": "share"}, {"label": "Comments", "value": "comment"}],
                 multi=False,
                 value="TotalInteract",
                 className="dropdown",
                 clearable=False
                 #,style={'width': "min(400px, 90vw)"}
                 ),
        ])

    ]),

    dcc.Graph(
        id='main_graph',
        figure={},
    ),
])

graph_2 = html.Div([
    html.H2(["Followers"]),

    html.Div(className="dropdowns" , children=[
        html.Div([
            "Group by: ",
            dcc.Dropdown(id="slct_group-2",
                 options=["Month", "Weekday", "Hour"],
                 multi=False,
                 value="Month",
                 className="dropdown",
                 clearable=False
                 #,style={'width': "min(400px, 90vw)"}
                 ),
            ]),

    ]),

    dcc.Graph(
        id='follower_graph',
        figure={},
    ),
])

graph_tabs = dbc.Tabs(
    [
        dbc.Tab(graph_1, label="Tab 1"),
        dbc.Tab(graph_2, label="Tab 2"),
    ]
)

logo = html.Img(src=app.get_asset_url("img/logo.jpg"), className="logo")

app.layout = html.Div(className="container", children=[
    html.H1(className="title",children=[logo, 'Final Project']),
    
    graph_tabs,

    html.H2(["Ana Paula"]),

    ana_tabs,
    ygraph
])

@app.callback(
    Output(component_id='main_graph', component_property='figure'),
    [Input(component_id='slct_group', component_property='value'), Input(component_id='slct_unit', component_property='value')]
)
def update_graph(option_slctd, unit_slctd):
    print("Option selected:", option_slctd, unit_slctd)

    if option_slctd == None or unit_slctd == None:
        return

    ddf = pysqldf("""
    SELECT {0}, SUM({1}) as {1}
    from df
    GROUP BY {0}
    """.format(option_slctd, unit_slctd))

    fig = px.line(ddf, x=option_slctd, y=unit_slctd, color_discrete_sequence=colors)
    fig = fig.update_xaxes(fixedrange=True, gridcolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.2)")
    fig = fig.update_yaxes(fixedrange=True, gridcolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.2)")

    fig = fig.update_layout({"paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "#F7F6F6"})

    return fig

@app.callback(
    Output(component_id='follower_graph', component_property='figure'),
    Input(component_id='slct_group-2', component_property='value')
)
def update_graph2(option_slctd):
    print("Option selected:", option_slctd)

    if option_slctd == None:
        return {}

    ddf = pysqldf("""
    SELECT {0}, SUM(Followers) as Followers
    from df
    GROUP BY {0}
    """.format(option_slctd))

    fig = px.line(ddf, x=option_slctd, y="Followers", color_discrete_sequence=colors)
    fig = fig.update_xaxes(fixedrange=True, gridcolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.2)")
    fig = fig.update_yaxes(fixedrange=True, gridcolor="rgba(0,0,0,0.2)", linecolor="rgba(0,0,0,0.2)")

    fig = fig.update_layout({"paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "#F7F6F6"})

    return fig    

if __name__ == '__main__':
    app.run_server(debug=True)
