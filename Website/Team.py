import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

team = dash.Dash()


# Composing the website
team.layout = html.Div(style={"height": "200vh", "font-family": "Georgia", "border": "black"}, children=[


    # introduction of our team
    html.H3('Our Team:', style={"align": "center", 'margin-left': '8.66666666667%'}),
    # Bob Ding
    html.Div([
        html.Div([
            html.Div([
                html.H4(style={"margin-left": "8.66666666667%"}, children='Bob Ding'),
                html.P(style={"margin-left": "8.66666666667%"}, children="""My name is Bob Ding. I\'m currently a 
                Duke 2021 Undergraduate majoring in Mathematics and Statistics.""")
            ], className="four columns"),

            html.Div([
                html.Img(src='https://bigdata.duke.edu/sites/bigdata.duke.edu/files/styles/'
                             'masonry_item_225px/public/Ziyang-Bob-Ding.jpg?itok=XlqD2o5g',
                        style={"margin-top": "2vh", "margin-left": "3vh"}),
            ], className="four columns"),
        ], className="row"),
        ]),

    # Daniel Tao
    html.Div([
        html.Div([
            html.Div([
                html.H4(children='Daniel Tao'),
                html.P(children="""My name is Daniel Tao. I\'m currently a
                Duke 2021 undergraduate majoring in ECE and Computer Science.""")
            ], className="four columns"),
            html.Div([
                html.Img(src='https://bigdata.duke.edu/sites/bigdata.duke.edu/files/styles/'
                             'masonry_item_225px/public/Daniel%20Tao.jpg?itok=RQ6bv037',
                         style={"margin-top": "2vh", "margin-left": "3vh"}),
            ], className="four columns"),
        ], className="row", style={"border-style": "solid"}),
        ]),

    # Kuei
    html.Div([
        html.Div([
            html.Div([
                html.H4(style={"margin-left": "8.66666666667%"}, children='Kuei Yueh Ko'),
                html.P(style={"margin-left": "8.66666666667%"}, children="""My name is Kuei blablabla""")
            ], className="four columns"),
            html.Div([
                html.Img(src='https://bigdata.duke.edu/sites/bigdata.duke.edu/files/styles/'
                             'masonry_item_225px/public/Kuei%20Yueh%20Ko.jpg?itok=o6anbMzO',
                         style={"margin-top": "2vh", "margin-left": "3vh"}),
            ], className="four columns"),
        ], className="row"),
    ]),

    # Professor Cliburn
    html.Div([
        html.Div([
            html.Div([
                html.H4(style={"margin-left": "8.66666666667%"}, children='Doc. Cliburn Chan'),
                html.P(style={"margin-left": "8.66666666667%"}, children="""I am Doc Cilburn Chan blablabla""")
            ], className="four columns"),
            html.Div([
                html.Img(src='https://genome.duke.edu/sites/genome.duke.edu/files/styles/'
                             'gcb_350x350/public/Chan%2C%20Cliburn.jpg?itok=QUoyoCq5',
                         style={"margin-top": "2vh", "margin-left": "3vh"}),
            ], className="four columns"),
        ], className="row"),
    ])
])

# css style repository
team.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == "__main__":
    team.run_server()
