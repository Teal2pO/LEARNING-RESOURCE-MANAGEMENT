import pandas as pd
import csv
import ast

import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table, callback
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from datetime import datetime

from static_globals import *
from globals import *
from fns import *
from uifn import *

from dash.dependencies import ClientsideFunction
from dash.exceptions import PreventUpdate

chosenDomain = ''
chosenSubDomain = ''
chosenSubSubDomain = ''
chosenCategory = ''
domainNamesIDs = {dmn['name']: dmn['id']
                  for dmn in allCategories if dmn['parent'] == 0}
domainNames = [*domainNamesIDs]
domainNames.sort()


dash.register_page(__name__, path='/')

layout = html.Div([


    # html.H6("‣ View content",style={"font-weight": "bold"}),
    # html.P("Use following dropdown for quick filtering. If you just want to browse content categories use the pane below."),

    # html.P("Please pick domain"),
    # UI_dropdown("chosenDomain",domainNames),

    # html.P("#Pick sub domain from Dropdown list"),
    # UI_dropdown("chosenSubDomain",[]),

    # html.P("#Pick sub sub domain from Dropdown list"),
    # UI_dropdown("chosenSubSubDomain",[]),

    # html.Button('Proceed', id='btn-after_domain_select', n_clicks=0),


    # html.Div(id="output-after_domain_select"),

    html.Br(),
    html.Br(),
    # html.A(id="viewTop"),



    html.Div([
        # html.A(html.Button('Create/Update/Fork Content'),href="/{}-lrm/update-fork-create".format(appPrefixname),style={'margin':'5px'}),
        html.A(html.Button('Create/Update/Fork Content'), href="/teal-lrm/update-fork-create",
               style={'margin': '1px', 'padding-right': '1px'}),

        # html.A(html.Button('Update Content Version Information'),href="/{}-lrm/updategit".format(appPrefixname),style={'margin':'5px'}),
        html.A(html.Button('Update Content Version Information'),
               href="/teal-lrm/updategit", style={'margin': '1px'}),

        # html.A(html.Button('Program/Course/Classroom Create/Edit'),href="{}/{}-program-course".format(serverURL,appPrefixname),style={'margin':'5px'}),
        html.A(html.Button('Program/Course/Classroom Create/Edit'),
               href="{}/teal-program-course".format(serverURL), style={'margin': '1px'}),



    ], style={'display': 'inline-block', 'width': '85%'}),

    html.Div([
        html.A(html.Button('Login/Logout'),
               href="{}/teal-lrm/login".format(serverURL)),
    ], style={'text-align': 'right', 'width': '15%', 'display': 'inline-block'}),

    html.Br(),
    html.Br(),

    # html.Div(id="output-create-content",children=html.Iframe(id="myframe1",src='{}/{}_content'.format(serverURL,appPrefixname),style={"height": "1067px", "width": "100%"})),
    html.Div(id="output-iframe"),


], style={'margin': '15px'})


# ===========================Callbacks
# Display Iframe only if user logged in
@callback(
    Output('output-iframe', 'children'),
    Input('session1Type', 'data'),
)
def func(userEmail):
    print(userEmail)
    try:
        valid_email = check_email(userEmail)
    except:
        return html.Div([html.P('User not logged in!'), html.Img(src="assets/partner_map.png", style={'width': '100%', 'height': 'auto'})])

    if (valid_email == True):
        div = html.Div([
            html.Iframe(id="myframe1", src='{}/{}_content'.format(serverURL,
                        appPrefixname), style={"height": "1067px", "width": "100%"}),
        ])
    else:
        div = html.Div([
            html.P('Please login to continue'),
        ])

    return div


# choose domain
@callback(
    Output('chosenSubDomain', 'options'),
    Input('chosenDomain', 'value'),
    prevent_initial_call=True,
)
def func(chosenDomain):
    if (chosenDomain != None):
        subDomainNamesIDs = {dmn['name']: dmn['id']
                             for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain]}
        subDomainNames = [*subDomainNamesIDs]
        subDomainNames.sort()
        if len(subDomainNames) != 0:
            options1 = subDomainNames
        else:
            options1 = []

        return options1
    else:
        return []

# choose sub domain


