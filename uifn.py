from globals import *
import base64
import io

from dash import dash_table
from dash import dcc, callback_context
from dash import html
import dash_daq as daq
from collections import OrderedDict
import dash_bootstrap_components as dbc

import re


def UI_orderedList(itm_list):
    div = html.Div([
        html.Ol(children=[html.Li(i) for i in itm_list])
    ])
    return div


# PDF to data table
def UI_PDFtoTable(data_df):
    div = dash_table.DataTable(
        data=data_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in data_df.columns],
        style_cell={'textAlign': 'left',
                    'height': 'auto', 'whiteSpace': 'normal'},
        style_header={
            'backgroundColor': '#8febb5',
            'fontWeight': 'bold'
        },
        # page_size=2,
        style_table={'height': '300px', 'overflowY': 'auto'},  # enable scroll
        # style_table={'height': '300px'},#enable scroll
        # style_table={
        #     'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
        #     'minWidth': '900px', 'width': '900px', 'maxWidth': '900px'
        # },
        # fixed_rows={'headers': True}
    )
    return div


def UI_dropdown(dropdown_id, option_list, styleDict={}, defaultValue=None):
    div = dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        value=defaultValue,
        style=styleDict)

    return div


def UI_multidropdown(dropdown_id, option_list, styleDict={}):
    div = dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        style=styleDict,
        multi=True,
        value=option_list,
    )

    return div


def UI_multidropdown_empty(dropdown_id, option_list, styleDict={}):
    div = dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        style=styleDict,
        multi=True,
        # value=option_list,
    )

    return div


# template download
# html.Div([
#     html.A('Download template',id='btn-template1',style={'font-style':'italic','textAlign': 'center'}),
#     dcc.Download(id='download-template1')
# ]),

