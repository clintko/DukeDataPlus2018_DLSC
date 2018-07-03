import dash
import dash_core_components as dcc
import dash_html_components as html
import base64


# load images
logo = "./images/Duke_logo.webp"

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='http://logonoid.com/images/vanguard-logo.png', height='40', width='160')
        ], className="ten columns padded")]
    )
    return logo

def get_menu():
    menu = html.Div([

        dcc.Link('Overview   ', href='/overview', className="tab first"),

        dcc.Link('Price Performance   ', href='/price-performance', className="tab"),

        dcc.Link('Portfolio & Management   ', href='/portfolio-management', className="tab"),

        dcc.Link('Fees & Minimums   ', href='/fees', className="tab"),

        dcc.Link('Distributions   ', href='/distributions', className="tab"),

        dcc.Link('News & Reviews   ', href='/news-and-reviews', className="tab")

    ], className="row ")
    return menu

app = dash.Dash()

app.layout = html.Div(style={"height": "200vh", "fontFamily": "Georgia"}, children=[
    # head
    html.Div(style={'background-color': "#CEF0EF", "height": "10vh", "width": "100%"}, children=[
        html.Img(src="./images/Duke_logo.webp", height="50vh", width="50vh"),
        html.Ul(style={"float": "right", "list-style": "none", "margin-right": "5vh"},
                children=[
            html.Li(children=["About"], style={"font-size": "15px", "display": "inline-block", "padding": "2vh"}),
            html.Li(children=["Home"], style={"font-size": "15px", "display": "inline-block", "padding": "2vh"}),
            html.Li(children=["Team"], style={"font-size": "15px", "display": "inline-block", "padding": "2vh"})
        ]),

    ])











])
if __name__ == "__main__":
    app.run_server()