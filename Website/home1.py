import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plot

# load file and generate tsne
filepath = '../data/mincell=50_mingene=100/filtered.txt'
tsne = plot.getTsne(filepath)

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

    # empty
    html.Br(),

    # graph
    html.Div(style={"border": "solid"}, children=[
        dcc.Graph(
            id="graph-1",
            figure={
                'data': [
                    go.Scattergl(
                        x=tsne[0],
                        y=tsne[1],
                        mode="markers",
                        marker=dict(
                            size=16,
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
                    height="100vh",
                    width="40%",
                    hovermode="closest",
                    margin={
                        "r": 20,
                        "t": 50,
                        "b": 20,
                        "l": 50
                    },
                    xaxis={
                        "autorange": True,
                        "linecolor": "rgb(0, 0, 0)",
                        "linewidth": 1,
                        "range": [],
                        "showgrid": False,
                        "showline": True,
                        "title": "",
                        "type": "linear"
                    },
                    yaxis={
                        "autorange": False,
                        "gridcolor": "rgba(127, 127, 127, 0.2)",
                        "mirror": False,
                        "nticks": 0,
                        "range": [],
                        "showgrid": True,
                        "showline": True,
                        "ticklen": 10,
                        "ticks": "outside",
                        "title": "",
                        "type": "linear",
                        "zeroline": False,
                        "zerolinewidth": 4
                    }
                )
            },
            config={
                'displayModeBar': False
            }
        ),
        dcc.Graph(
            id="graph-2",
            figure={
                'data': [
                    go.Scattergl(
                        x=tsne[0],
                        y=tsne[1],
                        mode="markers",
                        marker=dict(
                            size=16,
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
                    height="100vh",
                    width="40%",
                    hovermode="closest",
                    margin={
                        "r": 20,
                        "t": 50,
                        "b": 20,
                        "l": 50
                    },
                    xaxis={
                        "autorange": True,
                        "linecolor": "rgb(0, 0, 0)",
                        "linewidth": 1,
                        "range": [],
                        "showgrid": False,
                        "showline": True,
                        "title": "",
                        "type": "linear"
                    },
                    yaxis={
                        "autorange": False,
                        "gridcolor": "rgba(127, 127, 127, 0.2)",
                        "mirror": False,
                        "nticks": 0,
                        "range": [],
                        "showgrid": True,
                        "showline": True,
                        "ticklen": 10,
                        "ticks": "outside",
                        "title": "",
                        "type": "linear",
                        "zeroline": False,
                        "zerolinewidth": 4
                    }
                )
            },
            config={
                'displayModeBar': False
            }
        )
    ]),
    ])


if __name__ == "__main__":
    app.run_server()