import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

# reading the normal plot file
# convert the tsv into csv
tsv_file = '/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/normal.tsv'
table = pd.read_table(tsv_file, sep='\t')
table.to_csv('/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/normal.csv', index=False)

# read the csv
df = pd.read_csv(
    '/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/normal.csv')
normal = df.drop('Unnamed: 0', 1)

# reading the log likelihood file
tsv_file = '/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/log_likelihood.tsv'
table = pd.read_table(tsv_file, sep='\t')
table.to_csv('/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/log_likelihood.csv', index=False)

df = pd.read_csv(
    '/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/log_likelihood.csv')
likelihood = df.drop('Unnamed: 0', 1)
likelihood = pd.concat([normal, likelihood], axis=1)

# reading the learning file
tsv_file = '/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/learn.tsv'
table = pd.read_table(tsv_file, sep='\t')
table.to_csv('/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/learn.csv', index=False)

learn = pd.read_csv(
    '/Users/dzy/Desktop/变量/Programs/DATA+/scvis-dev/output/bipolar/learn.csv')

# We only use one image for demonstration purpose
figures = {
    # data plot
    'normal':
        dict(data=[
            go.Scatter(
                x = normal['z_coordinate_0'],
                y = normal['z_coordinate_1'],
                text='observation' + str(i),
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 3,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in normal
        ], layout=go.Layout(
            xaxis={'title': 'z_coordinate_0'},
            yaxis={'title': 'z_coordinate_1'},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            font={"size": 11}
        )),

    # log likelihood
    'likelihood':
        dict(data=[
            go.Scatter(
                x =likelihood['z_coordinate_0'],
                y =likelihood['z_coordinate_1'],
                text='observation' + str(i) + str(likelihood['log_likelihood']),
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 3,
                    'color': likelihood['log_likelihood'],
                    'colorscale': 'Viridis',
                    'showscale': True
                },
                name=i
            ) for i in likelihood
        ], layout=go.Layout(
            xaxis={'title': 'z_coordinate_0'},
            yaxis={'title': 'z_coordinate_1'},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            font={"size": 11}
        )),

    # ELBO value
    'learn_ELBO':
        dict(data=[
            go.Scatter(
                x = learn['Unnamed: 0'],
                y = learn['elbo'],
                text='ELBO cost = ' + str(learn['elbo']) + 'at iteration' + str(i),
                mode='lines',
                marker={
                    'line': {'width': 0.5, 'color': 'blue'}
                },
                name=i
            ) for i in learn
        ], layout=go.Layout(
            xaxis={'title': 'iteration'},
            yaxis={'title': 'ELBO'},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            font={"size": 11}
        )),

    # TSNE learning loss
    'learn_TSNE' :
        dict(data=[
            go.Scatter(
                x = learn['Unnamed: 0'],
                y = learn['tsne_cost'],
                text='TSNE cost = ' + str(learn['tsne_cost']) + 'at iteration' + str(i),
                mode='lines',
                marker={
                    'line': {'width': 0.5, 'color': 'blue'}
                },
                name=i
            ) for i in learn
        ], layout=go.Layout(
            xaxis={'title': 'iteration'},
            yaxis={'title': 'TSNE Cost'},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            font={"size": 11}
        ))
}

# Composing the website
app.layout = html.Div(style={"height": "200vh", "font-family": "Georgia"}, children=[

    # title and header
    html.Div(
        html.H1(style={"text-align": "center", "font-weight": "heavy", },
            children="Deep Learning For Single Cell Analysis"),
                      style={"background-color":"#01FE41"}),

    html.H4(style={"margin-top": "50px", "text-align": "center"},
            children="By Daniel Tao and Bob Ding, under the guidance of Kuei Yueh Ko and Prof. Cliburn Chen"),

    # introduction of our team
    html.H3('Our Team:', style={"align": "center", 'margin-left': '8.66666666667%'}),
    # Bob Ding
    html.Div([
        html.Div([
            html.Div([
                html.H4(style={"margin-left": "8.66666666667%"}, children='Bob Ding'),
                html.P(style={"margin-left": "8.66666666667%"}, children="""My name is Bob Ding. I\'m currently a 
                Duke 2021 Undergraduate majoring in Mathematics and Statistics.""")
            ], className="five columns"),

            html.Div([
                html.H3(style={"margin-right": "8.66666666667%"}, children='My Image'),
            ], className="five columns"),
        ], className="row"),
        ]),

    # Daniel Tao
    html.Div([
        html.Div([
            html.Div([
                html.H4(style={"margin-left":"8.66666666667%" }, children='Daniel Tao'),
                html.P(style={"margin-left":"8.66666666667%" }, children="""My name is Daniel Tao. I\'m currently a
                Duke 2021 undergraduate majoring in ECE and Computer Science.""")
            ], className="five columns"),
            html.Div([
                html.H3(style={"margin-right":"8.66666666667%"}, children='My Image'),
            ], className="five columns"),
        ], className="row"),
        ]),

    # Kuei
    html.Div([
        html.Div([
            html.Div([
                html.H4(style={"margin-left": "8.66666666667%"}, children='Kuei Yueh Ko'),
                html.P(style={"margin-left": "8.66666666667%"}, children="""My name is Daniel Tao. I\'m currently a
            Duke 2021 undergraduate majoring in ECE and Computer Science.""")
            ], className="five columns"),
            html.Div([
                html.H3(style={"margin-right": "8.66666666667%"}, children='My Image'),
            ], className="five columns"),
        ], className="row"),
    ]),

    # Professor Cliburn
    html.Div([
        html.Div([
            html.Div([
                html.H4(style={"margin-left": "8.66666666667%"}, children='Doc. Cliburn Chan'),
                html.P(style={"margin-left": "8.66666666667%"}, children="""My name is Daniel Tao. I\'m currently a
            Duke 2021 undergraduate majoring in ECE and Computer Science.""")
            ], className="five columns"),
            html.Div([
                html.H3(style={"margin-right": "8.66666666667%"}, children='My Image'),
            ], className="five columns"),
        ], className="row"),
    ]),

    # figure and visualization


    html.Div([

        html.Div(
            dcc.Tabs(
                id = "Tabs",
                tabs=[
                    {"label": 'normal', 'value': 'normal'},
                    {"label": 'log likelihood', 'value': 'likelihood'},
                    {"label": 'ELBO value', 'value': 'learn_ELBO'},
                    {"label": 'TSNE cost', 'value': 'learn_TSNE'}
                ],
                value=3,
                vertical=True,
                style={
                    'height': '100vh',
                    'borderRight': 'thin lightgrey solid',
                    'textAlign': 'left'}
                )
            , style={'width': '20%', 'float': 'left'}),
        html.Div(children=dcc.Graph(id="visualization", style={"height": "70vh"})
                 , style={'width': '80%', 'float': 'right'})]
        , style={'margin-top': '40px', 'width': '80%',
                 'margin-left': 'auto', 'margin-right': 'auto',
                 "border": "thin lightgrey solid"})
])

# css style repository
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
}),


# Update the website interactively
@app.callback(
    Output("visualization", "figure"),
    [Input("Tabs", "value")])
def update_figure(p):
    return figures[p]


if __name__ == "__main__":
    app.run_server()
