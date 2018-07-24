import dash
import dash_html_components as html

about = dash.Dash()


# Composing the website
about.layout = html.Div(style={"height": "200vh", "font-family": "Georgia"}, children=[
    html.Div(style={"height": "20px"}),

    # title single cell analysis
    html.Div(style={"margin-top":"2vh", "align": "center"}, children=[
        html.H1(style={"text-align": "center", "vertical-align": "middle"}, children=["Deep Learning for Single Cell Analysis"])
    ]),

    # empty placeholder
    html.Div(style={"height": "20px"}),

    # first paragraph for background
    html.Div(style={"width": "70%", "margin-left": "auto", "margin-right": "auto", "font-size": "18px"},
             children=["In the field of cellular biology, single cell analysis serves as an important role in "
                       "understanding genomics and their behaviors from the microscopic level. As technology "
                       "has improved the efficacy of obtaining quantified data from single cell’s mRNA expression, "
                       "single cell analysis found its new basis upon statistical learning methods, which incorporates "
                       "machine learning and deep learning methods. \n"]),

    html.Div(style={"height": "20px"}),

    html.Div(style={"width": "80%", "margin-left":"auto", "margin-right": "auto"}, className="row", children=[
        html.Div(className="five columns", children=[
            html.Img(src='https://www.rna-seqblog.com/wp-content/uploads/2016/12/heatmap-983x1024.gif',
                         style={"margin-top": "1vh", "height": "auto", "width": "100%"})
        ]),

        html.Div(className="six columns", style={"margin-left": "10%", "margin-right": "auto"},
                 children=[
                 html.Div(style={"margin-left": "10%", "margin-right": "auto", "font-size": "18px"},
                          children=["Single cell sequencing data always incorporate very high dimensional data. "
                                    "Furthermore, the considering the number of different genes a genome can "
                                    "possess, usually the number of observations comparing to the number of genes "
                                    "are too small, leaving the sequencing data matrix very sparse. Therefore, "
                                    "data cleaning is an imperative and crucial part of conducting data analysis "
                                    "for single cell analysis.  \n"]),

                 html.Div(style={"height": "2vh"}),

                 html.Div(style={"margin-left": "10%", "margin-right": "auto", "font-size": "18px"},
                          children=["Furthermore, single cell analysis involves dimension reduction, unsupervised "
                                    "clustering algorithms, and high dimensional data visualization procedure. "
                                    "These machine learning algorithms have been fully developed and ready to use: "
                                    "the algorithms packages need and are always convenient to use… \n"])
                     ])
            ]),

    html.Div(style={"height": "40px"}),

    html.Div(style={"width": "80%", "margin-left": "auto", "margin-right": "auto"}, className="row", children=[

        html.Div(className="six columns", children=[
                     html.Div(
                         style={"margin-left": "auto", "margin-right": "10%", "font-size": "18px"},
                         children=["Currently, even there are many single cell analysis tools and packages. Scanpy and "
                                   "Seurat have all contributed great deal in integrating the entire single "
                                   "cell analysis pipeline and tutor researchers how to properly use the packages. "
                                   "Even so, there’re still space to make the entire process easier and handier.  \n"]),

                     html.Div(style={"height": "2vh"}),

                     html.Div(
                         style={"margin-left": "auto", "margin-right": "10%", "font-size": "18px"},
                         children=["By using Plotly dash, we integrate possibly 6 different pipelines together, and "
                                   "make it user friendly. This website application doesn’t require any knowledge for "
                                   "coding and is ready to give out valuable information of the dataset. Users may "
                                   "utilize the website as a tool for research, and hopefully excavate new cell types."])
                 ]),

        html.Div(className="five columns", style={"margin-left": "10%"}, children=[
            html.Img(src='https://www.helsinki.fi/sites/default/files/thumbnails/image/tsne_filtered.jpg',
                     style={"margin-top": "1vh", "height": "auto", "width": "100%"})
        ]),
    ]),
])

# css style repository
about.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == "__main__":
    about.run_server()