@callback(
    Output('chosenSubSubDomain', 'options'),
    Input('chosenSubDomain', 'value'),
    Input('chosenDomain', 'value'),
    prevent_initial_call=True,
)
def func(chosenSubDomain, chosenDomain):
    if (chosenSubDomain != None and chosenDomain != None):

        try:
            subDomainNamesIDs = {dmn['name']: dmn['id']
                                 for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain]}
            subDomainNames = [*subDomainNamesIDs]
            subDomainNames.sort()
            print(subDomainNames)
            if len(subDomainNames) != 0:
                subSubDomainNamesIDs = {
                    dmn['name']: dmn['id'] for dmn in allCategories if dmn['parent'] == subDomainNamesIDs[chosenSubDomain]}
                subSubDomainNames = [*subSubDomainNamesIDs]
                subSubDomainNames.sort()
                if len(subSubDomainNames) != 0:
                    options1 = subSubDomainNames

                else:
                    options1 = []
            else:
                options1 = []
        except:
            options1 = []

        return options1
    else:
        return []

# Click proceed after domain/subdomain/subsubdomain selection


@callback(
    Output('output-after_domain_select', 'children'),
    # Output('email', 'data'),
    Input('btn-after_domain_select', 'n_clicks'),
    State('chosenDomain', 'value'),
    State('chosenSubDomain', 'value'),
    State('chosenSubSubDomain', 'value'),
    # State('email', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenDomain, chosenSubDomain, chosenSubSubDomain):
    print(chosenDomain)
    print(chosenSubDomain)
    print(chosenSubSubDomain)
    # print(email)
    if (chosenDomain != None):
        if (chosenSubDomain == None and chosenSubSubDomain != None):
            div = html.Div([
                html.P("Please pick sub domain first"),
            ])

        else:
            text1 = chosenDomain
            if (chosenSubDomain != None and chosenSubSubDomain == None):
                text1 = chosenSubDomain
            elif (chosenSubDomain != None and chosenSubSubDomain != None):
                text1 = chosenSubSubDomain

            div = html.Div([
                html.Br(),
                # html.P(email),
                html.P("Selected Category Name/Competancy"),
                dcc.Input(id="categoryName", value=text1,
                          type="text", readOnly=True),

                html.Br(),

                html.Button(
                    'Proceed', id='btn-proceed-after-domain-select', n_clicks=0),
                html.Div(id="output-create-content-msg"),
            ])

    else:
        div = html.Div([
            html.P("Please pick domain first"),
        ])

    return div

# Check Category Name/Competancy then click proceed


@callback(
    Output('output-create-content-msg', 'children'),
    Input('btn-proceed-after-domain-select', 'n_clicks'),
    State('categoryName', 'value'),
    # State('email', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, categoryName):
    if (n_clicks != 0):
        if (categoryName != None):

            chosenCategory = categoryName
            chosenCategoryID = call('core_course_get_categories ', criteria=[
                                    {'key': 'name', 'value': chosenCategory}])[0]['id']
            categoryContentListPDF = pd.read_sql(
                'SELECT id, category, shortname, fullname FROM mdl_course WHERE category={}'.format(chosenCategoryID), engine)
            categoryContentList = categoryContentListPDF['shortname'].to_list()
            categoryContentList.sort()

            div2 = html.Div([
                html.Br(),
                # html.P(email),
                html.P("Select content by short name"),
                UI_dropdown("chosenContentShortname", categoryContentList),
                # html.Button('Show content', id='btn-show_content', n_clicks=0),
                html.A(html.Button('Show content', id='btn-show_content',
                       n_clicks=0), href='#viewTop'),
                html.Div(id="output-show_content_msg"),
            ]),

        else:
            div2 = html.Div("Please fill all fields")

        return div2

    else:
        raise PreventUpdate

# Click show content button


@callback(
    Output('output-create-content', 'children'),
    Output('output-show_content_msg', 'children'),
    Input('btn-show_content', 'n_clicks'),
    State('chosenContentShortname', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenContentShortname):
    if (n_clicks != 0):

        chosenContentID = call('core_course_search_courses', criterianame='search',
                               criteriavalue=chosenContentShortname)['courses'][0]['id']
        # contentURL=siteURL+'/course/view.php?id={}'.format(chosenContentID)
        contentURL = call('core_course_get_contents', courseid=chosenContentID)[
            0]['modules'][0]['url']
        contentURL = contentURL.replace("https://127.0.0.1", serverURL)

        msg_show = "Content "+chosenContentShortname+" displayed below."

        div = html.Div([
            html.Iframe(src=contentURL, style={
                        "height": "1067px", "width": "100%"}),
            html.P(msg_show),
        ]),

        div2 = html.Div([
            html.P(msg_show),
        ]),

        return div, div2
    else:
        raise PreventUpdate
