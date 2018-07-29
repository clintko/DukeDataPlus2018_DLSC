import dash
import dash_core_components as dcc
import dash_html_components as html
from home1_backup import home1, load, loadColorMask, loadTable, loadList, update_table, update_graph_2, update_graph1
from Team import team
from About import about


pages = {"/home": home1, "/team": team, "/about": about}


app = dash.Dash()

app.layout = html.Div(style={"height": "200vh", "fontFamily": "Georgia"}, children=[
    # head
    # the head never change
    html.Div(style={'background-color': "#CEF0EF", "height": "10vh", "width": "100%"}, children=[
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/e/e1/Duke_Athletics_logo.svg', height="50vh",
                 width="50vh", style={"margin-top": "2vh", "margin-left": "3vh"}),
        html.Ul(style={"float": "right", "list-style": "none", "margin-right": "5vh"},
                children=[
            dcc.Location(id='url', refresh=False),
            dcc.Link(children=["About"], href="about", style={"font-size": "15px",
                                                              "display": "inline-block", "padding": "2vh"}),
            html.Br(),
            dcc.Link(children=["Home"], href="home", style={"font-size": "15px",
                                                            "display": "inline-block", "padding": "2vh"}),
            html.Br(),
            dcc.Link(children=["Team"], href="team", style={"font-size": "15px",
                                                            "display": "inline-block", "padding": "2vh"})
                ])
    ]),

    html.Div(id="page_content")
])


@app.callback(
    dash.dependencies.Output('page_content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def display_value(pathname):
    print(pathname)
    return pages[pathname].layout


if __name__ == "__main__":
    app.run_server()
