import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from seaborn import heatmap
import cluster
import numpy as np

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

def loadTable(file):
    with open(file, "r") as o:
        data = o.read()
    lines = data.splitlines()
    result = np.zeros(shape=(len(lines), len(lines[0].split())))
    for i in range(len(lines)):
        for j in range(len(lines[0].split())):
            result[i, j] = float(lines[i].split()[j])
    return result

def loadList(file):
    with open(file, "r") as o:
        data = o.read()
    lines = data.splitlines()
    result = []
    for n_ in range(len(lines)):
        result.append(lines[n_])
    return result




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
        # dataset button
        html.Div(id="buttons", children=[
        html.Div(id="dropdown1", children=[
            html.H3("Choose dataset", style={"text-align": "center"}),
            dcc.Dropdown(
                options=[
                    {"label": "PBMC", "value": 1}
                ],
                value=1,
                id="dataset-dropdown"
            )
        ], style={"width": "20%", "display": "inline-block"}
                 ),

        # dimension reduction button
        html.Div(id="dropdown2", children=[
            html.H3("Choose dimension reduction method", style={"text-align": "center"}),
            dcc.Dropdown(
                options=[
                    {"label": "none", "value": 0},
                    {"label": "PCA", "value": 1},
                    {"label": "autoencoder", "value": 2},
                ],
                value=0,
                id="dimension-dropdown"
            )
        ], style={"width": "20%", "display": "inline-block"}
                 ),

        # k means button
        html.Div(id="dropdown3", children=[
            html.H3("Choose K value for KMeans clustering", style={"text-align": "center"}),
            dcc.Dropdown(
                options=[
                    {"label": "2", "value": 2},
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
            )],
                 style={"width": "20%", "display": "inline-block"}
                 ),

        # visualization button
        html.Div(id="dropdown4", children=[
            html.H3("Choose visualization", style={"text-align": "center"}),
            dcc.Dropdown(
                options=[
                    {"label": "TSNE", "value": 0},
                    {"label": "SCVIS", "value": 1}
                ],
                value=0,
                id="visualization-dropdown"
            )
        ], style={"width": "20%", "display": "inline-block"}
                 )], style={"align": "center"}),

        dcc.Graph(
            id="graph-1",
            figure={},
            config={
                'displayModeBar': False
            },
            style={'display': "inline-block"}
        ),

        dcc.Graph(
            id="graph-2",
            config={
                'displayModeBar': False
            }, figure={}, style={'display': "inline-block", "width": "30%"}
        )
    ]),

    # empty placeholder
    html.Div(style={"height": "5vh"}),


    # table
    html.Div(children=[
        # table
        html.Div(style={"border": "solid gray", "width": "100%", "text-align": "center", "display": "inline-block"},
                 id="table", children=[])

        # heatmap
        #dcc.Graph(
        #    id="heatmap",
         #   figure={},
         #   style={"width": "40%", "display": "inline-block", "height": "80vh"}
       # )
    #], style={"width": "100%"}),
        ]
    )
])

@app.callback(
    dash.dependencies.Output("table", "children"),
    [dash.dependencies.Input("kmean-dropdown", "value")])
def update_table(value, dim_method):
    # load data
    if dim_method == 0:
        color_mask = []
        gene_tables = []
        for k_ in range(1, 9):
            color_mask.append(loadColorMask("./data/PBMC/none/color_mask_" + str(k_) + ".txt"))
            gene_tables.append(loadTable("./data/PBMC/none/geneTable_" + str(k_) + ".txt"))
        gene_list = loadList("./data/PBMC/none/genelist.txt")
    else:
        color_mask = []
        gene_tables = []
        for k_ in range(1, 9):
            color_mask.append(loadColorMask("./data/PBMC/pca/color_mask_" + str(k_) + ".txt"))
            gene_tables.append(loadTable("./data/PBMC/pca/geneTable_" + str(k_) + ".txt"))
        gene_list = loadList("./data/PBMC/pca/genelist.txt")

    # generate table
    body = []
    for i in range(100):
        row = [html.Td(gene_list[i], style={"background-color": "#CEF0EF"})]
        for j in range(value):
            row.append(html.Td(round(gene_tables[value - 1][i][j], 3), style={"background-color": "#EEFCFB"}))
        body.append(html.Tr(row))

    header = [html.Th("Genes")]
    for k in range(1, value + 1):
        header.append(html.Th("Cluster" + str(k), style={"background-color": "#CEF0EF"}))
    return html.Table(
        # header
        header +
        # body
        body,
        style={"width": "100%"}
    )

#@app.callback(
#    dash.dependencies.Output("heatmap", "figure"),
#    [dash.dependencies.Input("kmean-dropdown", "value")])
#def update_heatmap(value):
##    return {
  #      "data": [go.Heatmap(
   #         x=list(range(1, value + 1)),
    #        y=gene_list[:100],
     #       z=gene_tables[value - 1][:100],
      #      colorscale='Viridis'
       # )],

       # "layout": go.Layout(
       #     title="Gene Heatmap",
       #     xaxis=dict(ticks=''),
       ##     yaxis=dict(ticks='')
        #)
   # }



@app.callback(
    dash.dependencies.Output('graph-2', 'figure'),
    [dash.dependencies.Input('kmean-dropdown', 'value'),
     dash.dependencies.Input("dimension-dropdown", "value")])
def update_graph_2(value, dim_method):
    filepath = './data/PBMC/none/tsne.txt'
    filepath_pca = "./data/PBMC/pca/tsne.txt"
    if dim_method == 0:
        tsne = load(filepath)
    else:
        tsne = load(filepath_pca)
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


@app.callback(
    dash.dependencies.Output("graph-1", "figure"),
    [dash.dependencies.Input("visualization-dropdown", "value"),
     dash.dependencies.Input("dimension-dropdown", "value")])
def update_graph1(value, dim_method):
    filepath = './data/PBMC/none/tsne.txt'
    filepath_pca = "./data/PBMC/pca/tsne.txt"
    if not value:
        if dim_method == 0:
            tsne = load(filepath)
        else:
            tsne=[]
        return {'data': [
            go.Scattergl(x=tsne[0],
            y=tsne[1],
            mode="markers",
            marker=dict(
                # set color equal to a variable
                colorscale='Viridis',
                showscale=True
                )
            )], 'layout': go.Layout(
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
            })}

if __name__ == "__main__":
    app.run_server()
