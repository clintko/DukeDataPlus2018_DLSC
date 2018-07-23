import dash
import dash_table_experiments as dt
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from seaborn import heatmap
import cluster
import numpy as np
from data_helper import loadTSV

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


# load genelist
genelist = loadList("./data/Airway/genelist.txt")
filtered = loadTSV("./data/Airway/filtered.txt")
dropdown_label = []
color_mask_genes = []
for i in range(len(genelist)):
    dropdown_label.append({"label": genelist[i], "value": i})
    color_mask_genes.append(filtered[:, i])

# draw website
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
                        {"label": "PBMC", "value": "PBMC"},
                        {"label": "Airway", "value": "Airway"},
                        {"label": "Gland", "value": "Gland"}
                    ],
                    value="Airway",
                    id="dataset-dropdown"
                )
            ], style={"width": "20%", "display": "inline-block"}
                     ),

            # dimension reduction button
            html.Div(id="dropdown2", children=[
                html.H3("Choose dimension reduction method", style={"text-align": "center"}),
                dcc.Dropdown(
                    options=[
                        {"label": "none", "value": "none"},
                        {"label": "PCA", "value": "pca"},
                        {"label": "autoencoder", "value": "auto"},
                    ],
                    value="none",
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
            ], style={"width": "20%", "display": "inline-block"}),

            # gene button
            html.Div(id="dropdown5", children=[
                html.H3("Choose the gene to visualize", style={"text-align": "center"}),
                dcc.Dropdown(
                    options=dropdown_label,
                    value=0,
                    searchable=True,
                    id="gene-dropdown"
                )
            ], style={"width": "20%", "display": "inline-block"})
        ], style={"align": "center"}),


        # Graphs
        dcc.Graph(
            id="graph-1",
            figure={},
            config={
                'displayModeBar': False
            },
            style={'display': "inline-block", "width": "50%"}
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
            dt.DataTable(
                rows=[{}],
                sortable=True,
                id="table"
            )
        ], style={"border": "solid gray", "width": "100%", "text-align": "center", "display": "inline-block"},
    )

])

@app.callback(
    dash.dependencies.Output("table", "rows"),
    [dash.dependencies.Input("kmean-dropdown", "value"),
    dash.dependencies.Input("dimension-dropdown", "value"),
    dash.dependencies.Input("dataset-dropdown", "value")])
def update_table(value, dim_method, dataset):
    # load dataset
    filepath = "./data/" + dataset + "/" + dim_method + "/"

    # load data
    gene_tables = []
    for k_ in range(1, 9):
        gene_tables.append(loadTable(filepath + "geneTable_" + str(k_) + ".txt"))
    gene_list = loadList(filepath + "genelist.txt")

    # generate table
    rows = []
    cols = ["Genes"]
    for k in range(1, value + 1):
        cols.append("Cluster" + str(k))
    for i in range(len(gene_list)):
        row = {}
        row["Genes"] = gene_list[i]
        for j in range(1, len(cols)):
            row[cols[j]] = round(gene_tables[value - 1][i][j - 1], 3)
        rows.append(row)
    return rows


@app.callback(
    dash.dependencies.Output('graph-2', 'figure'),
    [dash.dependencies.Input('kmean-dropdown', 'value'),
     dash.dependencies.Input("dimension-dropdown", "value"),
     dash.dependencies.Input("dataset-dropdown", "value")])
def update_graph_2(value, dim_method, dataset):
    filepath = './data/' + dataset + "/" + dim_method + "/" + 'tsne.txt'
    tsne = load(filepath)
    color_mask = []
    for k_ in range(1, 9):
        color_mask.append(loadColorMask("./data/" + dataset + "/" + dim_method + "/" + "color_mask_" + str(k_) + ".txt")
                          )
    text = []
    for i in color_mask[value - 1]:
        text.append("Cluster " + str(i))
    rx = [min(tsne[0]) - 10, max(tsne[0]) + 10]
    ry = [min(tsne[1]) - 10, max(tsne[1]) + 10]
    return {
        'data': [
            go.Scattergl(
                x=tsne[0],
                y=tsne[1],
                text=text,
                mode="markers",
                marker=dict(
                    color=color_mask[value - 1],  # set color equal to a variable
                    showscale=True,
                    colorscale="Jet"
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
                "range": rx,
                "zeroline": False
            },
            yaxis={
                "range": ry,
                "zeroline": False
                }
        )
    }


@app.callback(
    dash.dependencies.Output("gene-dropdown", "options"),
    [dash.dependencies.Input("dataset-dropdown", "value")])
def update_gene_dropdown(dataset):
    filename = "./data/" + dataset
    genelist = loadList(filename+"/genelist.txt")
    print(len(genelist))
    dropdown_label = []
    for i in range(len(genelist)):
        dropdown_label.append({"label": genelist[i], "value": i})
    return dropdown_label


@app.callback(
    dash.dependencies.Output("graph-1", "figure"),
    [dash.dependencies.Input("visualization-dropdown", "value"),
     dash.dependencies.Input("dimension-dropdown", "value"),
     dash.dependencies.Input("gene-dropdown", "value"),
     dash.dependencies.Input("dataset-dropdown", "value")])
def update_graph1(value, dim_method, gene, dataset):
    # load
    filepath = './data/' + dataset + "/" + dim_method + '/tsne.txt'
    tsne = load(filepath)
    # generate range
    rx = [min(tsne[0]) - 10, max(tsne[0]) + 10]
    ry = [min(tsne[1]) - 10, max(tsne[1]) + 10]
    return {'data': [
        go.Scattergl(
            x=tsne[0],
            y=tsne[1],
            mode="markers",
            marker=dict(
                # set color equal to a variable
                color=color_mask_genes[gene],
                colorscale='Jet',
                showscale=True
                )
            )], 'layout': go.Layout(
            autosize=False,
            title="TSNE with Genes",
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
                "range": rx,
                "zeroline": False
            },
            yaxis={
                "mirror": False,
                "range": ry,
                "zeroline": False,
        })}

if __name__ == "__main__":
    app.run_server()
