from dash import Dash, html, dcc
import dash
from dash import callback
from dash.dependencies import Input, Output, State
from static_globals import *
import dash_bootstrap_components as dbc

# app = dash.Dash(__name__,suppress_callback_exceptions=True,use_pages=True,url_base_pathname='/{}-lrm/'.format(appPrefixname))
app = dash.Dash(__name__, suppress_callback_exceptions=True, use_pages=True,
                url_base_pathname='/teal-lrm/', external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__,suppress_callback_exceptions=True,use_pages=True,url_base_pathname='/teal-lrm/')
app.title = '{}-lrm'.format(appPrefixNAME)
server = app.server

# Following are the static content in the main application throughout the app. Dynamic content are served via pages.
app.layout = html.Div([
    # html.P("Development in progress",style={'color':'red'}),
    html.Div([  # logos and site title
        # Logo at the left
        html.Div([
                # static access to asset folder - deosn't change with page navaigate
                html.Img(src=app.get_asset_url('erasmus_logo.png'),
                         style={'height': '50%', 'width': '50%'}),
                # html.Img(src=('assets/erasmus_logo.png'),style={'height':'50%', 'width':'50%'}),
        ], style={'width': '33%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'left'}),

        # Title
        html.Div([
            # html.Img(src=('assets/logo.png'),style={'height':'50%', 'width':'50%'}),
            html.H4("Learning Resource Management",
                    style={"fontWeight": "bold"}),
        ], style={'width': '33%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),

        # Logo at the right
        html.Div([
            html.Img(src=app.get_asset_url('teal_logo.jpeg'),
                     style={'height': '50%', 'width': '50%'}),
        ], style={'width': '33%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'right'}),
    ]),

    dash.page_container,  # pages load here (by defalt / loaded first)

    # for storing user email
    dcc.Store(id='session1Type', storage_type='local')
])


if __name__ == '__main__':
    app.run_server(debug=False, port=5601)
