import dash
import os
import base64
import io
import dash_table_experiments as dt
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from seaborn import heatmap
import cluster
import numpy as np
from data_helper import loadTSV
import scipy.stats as stats
from generateDATA import realOneClick


UPLOAD_DIR = "./data/upload/"
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


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode('utf8').split(b';base64,')[1]
    with open(os.path.join(UPLOAD_DIR, name), 'wb') as fp:
        fp.write(base64.decodebytes(data))

print(dcc.__version__)
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
app.config.suppress_callback_exceptions = True
app.layout = html.Div(style={"height": "150vh", "fontFamily": "Georgia"}, children=[
    # dcc
    dcc.Location(id="url", refresh=False),
    # head
    html.Div(style={'background-color': "#CEF0EF", "height": "10vh", "width": "100%"}, children=[
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/e/e1/Duke_Athletics_logo.svg', height="50vh",
                 width="50vh", style={"margin-top": "2vh", "margin-left": "3vh"}),
        html.Ul(style={"float": "right", "list-style": "none", "margin-right": "5vh"},
                children=[
            html.Li(children=[dcc.Link("About", href="/about")],
                    style={"font-size": "15px", "display": "inline-block", "padding": "2vh"}),
            html.Li(children=[dcc.Link("Home", href="/home")],
                    style={"font-size": "15px", "display": "inline-block", "padding": "2vh"}),
            html.Li(children=[dcc.Link("Team", href="./team")],
                    style={"font-size": "15px", "display": "inline-block", "padding": "2vh"})
        ])]),

    # empty placeholder
    html.Div(style={"height": "5vh"}),

    # graph
    html.Div(id="main", children=[html.Div([html.Div(style={"border": "solid gray"}, children=[
            # dataset button
            html.Div(id="buttons", children=[
                html.Div(id="dropdown1", children=[
                    html.H3("Choose dataset", style={"text-align": "center"}),
                    dcc.Dropdown(
                        options=[
                            {"label": "PBMC", "value": "PBMC"},
                            {"label": "Airway", "value": "Airway"},
                            {"label": "Gland", "value": "Gland"},
                            {"label": "Your Upload", "value": "upload"}
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
                        options=[],
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
            html.Div(children=[
                # empty placeholder
                html.Div(style={"height": "5vh"}),

                dcc.Graph(
                    id="graph-1",
                    figure={},
                    config={
                        'displayModeBar': True
                    })
            ], style={'display': "inline-block", "width": "50%"}),

            html.Div(children=[
                # empty placeholder
                html.Div(style={"height": "5vh"}),

                dcc.Graph(
                    id="graph-2",
                    config={
                        'displayModeBar': True
                    },
                    figure={}
                )
            ], style={'display': "inline-block", "width": "30%"})
        ]),

        # empty placeholder
        html.Div(style={"height": "5vh"}),

        # table
        html.Div(children=[
            dt.DataTable(
                rows=[{}],
                sortable=True,
                id="table",
             )
            ], style={"border": "solid gray", "width": "100%", "text-align": "center", "display": "inline-block"},
        ),

        # empty placeholder
        html.Div(style={"height": "5vh"}),

        # upload button
        html.Div(children=[
            html.H3("Upload your own dataset. Please wait for about 30 minutes for program to finish computing.",
                    style={"text-align": "center"}),
            html.H3("Please upload a csv file", style={"text-align": "center"}),
            html.H3("The rows should be observations/cells, and the columns be genes.", style={"text-align": "center"}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files', style={"background-color": "#CEF0EF"})
                ]),
                style={
                    'width': '80%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': 'auto'
                }),
            html.H3("Uploaded: "),
            html.Ul(id="uploaded"),
            html.H3(id="processing"),
        ], style={"border": "solid gray", "align": "center"})])])
])


about_page = html.Div(style={"height": "200vh", "font-family": "Georgia"}, children=[
    html.Div(style={"height": "20px"}),

    # title single cell analysis
    html.Div(style={"margin-top": "1vh", "align": "center"}, children=[
        html.H1(style={"text-align": "center", "vertical-align": "middle"},
                children=["Deep Learning for Single Cell Analysis"])
    ]),

    # empty placeholder
    html.Div(style={"height": "20px"}),

    # first paragraph for background
    html.Div(style={"width": "80%", "margin": "auto", "font-size": "18px"},
             children=["In the field of cellular biology, single cell analysis serves as an important role in "
                       "understanding genomics and their behaviors from the microscopic level. As technology "
                       "has improved the efficacy of obtaining quantified data from single cell’s mRNA expression, "
                       "single cell analysis found its new basis upon statistical learning methods, which incorporates "
                       "machine learning and deep learning methods. \n"]),

    # empty div
    html.Div(style={"height": "20px"}),

    html.Div(style={"width": "80%", "margin": "auto"}, className="row", children=[
        html.Img(src='https://www.rna-seqblog.com/wp-content/uploads/2016/12/heatmap-983x1024.gif',
                         style={"margin-top": "1vh", "height": "auto", "width": "50%", "display": "inline-block",
                                "vertical-align": "middle"}),
        html.Div(style={"margin-left": "3%", "font-size": "18px", "width": "45%", "display": "inline-block",
                        "vertical-align": "middle"},
                 children=["Single cell sequencing data always incorporate very high dimensional data. "
                           "Furthermore, the considering the number of different genes a genome can "
                           "possess, usually the number of observations comparing to the number of genes "
                           "are too small, leaving the sequencing data matrix very sparse. Therefore, "
                           "data cleaning is an imperative and crucial part of conducting data analysis "
                           "for single cell analysis. \n \n Furthermore, single cell analysis involves dimension"
                           " reduction, unsupervised clustering algorithms, and high dimensional data "
                           "visualization procedure. These machine learning algorithms have been fully "
                           "developed and ready to use: the algorithms packages need and "
                           "are always convenient to use… \n"])]),

    # empty div
    html.Div(style={"height": "40px"}),


    html.Div(style={"width": "80%", "margin": "auto"}, children=[
        html.Div(style={"font-size": "18px", "width": "45%", "display": "inline-block", "vertical-align": "middle"},
                 children=["Currently, even there are many single cell analysis tools and packages. Scanpy and "
                          "Seurat have all contributed great deal in integrating the entire single "
                          "cell analysis pipeline and tutor researchers how to properly use the packages. "
                          "Even so, there’re still space to make the entire process easier and handier.\n\n By using "
                          "Plotly Dash, we integrate possibly 6 different pipelines together, and make it user friendly. "
                          "This website application doesn’t require any knowledge for coding and is ready to give out "
                          "valuable information of the dataset. Users may utilize the website as a tool for research, "
                          "and hopefully excavate new cell types."]),
        html.Img(src='https://www.helsinki.fi/sites/default/files/thumbnails/image/tsne_filtered.jpg',
                 style={"margin-top": "1vh", "height": "auto", "width": "50%", "display": "inline-block",
                        "vertical-align": "middle"})
    ])
])

home_page = html.Div([html.Div(style={"border": "solid gray"}, children=[
            # dataset button
            html.Div(id="buttons", children=[
                html.Div(id="dropdown1", children=[
                    html.H3("Choose dataset", style={"text-align": "center"}),
                    dcc.Dropdown(
                        options=[
                            {"label": "PBMC", "value": "PBMC"},
                            {"label": "Airway", "value": "Airway"},
                            {"label": "Gland", "value": "Gland"},
                            {"label": "Your Upload", "value": "upload"}
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
                        options=[],
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
            html.Div(children=[
                # empty placeholder
                html.Div(style={"height": "5vh"}),

                dcc.Graph(
                    id="graph-1",
                    figure={},
                    config={
                        'displayModeBar': True
                    })
            ], style={'display': "inline-block", "width": "50%"}),

            html.Div(children=[
                # empty placeholder
                html.Div(style={"height": "5vh"}),

                dcc.Graph(
                    id="graph-2",
                    config={
                        'displayModeBar': True
                    },
                    figure={}
                )
            ], style={'display': "inline-block", "width": "30%"})
        ]),

        # empty placeholder
        html.Div(style={"height": "5vh"}),


        # table
        html.Div(children=[
            dt.DataTable(
                rows=[{}],
                sortable=True,
                id="table",
             )
            ], style={"border": "solid gray", "width": "100%", "text-align": "center", "display": "inline-block"},
        ),

        # empty placeholder
        html.Div(style={"height": "5vh"}),

        # upload button
        html.Div(children=[
            html.H3("Upload your own dataset. Please wait for about 30 minutes for program to finish computing.",
                    style={"text-align": "center"}),
            html.H3("Please upload a csv file", style={"text-align": "center"}),
            html.H3("The rows should be observations/cells, and the columns be genes.", style={"text-align": "center"}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files', style={"background-color": "#CEF0EF"})
                ]),
                style={
                    'width': '80%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': 'auto'
                }),
            html.H3("Uploaded: "),
            html.Ul(id="uploaded"),
            html.H3(id="processing"),
        ], style={"border": "solid gray", "align": "center"})])


team_page = html.Div(style={"height": "200vh", "font-family": "Georgia", "border": "black", "border": "solid"},
                     children=[
                        # empty placeholder
                        html.Div(style={"height": "5vh"}),

                         # introduction of our team
                        html.H2('Our Team:', style={"text-align": "center", "width": "40%", "margin": "auto",
                                                    "border": "solid"}),
                        # Bob Ding
                        html.Div([
                            html.Div(children=[
                                html.Div(children=[
                                    html.Img(src='https://bigdata.duke.edu/sites/bigdata.duke.edu/files/styles/'
                                                 'masonry_item_225px/public/Ziyang-Bob-Ding.jpg?itok=XlqD2o5g',
                                             style={"margin-top": "1vh", "margin-right": "8.66666666667%"}),
                                ], className="six columns"),

                                html.Div(children=[
                                    html.H4(style={"margin-left": "8.66666666667%"}, children='Bob Ding'),
                                    html.P(style={"margin-left": "8.66666666667%", "color": "red"},
                                           children="""Duke 2021 Undergraduate, 
                                    Mathematics and Statistic Major"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""One of the developers of the website,
                                    contributed to 'None' and PCA dimension reduction methods pipeline,
                                    and SCVIS visualization machine learning pipeline construction"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Email: ziyang.ding@duke.edu"""),
                                ], className="six columns")
                            ], className="row")
                            ]),

                        # Daniel
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Img(src='https://bigdata.duke.edu/sites/bigdata.duke.edu/files/styles/'
                                                 'masonry_item_225px/public/Daniel%20Tao.jpg?itok=RQ6bv037',
                                             style={"margin-top": "2vh", "margin-right": "8.66666666667%"}),
                                ], className="six columns"),
                                html.Div([
                                    html.H4(style={"margin-left": "8.66666666667%"}, children='Kuei Yueh Ko'),
                                    html.P(style={"margin-left": "8.66666666667%", "color": "red"},
                                           children="""Duke 2021 Undergraduate, 
                                                ECE and Computer Science Major"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""One of the developers of the website, built /Home page, and  
                                           contributed to all pipelines construction"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Email: chaofan.tao@duke.edu"""),
                                ], className="six columns")
                            ], className="row"),
                        ]),

                        # Kuei
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Img(src='https://bigdata.duke.edu/sites/bigdata.duke.edu/files/styles/'
                                                 'masonry_item_225px/public/Kuei%20Yueh%20Ko.jpg?itok=o6anbMzO',
                                             style={"margin-top": "2vh", "margin-right": "8.66666666667%"}),
                                ], className="six columns"),
                                html.Div([
                                    html.H4(style={"margin-left": "8.66666666667%"}, children='Kuei Yueh Ko'),
                                    html.P(style={"margin-left": "8.66666666667%", "color": "red"},
                                           children="""Duke master program Biostatistics department"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Project manager of 2018 Data+ project 8: 
                                           Deep Learning for Single Cell Analysis. 
                                           Contributed to coordinating and managing project team, 
                                           communicating with Tata's Lab, 
                                           and connecting project team with professors"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Email: kuei.yueh.ko@duke.edu"""),
                                ], className="six columns")
                            ], className="row"),
                        ]),

                        # Professor Cliburn
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Img(src='https://genome.duke.edu/sites/genome.duke.edu/files/styles/'
                                                 'gcb_350x350/public/Chan%2C%20Cliburn.jpg?itok=QUoyoCq5',
                                             style={"margin-top": "2vh", "margin-right": "8.66666666667%"}),
                                ], className="six columns"),
                                html.Div([
                                    html.H4(style={"margin-left": "8.66666666667%"}, children='Cliburn Chan, PHD'),
                                    html.P(style={"margin-left": "8.66666666667%", "color": "red"},
                                           children="""Associate Professor, Duke Biostatistic department"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Director professor 2018 Data+ project 8: Deep Learning for Single 
                                           Cell Analysis.Computational immunology (stochastic and spatial 
                                           models and simulations, T cell signaling, immune regulation) """),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Statistical methodology for immunological laboratory techniques 
                                           (flow cytometry, CFSE analysis, receptor-ligand binding and signaling 
                                           kinetics)"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Informatics of the immune system (reference 
                                                and application ontologies, meta-programming, 
                                                text mining and machine learning)"""),
                                    html.P(style={"margin-left": "8.66666666667%"},
                                           children="""Email: cliburn.chan@duke.edu"""),
                                ], className="six columns"),
                            ], className="row"),
                        ])
])

@app.callback(
    dash.dependencies.Output("main", "children"),
    [dash.dependencies.Input("url", "pathname")])
def update_main(pathname):
    if pathname == "/about":
        return about_page
    elif pathname == "/team":
        return team_page
    else:
        return home_page


@app.callback(
    dash.dependencies.Output("processing", "children"),
    [dash.dependencies.Input("upload-data", "filename"),
     dash.dependencies.Input("uploaded", "children")])
def update_process(filename, ch):
    if filename == None:
        return ""
    elif ch == None:
        return "Processing " + filename + ". Please be patient"
    else:
        return "Processing done!"



@app.callback(
    dash.dependencies.Output("uploaded", "children"),
    [dash.dependencies.Input("upload-data", "filename"),
     dash.dependencies.Input("upload-data", "contents")])
def update_output(filename, contents):
    """Save uploaded files and regenerate the file list."""
    if filename == None:
        files = "No files yet!"
    else:
        print(os.getcwd())
        save_file(filename, contents)
        csv_name = "./" + filename
        realOneClick(csv_name)
        files = filename
    return [html.Li(files)]



@app.callback(
    dash.dependencies.Output("table", "rows"),
    [dash.dependencies.Input("kmean-dropdown", "value"),
    dash.dependencies.Input("dimension-dropdown", "value"),
    dash.dependencies.Input("dataset-dropdown", "value"),
    dash.dependencies.Input("visualization-dropdown", "value")])
def update_table(value, dim_method, dataset, visualization):
    # load dataset
    filepath = "./data/" + dataset + "/" + dim_method + "/"

    # load data
    gene_tables = []
    if not visualization:
        for k_ in range(1, 9):
            gene_tables.append(loadTable(filepath + "geneTable_" + str(k_) + ".txt"))
    else:
        for k_ in range(1, 9):
            gene_tables.append(loadTable(filepath + "geneTable_" + str(k_) + "_scvis.txt"))

    # load genelist
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
     dash.dependencies.Input("dataset-dropdown", "value"),
     dash.dependencies.Input("visualization-dropdown", "value")])
def update_graph_2(value, dim_method, dataset, visualization):
    filepath = './data/' + dataset + "/" + dim_method + "/"

    # load
    if not visualization:
        filepath += "tsne.txt"
        tsne = load(filepath)
    else:
        filepath = './data/' + dataset + "/" + dim_method + '/scvis.tsv'
        scvis = loadTSV(filepath)
        tsne = (scvis[:, 1], scvis[:, 2])

    # load colormap
    color_mask = []
    if not visualization:
        for k_ in range(1, 9):
            color_mask.append(loadColorMask("./data/" + dataset + "/" + dim_method + "/" +
                                            "color_mask_" + str(k_) + ".txt"))
    else:
        for k_ in range(1, 9):
            color_mask.append(loadColorMask("./data/" + dataset + "/" + dim_method + "/" +
                                            "color_mask_" + str(k_) + "_scvis.txt"))

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
    dash.dependencies.Output("visualization-dropdown", "options"),
    [dash.dependencies.Input("dimension-dropdown", "value")])
def update_visualization_dropdown(dimension):
    if dimension == "none":
        return [{"label": "TSNE", "value": 0}]
    else:
        return [{"label": "TSNE", "value": 0}, {"label": "SCVIS", "value": 1}]


@app.callback(
    dash.dependencies.Output("graph-1", "figure"),
    [dash.dependencies.Input("visualization-dropdown", "value"),
     dash.dependencies.Input("dimension-dropdown", "value"),
     dash.dependencies.Input("gene-dropdown", "value"),
     dash.dependencies.Input("dataset-dropdown", "value")])
def update_graph1(visualization, dim_method, gene, dataset):
    # load
    if not visualization:
        filepath = './data/' + dataset + "/" + dim_method + '/tsne.txt'
        tsne = load(filepath)
    else:
        filepath = './data/' + dataset + "/" + dim_method + '/scvis.tsv'
        scvis = loadTSV(filepath)
        tsne = (scvis[:, 1], scvis[:, 2])


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
