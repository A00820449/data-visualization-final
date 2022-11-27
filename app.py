# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from pandasql import sqldf 
pysqldf = lambda q: sqldf(q, globals())

app = Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

df = pd.read_csv("clean.csv")

months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
colors = ['#E8570E', '#FF8730', '#E06E48', '#FFA96B', '#E89D80', '#FACAA5', '#E8C6B7']


### Ana Paula ###

ydf1 = df.groupby(['Paid']).mean()
ydf1=ydf1.reset_index()
ydf1[['Paid','Reach','EngagedUsers']]

ana_fig1 =  px.pie(ydf1, names='Paid', values='EngagedUsers', hole=0.5, color_discrete_sequence=colors)

data0 = go.Bar(
    x = ydf1.EngagedUsers,
    y = ydf1.Paid,
    name = 'EngagedUsers',
    textposition = 'outside',
    texttemplate = '%(text:.2f)'
)
data1 = go.Bar(
    x = ydf1.Reach,
    y = ydf1.Paid,
    name = 'Reach',
    textposition = 'outside',
    texttemplate = '%(text:.2f)'
)

data = [data0, data1]

layout = go.Layout(title = 'Publicidad pagada')

ana_fig2 = go.Figure(data = data, layout = layout)

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

### Yuyu Fin ##



app.layout = html.Div(className="test", children=[
    html.H1(children='Final Project'),
    
    html.H2(["Interactions"]),

    html.Div([
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

    html.H2(["Ana Paula"]),

    dcc.Graph(figure=ana_fig1),
    dcc.Graph(figure=ana_fig2),
    dcc.Graph(figure=ana_fig3),
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

    fig = px.bar(ddf, x=option_slctd, y=unit_slctd, range_y=[0,20_000], color_discrete_sequence=colors)
    fig = fig.update_xaxes(fixedrange=True)
    fig = fig.update_yaxes(fixedrange=True)

    fig = fig.update_layout({"paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "#F7F6F6"})

    return fig        ###

if __name__ == '__main__':
    app.run_server(debug=True)
