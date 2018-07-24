import dash
import dash_html_components as html

team = dash.Dash()


# Composing the website
team.layout = html.Div(style={"height": "200vh", "font-family": "Georgia", "border": "black", "border": "solid"}, children=[


    # introduction of our team
    html.H2('Our Team:', style={"text-align": "center", "border": "solid"}),
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
                html.P(style={"margin-left": "8.66666666667%", "color": "red"}, children="""Duke 2021 Undergraduate, 
                Mathematics and Statistic Major"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""One of the developers of the website,
                contributed to 'None' and PCA dimension reduction methods pipeline,
                and SCVIS visualization machine learning pipeline construction"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Email: ziyang.ding@duke.edu"""),
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
                html.P(style={"margin-left": "8.66666666667%", "color": "red"}, children="""Duke 2021 Undergraduate, 
                            ECE and Computer Science Major"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""One of the developers of the website,
                            contributed to Autoencoder and PCA dimension reduction methods pipeline,
                            and tSNE visualization machine learning pipeline construction"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Email: chaofan.tao@duke.edu"""),
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
                html.P(style={"margin-left": "8.66666666667%", "color": "red"}, children="""Duke master program
                Biostatistics department"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Project manager of 2018 Data+ project 8:
                Deep Learning for Single Cell Analysis. Contributed to coordinating and managing project team in
                academic research, communicating with Tata's Lab, and connecting project team with professors"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Email: 填写填写填写@duke.edu"""),
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
                html.P(style={"margin-left": "8.66666666667%", "color": "red"}, children="""Associate Professor, Duke 
                Biostatistic department"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Director professor 2018 Data+ project 8:
                            Deep Learning for Single Cell Analysis.Computational immunology (stochastic and spatial 
                            models and simulations, T cell signaling, immune regulation) """),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Statistical methodology for immunological 
                            laboratory techniques (flow cytometry, CFSE analysis, receptor-ligand binding and 
                            signaling kinetics)"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Informatics of the immune system (reference 
                            and application ontologies, meta-programming, text mining and machine learning)"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Phone: (919) 668-2459"""),
                html.P(style={"margin-left": "8.66666666667%"}, children="""Email: 填写填写填写@duke.edu"""),
            ], className="six columns"),
        ], className="row"),
    ])
])

# css style repository
team.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == "__main__":
    team.run_server()
