import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plot
import cluster

# load method from txt
def load(file):
    with open(file, "r") as o:
        data = o.read()
    lines = data.splitlines()
    n = int(lines[0])
    x = []
    y = []
    for n_ in range(n):
        x.append(float(lines[1 + n_].split()[0]))
        y.append(float(lines[1 + n_].split()[1]))
    return x, y

def loadColorMask(file):
    with open(file, "r") as o:
        data = o.read()
    lines = data.splitlines()
    result = []
    for n_ in range(len(lines)):
        result.append(int(lines[n_]))
    return result

# load file
filepath = './data/tsne.txt'
tsne = load(filepath)
filename = "../data/mincell=3_mingene=200/filtered.txt"
color_mask = []
for k_ in range(1, 9):
    color_mask.append(loadColorMask("./data/color_mask_" + str(k_) + ".txt"))

# _, color_mask = cluster.kmeans(filename)

app = dash.Dash()

app.layout = html.Div(style={"height": "200vh", "fontFamily": "Georgia"}, children=[
    # head
    html.Div(style={'background-color': "#CEF0EF", "height": "10vh", "width": "100%"}, children=[
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/e/e1/Duke_Athletics_logo.svg', height="50vh",
                 width="50vh", style={"margin-top": "2vh", "margin-left": "3vh"}),
        html.Ul(style={"float": "right", "list-style": "none", "margin-right": "5vh"},
                children=[
            html.Li(children=["About"], style={"font-size": "15px", "display": "inline-block", "padding": "2vh"}),
            html.Li(children=["Home"], style={"font-size": "15px", "display": "inline-block", "padding": "2vh"}),
            html.Li(children=["Team"], style={"font-size": "15px", "display": "inline-block", "padding": "2vh"})
        ])]),

    # empty placeholder
    html.Div(style={"height": "5vh"}),

    # graph
    html.Div(style={"border": "solid gray"}, children=[
        html.H3("Input K number", style={"margin-left": "3vh"}),
        dcc.Dropdown(
            options=[
                {"label": "3", "value": 3},
                {"label": "4", "value": 4},
                {"label": "5", "value": 5},
                {"label": "6", "value": 6},
                {"label": "7", "value": 7},
                {"label": "8", "value": 8}
            ],
            placeholder="Select k value",
            value=8,
            id="kmean-dropdown"
        ),
        dcc.Graph(
            id="graph-1",
            figure={
                'data': [
                    go.Scattergl(
                        x=tsne[0],
                        y=tsne[1],
                        mode="markers",
                        marker=dict(
                              # set color equal to a variable
                            colorscale='Viridis',
                            showscale=True
                        )
                    )
                ],
                'layout': go.Layout(
                    autosize=False,
                    title="TSNE",
                    font={
                        "family": "Raleway",
                        "size": "5vh"
                    },
                    height="200vh",
                    width="30%",
                    hovermode="closest",
                    margin={
                        "r": 0,
                        "t": 50,
                        "b": 40,
                        "l": 100
                    },
                    xaxis={
                        "range": [-100, 100],
                        "zeroline": False
                    },
                    yaxis={
                        "mirror": False,
                        "range": [-100, 100],
                        "zeroline": False,
                    }
                )
            },
            config={
                'displayModeBar': False
            },
            style={'display': "inline-block"}
        ),

        dcc.Graph(
            id="graph-2",
            config={
                'displayModeBar': False
            }, figure={
                'data': [
                    go.Scattergl(
                        x=tsne[0],
                        y=tsne[1],
                        mode="markers",
                        marker=dict(
                            color=color_mask[7],  # set color equal to a variable
                            colorscale='Viridis',
                            showscale=True
                        )
                    )
                ],
                'layout': go.Layout(
                    autosize=False,
                    title="TSNE with KMeans",
                    font={
                        "family": "Raleway",
                        "size": "5vh"
                    },
                    height="200vh",
                    width="40%",
                    hovermode="closest",
                    margin={
                        "r": 0,
                        "t": 50,
                        "b": 40,
                        "l": 100
                    },
                    xaxis={
                        "range": [-100, 100],
                        "zeroline": False
                    },
                    yaxis={
                        "range": [-100, 100],
                        "zeroline": False
                        }
                )
            },
            style={'display': "inline-block", "width": "30%"}
        )
    ]),

    # empty placeholder
    html.Div(style={"height": "5vh"}),

    # table
    html.Div(style={"border": "solid gray", "width": "50%"}, children=[
        html.H1("table here")
    ])

])


@app.callback(
    dash.dependencies.Output('graph-2', 'figure'),
    [dash.dependencies.Input('kmean-dropdown', 'value')])
def update_graph_2(value):
    return {
                'data': [
                    go.Scattergl(
                        x=tsne[0],
                        y=tsne[1],
                        mode="markers",
                        marker=dict(
                            color=color_mask[value - 1],  # set color equal to a variable
                            colorscale='Viridis',
                            showscale=True
                        )
                    )
                ],
                'layout': go.Layout(
                    autosize=False,
                    title="TSNE with KMeans",
                    font={
                        "family": "Raleway",
                        "size": "5vh"
                    },
                    height="200vh",
                    width="40%",
                    hovermode="closest",
                    margin={
                        "r": 0,
                        "t": 50,
                        "b": 40,
                        "l": 100
                    },
                    xaxis={
                        "range": [-100, 100],
                        "zeroline": False
                    },
                    yaxis={
                        "range": [-100, 100],
                        "zeroline": False
                        }
                )
            }


if __name__ == "__main__":
    app.run_server()
