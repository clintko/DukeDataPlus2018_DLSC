import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

color = {"background": "black",
         "text": "white"}

df = pd.read_csv(
# It can read any csv file
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

# We only use one image for demonstration purpose
figures=[
    { 'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                paper_bgcolor=color["background"],
                plot_bgcolor=color["background"],
                font={"color": color["text"], "size": 11}
            )},
    {},
    {},
]

# Composing the website
app.layout = html.Div(style={"backgroundColor": color["background"], "height": "120vh"}, children=[
        # title and header
        html.H2(style={"margin-left": "5vh", "color": color["text"]}, children="Deep Learning For Single Cell Analysis"),
        html.H4(style={"margin-left": "5vh", "color": color["text"]},
                children="By Daniel Tao and Bob Ding, under the guidance of Kuei Yueh Ko and Prof. Cliburn Chen"),

        # figure and visualization
        html.Div(children=[
            dcc.Dropdown(
                id="dropdown",
                placeholder="select cluster",
                options=[{'label': "cluster 1", "value": 0},
                         {"label": 'cluster 2', 'value': 1},
                         {"label": 'cluster 3', 'value': 2}]
            )], style={"width": "10%", "margin-left": "auto", "margin-right": "auto",
                       "backgroundColor": color["background"]}),

        html.Div(children=dcc.Graph(id="visualization"),style={"width": "50%", "margin-left": "auto",
                                                               "margin-right": "auto"})
    ]
)

# Update the website interactively
@app.callback(
    Output("visualization", "figure"),
    [Input("dropdown", "value")])
def update_figure(index):
    return figures[index]

if __name__ == "__main__":
    app.run_server()