def UI_fileUpload(upload_id):
    # upload file
    div = html.Div([
        html.P('Please upload csv file below to start',
               style={'font-style': 'italic'}),
        dcc.Upload(
            id=upload_id,
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={
                'width': '98%',
                'height': '80px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
    ])
    return div

# pdf to CSV


def UI_fileDownload(button_id, download_id, user_msg):
    div = html.Div([
        html.A(user_msg, id=button_id, style={
               'font-style': 'italic', 'textAlign': 'left'}),
        dcc.Download(id=download_id)
    ])
    return div
# @app.callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        df = pd.DataFrame()

    return df

# DataTable with Per-Row Dropdowns
# def UI_table_dropdown(table_id,data):


def UI_table_dropdown(table_id, data):
    # table_id='test'
    # data={'Cname1':['1','2','3'],'Cname2':['11','22','33']}
    column_name_list = data.keys()

    L = []
    for name in data:
        option_list = data[name]
        dict = {'if': {'column_id': 'Value', 'filter_query': '{Column_name} eq '+name},
                'options': [{'label': str(i), 'value': str(i)}for i in option_list]}
        L.append(dict)

    df_per_row_dropdown = pd.DataFrame(OrderedDict([
        ('Column_name', column_name_list),
        # ('Value', ['213', '3213', '1232']),
    ]))

    div = html.Div([

        dash_table.DataTable(
            id=table_id,
            data=df_per_row_dropdown.to_dict('records'),
            columns=[
                {'id': 'Column_name', 'name': 'Column name'},
                {'id': 'Value', 'name': 'Value', 'presentation': 'dropdown'},
            ],
            editable=True,
            dropdown_conditional=L
        ),
    ])

    return div


# User Inputs for defining the course information
# UI_ILOx(1,ILOx_verb,ILOx_txt,ILOx_Cval)
def UI_ILOx(ILO_num, ILOx_verb, ILOx_txt, ILOx_Cval):
    # ILO_num=1

    ILO_name = 'ILO-'+str(ILO_num)
    solo_level_dropdown_id = 'solo_level_ILO' + \
        str(ILO_num)  # Ex: solo_level_ILO1
    verb_dropdown_id = 'verb_ILO'+str(ILO_num)  # Ex:verb_ILO1
    textbox_id = 'text_ILO'+str(ILO_num)  # Ex:text_ILO1
    credit_slider_id = 'creditSlider'+str(ILO_num)  # Ex:creditSlider1

    # ILO1
    div = html.Div([
        html.Div([
            html.H6("ILO", style={'font-weight': 'bold',
                    'textAlign': 'left', 'marginLeft': 20}),
            html.Div([  # left side - solo level and action verb pick
                html.P(['Pick solo level', UI_toolTipIcon("soloLevel")],
                       style={'font-weight': 'bold', 'textAlign': 'left'}),
                UI_toolTip("soloLevel", "Use this menu to select the SOLO level category to find the correct \"Action verb\". If you already selected the correct action verb no need to select this again."),
                dcc.Dropdown(
                    id=solo_level_dropdown_id,
                    options=[
                        {'label': 'SOLO-01-UNISTRUCTURAL',
                         'value': 'SOLO_01_UNISTRUCTURAL'},
                        {'label': 'SOLO-02-MULTISTRUCTURAL',
                         'value': 'SOLO_02_MULTISTRUCTURAL'},
                        {'label': 'SOLO-03-RELATIONAL',
                            'value': 'SOLO_03_RELATIONAL'},
                        {'label': 'SOLO-04-EXTENDED ABSTRACT',
                         'value': 'SOLO_04_EXTENDED ABSTRACT'},
                    ], style={'width': '95%'}),
                html.Br(),
                html.P(['to do (pick action verb)', UI_toolTipIcon("actionVerb")], style={
                       'font-weight': 'bold', 'textAlign': 'left'}),
                UI_toolTip(
                    "actionVerb", "Pick the action verb that you want to associate with the statement."),
                # html.Div(id='app-output-verbs-ILO1'),#verb selection drop down appear here


                dcc.Dropdown(  # dropdown with action verbs
                    id=verb_dropdown_id,
                    # options=[ILOx_verb],
                    options=[] if ILOx_verb == None else [ILOx_verb],
                    value=ILOx_verb,
                    style={'width': '95%'}),

                html.Br(),
                html.P(['Select expected number of hours', UI_toolTipIcon("noOfHrs")], style={
                       'font-weight': 'bold', 'textAlign': 'left'}),
                UI_toolTip(
                    "noOfHrs", "No of hours will contribute to the credits."),
                html.Br(),
                html.Br(),
                daq.Slider(
                    id=credit_slider_id,
                    min=0.5,
                    max=20,
                    # value=0.5,
                    value=ILOx_Cval,
                    # handleLabel={"showCurrentValue": True,"label": "VALUE"},
                    handleLabel={"showCurrentValue": True,
                                 "label": "Hours", "color": "black"},
                    step=0.5,
                ),

            ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': 20}),

            html.Div([  # right side of the div
                html.P(['what? (statement)', UI_toolTipIcon("statement")], style={
                       'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20}),
                UI_toolTip(
                    "statement", "ILO will be 'action verb' + 'statement' \n Ex: describe key concepts of physics using the language of mathematics."),
                dcc.Textarea(
                    id=textbox_id,
                    value=ILOx_txt,
                    style={'width': '100%', 'height': 240, 'marginLeft': 20},
                ),
            ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),








        ], style={'height': 350, 'borderWidth': '1px', 'borderRadius': '10px', }),
        # 'borderStyle': 'dashed'

        html.Br()
    ])

    return div


def div_skillSelectionCourseCreation(programDomains, CAH3_skill_txt, num):
    # course skill selection for course creation
    div = html.Div([
        # html.H6('Search by course skills',style={'textAlign': 'center','font-weight': 'bold'}),
        html.Div([
            html.P('Domain', style={
                   'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20, "height": "34px"}),
            html.P('Sub domain', style={
                   'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20, "height": "34px"}),
            html.P('CAH3 skill classification', style={
                   'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20, "height": "34px"}),
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            UI_dropdown('program_domainCC'+str(num), programDomains),
            UI_dropdown('program_subdomainCC'+str(num), []),
            UI_dropdown('program_skillCC'+str(num),
                        [CAH3_skill_txt], defaultValue=CAH3_skill_txt),
        ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    ])
    return div


# Dash bootstrap for tool tips

def UI_toolTipIcon(idOfIcon):
    div = html.Sup(html.A(
        html.P("🛈" ,style={"display": "inline" ,"color" :"#007bff"}) ,id=idOfIcon))
    return div


def UI_toolTip(idOfIcon, textTip):
    div = dbc.Tooltip(
        html.Div([
            html.H6(textTip),
        ]),
        target=idOfIcon,
        placement="auto-start",
        # trigger="click"
        trigger="legacy"
    )

    return div
