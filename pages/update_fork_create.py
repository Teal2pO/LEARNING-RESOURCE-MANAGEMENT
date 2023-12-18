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

import re
import json
# UI Styles
style_err_msg = {'color': 'red'}


chosenDomain_cr_update = ''
chosenSubDomain_cr_update = ''
chosenSubSubDomain_cr_update = ''
chosenCategory = ''
domainNamesIDs = {dmn['name']: dmn['id']
                  for dmn in allCategories if dmn['parent'] == 0}
domainNames = [*domainNamesIDs]
domainNames.sort()


dash.register_page(__name__, path='/update-fork-create')


layout = html.Div([
    html.Button('Proceed to update fork create',
                id='emailConfirm-update_fork_create-btn', n_clicks=0),
    # dcc.Link(html.Button("View/Edit content"), href="/{}-lrm".format(appPrefixname), refresh=True),
    dcc.Link(html.Button("Home"), href="/teal-lrm/", refresh=True),

    html.Div(id='contentAfterEmail-update_fork_create-output'),


    html.Div(id='dummy-div_update', style={'display': 'none'}),






    dcc.Loading(id="loading_update-loading", type="dot", fullscreen=True,
                children=html.Div(id="loading_update-output",
                                  style={'display': 'none'})
                ),

    dcc.Loading(id="loading_fork-loading", type="dot", fullscreen=True,
                children=html.Div(id="loading_fork-output",
                                  style={'display': 'none'})
                ),

    dcc.Loading(id="loading_create-loading", type="dot", fullscreen=True,
                children=html.Div(id="loading_create-output",
                                  style={'display': 'none'})
                ),

    # dcc.Store(id='session1Type',storage_type='local'),#user email saved into this variable- no need to define here since defined in main page

], style={'margin': '15px'})


# ===========================Callbacks
# email check when user click proceed
@callback(
    Output('contentAfterEmail-update_fork_create-output', 'children'),
    Input('emailConfirm-update_fork_create-btn', 'n_clicks'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, userEmail):
    print(userEmail)
    try:
        valid_email = check_email(userEmail)
    except:
        return html.P('User not logged in!')

    if (valid_email == True):
        msg = 'User: '+userEmail

        div = html.Div([
            html.P(msg),

            dcc.RadioItems(
                id="choose_create_mode_radio",
                options=[
                    {'label': 'Update', 'value': 'Update'},
                    {'label': 'Fork', 'value': 'Fork'},
                    {'label': 'Create', 'value': 'Create'},
                    {'label': 'Delete', 'value': 'Delete'},
                ],
                value='Update',
                inline=True,
                labelStyle={'display': 'block', 'margin-left': '5px'},
                style={'text-align': 'center'},
            ),

            html.Div(id='choose_create_mode_radio-output'),
        ])

    else:
        div = html.P('Invalid user!')

    return div


# user selects choose_create_mode_radio
@callback(
    Output('choose_create_mode_radio-output', 'children'),
    Input('choose_create_mode_radio', 'value'),
)
def func(value):
    if (value == 'Update'):
        div = html.Div([

            html.H2([
                html.H2("‣ Update learning resource", style={
                        "font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("lrmUpdate"),
                html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                       href="https://drive.google.com/file/d/1DeBPAZKs3Cdmz8tS57ZAql_s_UqczQDh/view?usp=sharing", target='_blank', style={"text-decoration": "none"}),
            ]),

            UI_toolTip("lrmUpdate", "For already created content by you, you're allowed to update content name and the ILO using this section. Please note updating short name is not allowed."),


            html.Div(id="output-create-content-cr_update"),

            html.P(["Please pick domain", UI_toolTipIcon("lrmUpdateDomain")]),
            UI_toolTip(
                "lrmUpdateDomain", "To find the content that you want to update, first filter your content using CAH3 classification."),

            UI_dropdown("chosenDomain_cr_update", domainNames,
                        {"margin": "5px", "width": "75%"}),

            html.P(["Pick sub domain from Dropdown list"]),

            UI_dropdown("chosenSubDomain_cr_update", [], {
                        "margin": "5px", "width": "75%"}),

            html.P("Pick sub sub domain from Dropdown list"),
            UI_dropdown("chosenSubSubDomain_cr_update", [],
                        {"margin": "5px", "width": "75%"}),

            html.Br(),
            html.Button(
                'Proceed', id='btn-after_domain_select_cr_update', n_clicks=0),


            html.Div(id="output-after_domain_select_cr_update"),




        ])

    elif (value == 'Fork'):
        div = html.Div([

            html.H2([
                html.H2("‣ Fork learning resource", style={
                        "font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("lrmFork"),
                html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                       href="https://drive.google.com/file/d/1tSdIat1WGaZ8Q2VyEly-c6uTjnvA86oQ/view?usp=sharing", target='_blank', style={"text-decoration": "none"}),
            ]),


            UI_toolTip("lrmFork", "If you want to create a new content using already available content prepared by someone else, you have to first fork it using this section."),



            html.Div(id="output-create-content-cr_fork"),

            html.P(["Please pick domain", UI_toolTipIcon("lrmForkDomain")]),
            UI_toolTip(
                "lrmForkDomain", "Use CAH3 classification filters to find the content that you want to fork."),


            UI_dropdown("chosenDomain_cr_fork", domainNames,
                        {"margin": "5px", "width": "75%"}),

            html.P("Pick sub domain from Dropdown list"),
            UI_dropdown("chosenSubDomain_cr_fork", [], {
                        "margin": "5px", "width": "75%"}),

            html.P("Pick sub sub domain from Dropdown list"),
            UI_dropdown("chosenSubSubDomain_cr_fork", [], {
                        "margin": "5px", "width": "75%"}),

            html.Br(),
            html.Button(
                'Proceed', id='btn-after_domain_select_cr_fork', n_clicks=0),


            html.Div(id="output-after_domain_select_cr_fork"),



        ])

    elif (value == 'Create'):
        div = html.Div([

            html.H2([
                html.H2("‣ Create learning resource", style={
                        "font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("lrmCreate"),
                html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                       href="https://drive.google.com/file/d/1yihZE5Fk-FYRnF8KC5YwimCAHOZJGji9/view?usp=sharing", target='_blank', style={"text-decoration": "none"}),
            ]),


            UI_toolTip("lrmCreate", "Use this section to create new content."),
            html.Div(id="output-create-content-cr_create"),


            html.P(["Please pick domain", UI_toolTipIcon("lrmCreateDomain")]),
            UI_toolTip(
                "lrmCreateDomain", "Set CAH3 classification for the new content using the drop-down menus."),

            UI_dropdown("chosenDomain_cr_create", domainNames,
                        {"margin": "5px", "width": "75%"}),

            html.P("Pick sub domain from Dropdown list"),
            UI_dropdown("chosenSubDomain_cr_create", [], {
                        "margin": "5px", "width": "75%"}),

            html.P("Pick sub sub domain from Dropdown list"),
            UI_dropdown("chosenSubSubDomain_cr_create", [],
                        {"margin": "5px", "width": "75%"}),

            html.Br(),
            html.Button(
                'Proceed', id='btn-after_domain_select_cr_create', n_clicks=0),


            html.Div(id="output-after_domain_select_cr_create"),

        ])

    elif (value == 'Delete'):
        div = html.Div([

            html.H2([
                html.H2("‣ Delete learning resource", style={
                        "font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("lrmDelete"),
            ]),
            UI_toolTip(
                "lrmDelete", "Use this section to delete content. Only the content manager can delete content."),
            html.Iframe(id="myframe1", src='{}/{}'.format(serverURL,
                        "teal_content/course/management.php"), style={"height": "1067px", "width": "100%"}),

        ])

    return div


# ======================
# Section 1 : Update
# ======================


# choose domain
@callback(
    Output('chosenSubDomain_cr_update', 'options'),
    Input('chosenDomain_cr_update', 'value'),
    prevent_initial_call=True,
)
def func(chosenDomain_cr_update):
    if (chosenDomain_cr_update != None):
        subDomainNamesIDs = {dmn['name']: dmn['id']
                             for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_update]}
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
    Output('chosenSubSubDomain_cr_update', 'options'),
    Input('chosenSubDomain_cr_update', 'value'),
    Input('chosenDomain_cr_update', 'value'),
    prevent_initial_call=True,
)
def func(chosenSubDomain_cr_update, chosenDomain_cr_update):
    if (chosenSubDomain_cr_update != None and chosenDomain_cr_update != None):

        try:
            subDomainNamesIDs = {dmn['name']: dmn['id']
                                 for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_update]}
            subDomainNames = [*subDomainNamesIDs]
            subDomainNames.sort()
            print(subDomainNames)
            if len(subDomainNames) != 0:
                subSubDomainNamesIDs = {
                    dmn['name']: dmn['id'] for dmn in allCategories if dmn['parent'] == subDomainNamesIDs[chosenSubDomain_cr_update]}
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
    Output('output-after_domain_select_cr_update', 'children'),
    Input('btn-after_domain_select_cr_update', 'n_clicks'),
    State('chosenDomain_cr_update', 'value'),
    State('chosenSubDomain_cr_update', 'value'),
    State('chosenSubSubDomain_cr_update', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenDomain, chosenSubDomain, chosenSubSubDomain):

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
                html.P("Selected Category Name/Competancy"),

                html.Div([
                    html.Div([
                        dcc.Input(id="categoryName_cr_update", value=text1, type="text", readOnly=True, style={
                                  "margin": "5px", "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                    ], style={"width": "60%", "display": "inline-block", 'verticalAlign': 'top'}),
                    html.Div([
                        html.Button('Confirm', id='btn-proceed-after-domain-select_cr_update',
                                    n_clicks=0, style={"margin": "1%"}),
                    ], style={"width": "40%", "display": "inline-block", 'verticalAlign': 'top'}),
                ]),





                html.Div(id="boutput-create-content-msg_cr_update"),
            ])

    else:
        div = html.Div([
            html.P("Please pick domain first"),
        ])

    return div


# Check Category Name/Competancy then click confirm
@callback(
    Output('boutput-create-content-msg_cr_update', 'children'),
    Input('btn-proceed-after-domain-select_cr_update', 'n_clicks'),
    State('categoryName_cr_update', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, categoryName):
    if (n_clicks != 0):
        if (categoryName != None):

            chosenCategory = categoryName
            chosenCategoryID = call(webserviceAccessParamsContent, 'core_course_get_categories ', criteria=[
                                    {'key': 'name', 'value': chosenCategory}])[0]['id']

            categoryContentListPDF = pd.read_sql(
                'SELECT id, category, shortname, fullname FROM mdl_course WHERE category={}'.format(chosenCategoryID), engineContent)

            categoryContentList = categoryContentListPDF['shortname'].to_list()
            categoryContentList.sort()

            div2 = html.Div([
                html.Br(),

                html.P(["Existing content listed by short name",
                       UI_toolTipIcon("lrmUpdateShortname")]),
                UI_toolTip(
                    "lrmUpdateShortname", "Pick shortname for your content only. You can only update the content created by yourself."),

                html.Div([
                    html.Div([
                        UI_dropdown("chosenContentShortname_cr_update",
                                    categoryContentList, {"margin": "5px"}),
                    ], style={"width": "60%", "display": "inline-block", 'verticalAlign': 'top'}),
                    html.Div([
                        html.Button('Proceed', id='btn-go_to_content_creation_update',
                                    n_clicks=0, style={"margin": "1%"}),
                    ], style={"width": "40%", "display": "inline-block", 'verticalAlign': 'top'}),
                ]),


                html.Div(id="output-go_to_content_creation_update"),
            ]),

        else:
            div2 = html.Div("Please fill all fields")

        return div2

    else:
        raise PreventUpdate

# proceed after Existing content listed by short name select


@callback(
    Output('output-go_to_content_creation_update', 'children'),
    Input('btn-go_to_content_creation_update', 'n_clicks'),
    State('chosenDomain_cr_update', 'value'),
    State('chosenSubDomain_cr_update', 'value'),
    State('chosenSubSubDomain_cr_update', 'value'),
    State('categoryName_cr_update', 'value'),
    State('chosenContentShortname_cr_update', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func1(n_clicks, chosenDomain_cr_update, chosenSubDomain_cr_update, chosenSubSubDomain_cr_update, categoryName_cr_update, chosenContentShortname_cr_update, email):

    if (chosenContentShortname_cr_update != None):
        if (chosenSubDomain_cr_update == None and chosenSubSubDomain_cr_update != None):
            div = html.Div([
                html.P("Please pick sub domain first"),
            ])

        else:
            text1 = chosenDomain_cr_update
            if (chosenSubDomain_cr_update != None and chosenSubSubDomain_cr_update == None):
                text1 = chosenSubDomain_cr_update
            elif (chosenSubDomain_cr_update != None and chosenSubSubDomain_cr_update != None):
                text1 = chosenSubSubDomain_cr_update

            existingContent = call(webserviceAccessParamsContent, 'core_course_search_courses',
                                   criterianame='search', criteriavalue=chosenContentShortname_cr_update)['courses']
            chosenContentInfoDict = [
                crs for crs in existingContent if crs['shortname'] == chosenContentShortname_cr_update][0]
            chosenContentID = chosenContentInfoDict['id']
            chosenContentInfo = call(webserviceAccessParamsContent, 'core_course_get_courses', options={
                                     'ids': [chosenContentID]})[0]

            customFlds = {fld['shortname']: fld['valueraw']
                          for fld in chosenContentInfoDict['customfields']}

            print(chosenContentInfoDict)
            ilo_verb = customFlds['ilo'].split('#')[-2]
            ilo_text = customFlds['ilo'].split('#')[-1].strip()

            div = html.Div([
                html.Br(),

                html.Div([
                    html.Div([
                        html.P("Category Name/Competancy",
                               style={"height": "35px"}),
                        html.P("Content Short Name", style={"height": "35px"}),
                        html.P("Author", style={"height": "35px"}),
                        html.P(["Content Name", UI_toolTipIcon(
                            "lrmUpdateContentName")], style={"height": "35px"}),
                        UI_toolTip("lrmUpdateContentName",
                                   "You can update your content name here if needed"),

                    ], style={"width": "20%", "display": "inline-block", "verticalAlign": "top"}),
                    html.Div([
                        dcc.Input(id="categoryName_cr_update", value=text1, type="text", readOnly=True, style={
                                  "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                        dcc.Input(id="outpcontentShortName_cr_update", value=chosenContentInfo['shortname'], type="text", readOnly=True, style={
                                  "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                        dcc.Input(id="authorName_cr_update", value=customFlds['author'], type="text", readOnly=True, style={
                                  "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),

                        dcc.Input(id="contentName_cr_update", value=chosenContentInfo['fullname'], type="text", style={
                                  "width": "100%"}),
                    ], style={"width": "40%", "display": "inline-block", "verticalAlign": "top"}),

                ]),





                html.Hr(),


                # html.P("Number of Hours"),
                # dcc.Input(id="numHrs_cr_update",value=customFlds['number_of_hours'], type="number",min=0.5, max=20, step=0.5),

                # html.P("Intended Learning Outcome"),
                # dcc.Textarea(id="ilo_cr_update",value=customFlds['ilo'],style={"width":"50%"}),

                UI_ILOx(1, ilo_verb, ilo_text, float(
                    customFlds['number_of_hours'])),
                # id:verb_ILO1
                # id:text_ILO1
                # id:creditSlider1



                html.P(["Update Comment", UI_toolTipIcon(
                    "lrmUpdateUpdateComment")]),
                UI_toolTip("lrmUpdateUpdateComment",
                           "Add a comment for the version controlling system."),
                dcc.Textarea(id="updateComment_cr_update", style={
                             'width': '20%', 'height': 100}),

                html.Br(),

                html.Button('Update content',
                            id='btn-create-content_cr_update', n_clicks=0),
                html.Div(id="put-create-content-cr_update-msg_update"),
            ])

    else:
        div = html.Div([
            html.P("Please pick a short name first"),
        ])

    return div


# dummy call back
@callback(
    Output('dummy-div_update', 'children'),
    Input('categoryName_cr_update', 'value'),
    Input('contentName_cr_update', 'value'),
    Input('outpcontentShortName_cr_update', 'value'),
    Input('authorName_cr_update', 'value'),
    Input('updateComment_cr_update', 'value'),
    prevent_initial_call=True,
)
def func(A, B, C, D, E):
    return 1

# id:verb_ILO1
# id:text_ILO1
# id:creditSlider1

# click content create - update


@callback(
    Output('put-create-content-cr_update-msg_update', 'children'),
    Output('loading_update-output', 'children'),
    Input('btn-create-content_cr_update', 'n_clicks'),
    State('categoryName_cr_update', 'value'),
    State('contentName_cr_update', 'value'),
    State('outpcontentShortName_cr_update', 'value'),
    State('verb_ILO1', 'value'),
    State('text_ILO1', 'value'),
    State('creditSlider1', 'value'),
    State('authorName_cr_update', 'value'),
    State('updateComment_cr_update', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, categoryName_cr_update, contentName_cr_update, outpcontentShortName_cr_update, verb_ILO1, text_ILO1, creditSlider1, authorName_cr_update, updateComment_cr_update, email):
    def update(
        outpcontentShortName_cr_update,
        contentName_cr_update,
        creditSlider1,
        text_ILO1,
        verb_ILO1,
        updateComment_cr_update,
        email
    ):
        # user inputs
        # 'from_colab3-ah' #Pick from list [*categoryContentName2Id]
        chosenContentShortname = outpcontentShortName_cr_update
        contentName = contentName_cr_update
        numberOfHours = creditSlider1  # Integer --- Number of hours
        # ILOs like in the TEAL app
        ilo = "#"+verb_ILO1.replace(" ", "")+"# "+text_ILO1
        updateComment = updateComment_cr_update
        userEmail = email

        existingContent = call(webserviceAccessParamsContent, 'core_course_search_courses',
                               criterianame='search', criteriavalue=chosenContentShortname)['courses']
        chosenContentInfo = [
            crs for crs in existingContent if crs['shortname'] == chosenContentShortname][0]
        chosenContentID = chosenContentInfo['id']
        if userEmail in [fld['value'] for fld in chosenContentInfo['customfields'] if fld['shortname'] == 'author'][0]:
            contentInfo = {}
            contentInfo['id'] = chosenContentID
            contentInfo['shortname'] = chosenContentShortname
            contentInfo['fullname'] = contentName
            contentInfo['customfields'] = [
                {'shortname': 'number_of_hours', 'value': str(numberOfHours)},
                {'shortname': 'ilo', 'value': ilo},
                {'shortname': 'cah3_skill_classification', 'value': chosenCategory},
                {'shortname': 'author', 'value': userEmail}
            ]
            reponse = call(webserviceAccessParamsContent,
                           'core_course_update_courses', courses=[contentInfo])

            parameters = {'webserviceAccessParams': webserviceAccessParamsContent, 'access_parameters': {
                'gToken': githubToken, 'gUser': content_githubUser}, 'repoName': chosenContentShortname, 'updateComment': updateComment}
            outputMsg = course_content_GitHub_push(
                webserviceAccessParamsContent, mgGH, engineContent, parameters)

        else:
            # print('User '+userEmail+' does not have permission to update the content by the short name '+chosenContentShortname)
            outputMsg = 'User '+userEmail + \
                ' does not have permission to update the content by the short name ' + \
                chosenContentShortname
            chosenContentID = 0
        return outputMsg, chosenContentID

    if (n_clicks != 0):
        shortNameCheck = bool(
            re.search('^[a-z0-9_]*$', outpcontentShortName_cr_update))
        emptyCheck = categoryName_cr_update != None and contentName_cr_update != None and outpcontentShortName_cr_update != None and creditSlider1 != None and authorName_cr_update != None and updateComment_cr_update != None

        if (emptyCheck and shortNameCheck):
            outputMsg, chosenContentID = update(
                outpcontentShortName_cr_update,
                contentName_cr_update,
                creditSlider1,
                text_ILO1,
                verb_ILO1,
                updateComment_cr_update,
                email
            )

            # Add direct link to editable content page
            # contentID=result['created_content_id']
            # parameters={'webserviceAccessParams':webserviceAccessParamsContent,'access_parameters':{'gToken':githubToken, 'gUser':content_githubUser}, 'repoName':contentShortName, 'updateComment':'initial commit'}
            # outputMsg=course_content_GitHub_push(webserviceAccessParamsContent,mgGH,engineContent,parameters)
            # course_url=siteURLpublicContent+'/course/view.php?id={}'.format(contentID)
            course_url = siteURLpublicContent + \
                '/course/view.php?id={}'.format(chosenContentID)

            if (outputMsg == "Content updated"):
                print("success!")
                URLgithub = "https://github.com/TEAL2-O-Learning-Content/{}".format(
                    outpcontentShortName_cr_update)
                div = html.Div([
                    # html.P("Content with short name {} updated.".format(outpcontentShortName_cr_update)),
                    html.P("Metadata for content with short name {} updated.".format(
                        outpcontentShortName_cr_update)),
                    # html.A(URLgithub, href=URLgithub, target="_blank"),
                    # html.A("Go back to main page to edit the content", href="{}/{}-lrm".format(serverURL,appPrefixname), target="_blank"),
                    # html.Br(),
                    html.A("Click here if you want to edit the content",
                           href="{}".format(course_url), target="_blank"),
                ])

            else:
                # errMsg='User '+email+' does not have permission to update the content by the short name '+outpcontentShortName_cr_update
                print(outputMsg)
                div = html.Div([
                    html.P(outputMsg, style=style_err_msg),
                ])

        else:
            div = html.Div()
            if (not emptyCheck):
                div = html.Div("Please fill all fields")
            elif (not shortNameCheck):
                div = html.Div("Invalid short name format")

        return div, 1

    else:
        raise PreventUpdate


# ======================
# Section 2 : Fork
# ======================

# choose domain
@callback(
    Output('chosenSubDomain_cr_fork', 'options'),
    Input('chosenDomain_cr_fork', 'value'),
    prevent_initial_call=True,
)
def func(chosenDomain_cr_fork):
    if (chosenDomain_cr_fork != None):
        subDomainNamesIDs = {dmn['name']: dmn['id']
                             for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_fork]}
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
    Output('chosenSubSubDomain_cr_fork', 'options'),
    Input('chosenSubDomain_cr_fork', 'value'),
    Input('chosenDomain_cr_fork', 'value'),
    prevent_initial_call=True,
)
def func(chosenSubDomain_cr_fork, chosenDomain_cr_fork):
    if (chosenSubDomain_cr_fork != None and chosenDomain_cr_fork != None):

        try:
            subDomainNamesIDs = {dmn['name']: dmn['id']
                                 for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_fork]}
            subDomainNames = [*subDomainNamesIDs]
            subDomainNames.sort()
            print(subDomainNames)
            if len(subDomainNames) != 0:
                subSubDomainNamesIDs = {
                    dmn['name']: dmn['id'] for dmn in allCategories if dmn['parent'] == subDomainNamesIDs[chosenSubDomain_cr_fork]}
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
    Output('output-after_domain_select_cr_fork', 'children'),
    Input('btn-after_domain_select_cr_fork', 'n_clicks'),
    State('chosenDomain_cr_fork', 'value'),
    State('chosenSubDomain_cr_fork', 'value'),
    State('chosenSubSubDomain_cr_fork', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenDomain, chosenSubDomain, chosenSubSubDomain):

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
                html.P("Selected Category Name/Competancy"),

                html.Div([
                    html.Div([
                        dcc.Input(id="categoryName_cr_fork", value=text1, type="text", readOnly=True, style={
                                  "margin": "5px", "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                    ], style={"width": "60%", "display": "inline-block", 'verticalAlign': 'top'}),

                    html.Div([
                        html.Button('Confirm', id='btn-proceed-after-domain-select_cr_fork',
                                    n_clicks=0, style={"margin": "1%"}),
                    ], style={"width": "40%", "display": "inline-block", 'verticalAlign': 'top'}),
                ]),

                html.Div(id="boutput-create-content-msg_cr_fork"),
            ])

    else:
        div = html.Div([
            html.P("Please pick domain first"),
        ])

    return div


# Check Category Name/Competancy then click proceed
@callback(
    Output('boutput-create-content-msg_cr_fork', 'children'),
    Input('btn-proceed-after-domain-select_cr_fork', 'n_clicks'),
    State('categoryName_cr_fork', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, categoryName):
    if (n_clicks != 0):
        if (categoryName != None):

            chosenCategory = categoryName
            chosenCategoryID = call(webserviceAccessParamsContent, 'core_course_get_categories', criteria=[
                                    {'key': 'name', 'value': chosenCategory}])[0]['id']
            categoryContentListPDF = pd.read_sql(
                'SELECT id, category, shortname, fullname FROM mdl_course WHERE category={}'.format(chosenCategoryID), engineContent)
            categoryContentList = categoryContentListPDF['shortname'].to_list()
            categoryContentList.sort()

            div2 = html.Div([
                html.Br(),

                html.P(["Existing content listed by short name",
                       UI_toolTipIcon("lrmForkShortname")]),
                UI_toolTip("lrmForkShortname", ["Pick the short name of the content that you would like to fork. If you're unsure about the shortname, recheck by accessing ", html.A(
                    "TEAL content", href="/teal_content", target="_blank")]),


                html.Div([
                    html.Div([
                        UI_dropdown("chosenContentShortname_cr_fork",
                                    categoryContentList, {"margin": "5px"}),
                    ], style={"width": "60%", "display": "inline-block", 'verticalAlign': 'top'}),
                    html.Div([
                        html.Button('Proceed', id='btn-go_to_content_creation_fork',
                                    n_clicks=0, style={"margin": "1%"}),
                    ], style={"width": "40%", "display": "inline-block", 'verticalAlign': 'top'}),
                ]),

                html.Hr(),

                html.Div(id="output-go_to_content_creation_fork"),
            ]),

        else:
            div2 = html.Div("Please fill all fields")

        return div2

    else:
        raise PreventUpdate

# proceed after select Existing content listed by short name


@callback(
    Output('output-go_to_content_creation_fork', 'children'),
    Input('btn-go_to_content_creation_fork', 'n_clicks'),
    State('chosenDomain_cr_fork', 'value'),
    State('chosenSubDomain_cr_fork', 'value'),
    State('chosenSubSubDomain_cr_fork', 'value'),
    State('categoryName_cr_fork', 'value'),
    State('chosenContentShortname_cr_fork', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func1(n_clicks, chosenDomain_cr_fork, chosenSubDomain_cr_fork, chosenSubSubDomain_cr_fork, categoryName_cr_fork, chosenContentShortname_cr_fork, email):

    if (chosenDomain_cr_fork != None):
        if (chosenSubDomain_cr_fork == None and chosenSubSubDomain_cr_fork != None):
            div = html.Div([
                html.P("Please pick sub domain first"),
            ])

        else:
            text1 = chosenDomain_cr_fork
            if (chosenSubDomain_cr_fork != None and chosenSubSubDomain_cr_fork == None):
                text1 = chosenSubDomain_cr_fork
            elif (chosenSubDomain_cr_fork != None and chosenSubSubDomain_cr_fork != None):
                text1 = chosenSubSubDomain_cr_fork

            create_mode_radio = "update"  # remove later
            if (create_mode_radio == "update"):
                chosenContentInfoDict = call(webserviceAccessParamsContent, 'core_course_search_courses',
                                             criterianame='search', criteriavalue=chosenContentShortname_cr_fork)['courses'][0]
                chosenContentID = chosenContentInfoDict['id']
                chosenContentInfo = call(webserviceAccessParamsContent, 'core_course_get_courses', options={
                                         'ids': [chosenContentID]})[0]

                customFlds = {fld['shortname']: fld['valueraw']
                              for fld in chosenContentInfo['customfields']}

                div = html.Div([
                    html.Br(),

                    # html.P("Category Name/Competancy"),
                    # dcc.Input(id="categoryName_cr_fork",value=text1,type="text",readOnly=True),


                    html.Div([
                        html.Div([
                            # author is email here
                            html.P("Author", style={"height": "38px"}),
                        ], style={"width": "25%", "display": "inline-block", "verticalAlign": "top"}),
                        html.Div([

                            dcc.Input(id="authorName_cr_fork", value=email, type="text", readOnly=True, style={
                                      "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                        ], style={"width": "40%", "display": "inline-block", "verticalAlign": "top"}),

                    ]),








                    html.P("Please complete the following required fields."),
                    html.Br(),
                    div_skillSelectionCourseCreation(domainNames, '', 1),
                    # dcc.Input(id="categoryName_cr_fork",value=text1,type="text",readOnly=True),
                    html.Br(),



                    # html.H6('Search by course skills',style={'textAlign': 'center','font-weight': 'bold'}),
                    html.Div([
                        html.P(['Content Short Name', UI_toolTipIcon("lrmUpdateForkShortname")], style={
                               'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20, "height": "38px"}),
                        UI_toolTip("lrmUpdateForkShortname",
                                   "Only allowed \n [a-z,0-9,_] no spaces."),

                        html.P('Content Name', style={
                               'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20, "height": "38px"}),
                    ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                    html.Div([
                        dcc.Input(id="outpcontentShortName_cr_fork", value="", type="text", style={
                                  "width": "100%", "margin": "1px"}),
                        dcc.Input(id="contentName_cr_fork", value="", type="text", style={
                                  "width": "100%", "margin": "1px"}),
                    ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'}),


                    # html.P("Number of Hours"),
                    # dcc.Input(id="creditSlider2",value=customFlds['number_of_hours'], type="number",min=0.5, max=20, step=0.5),

                    # html.P("Intended Learning Outcome"),
                    # dcc.Textarea(id="ilo_cr_fork",value=customFlds['ilo'],style={"width":"50%"}),
                    html.Br(),
                    html.Br(),

                    UI_ILOx(2, None, "text here", 1.5),
                    # id:verb_ILO2
                    # id:text_ILO2
                    # id:creditSlider2



                    html.P(["Update Comment", UI_toolTipIcon(
                        "lrmUpdateForkComment")]),
                    UI_toolTip(
                        "lrmUpdateForkComment", "Add a comment for the version controlling system."),


                    dcc.Textarea(id="updateComment_cr_fork"),

                    html.Br(),

                    html.Button('Fork content',
                                id='btn-create-content_cr_fork', n_clicks=0),
                    html.Div(id="output-create-content-cr_fork-msg_fork"),
                ])
            elif (create_mode_radio == "create"):  # not used

                div = html.Div([
                    html.Br(),


                    html.P("Enter content Short Name"),
                    dcc.Input(id="outpcontentShortName_cr_update",
                              value=chosenContentShortname_cr_update, type="text"),


                    html.P("Category Name/Competancy"),
                    dcc.Input(id="categoryName_cr_update",
                              value=text1, type="text", readOnly=True),



                    html.P("Author"),
                    dcc.Input(id="authorName_cr_update", value=email,
                              type="text", readOnly=True),
                    html.P("Number of Hours"),
                    dcc.Input(id="numHrs_cr_update", value="nohrs",
                              type="number", min=0.5, max=20, step=0.5),

                    html.P("Content Name"),
                    dcc.Input(id="contentName_cr_update",
                              value="fullNamefd", type="text"),


                    html.P("Intended Learning Outcome"),
                    # dcc.Input(id="ilo_cr_update",value=iloTxt, type="text"),
                    dcc.Textarea(id="ilo_cr_update", value="iloTxt",
                                 style={"width": "50%"}),

                    html.P(["Update Comment", UI_toolTipIcon(
                        "lrmUpdateCreateComment")]),
                    UI_toolTip("lrmUpdateCreateComment",
                               "Add a comment for the version controlling system."),
                    dcc.Textarea(id="updateComment_cr_update"),

                    html.Br(),

                    html.Button('Update content',
                                id='btn-create-content_cr', n_clicks=0),
                    html.Div(id="put-create-content-cr_update-msg"),
                ])
            else:
                div = html.Div([
                    html.P("Please select mode"),
                ])

    else:
        div = html.Div([
            html.P("Please pick domain first"),
        ])

    return div


# dummy call back
@callback(
    Output('dummy-div_fork', 'children'),
    Input('categoryName_cr_fork', 'value'),
    Input('contentName_cr_fork', 'value'),
    Input('outpcontentShortName_cr_fork', 'value'),
    Input('creditSlider2', 'value'),
    Input('authorName_cr_fork', 'value'),
    Input('updateComment_cr_fork', 'value'),
    prevent_initial_call=True,
)
def func(A, B, C, D, E, F):
    return 1


# id:verb_ILO2
# id:text_ILO2
# id:creditSlider2

# click content create fork
@callback(
    Output('output-create-content-cr_fork-msg_fork', 'children'),
    Output('loading_fork-output', 'children'),
    Input('btn-create-content_cr_fork', 'n_clicks'),
    State('program_skillCC1', 'value'),
    State('contentName_cr_fork', 'value'),
    State('outpcontentShortName_cr_fork', 'value'),
    State('creditSlider2', 'value'),
    State('verb_ILO2', 'value'),
    State('text_ILO2', 'value'),
    State('authorName_cr_fork', 'value'),
    State('updateComment_cr_fork', 'value'),
    State('session1Type', 'data'),
    State('chosenContentShortname_cr_fork', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, program_skillCC1, contentName_cr_fork, outpcontentShortName_cr_fork, creditSlider2, verb_ILO2, text_ILO2, authorName_cr_fork, updateComment_cr_fork, email, chosenContentShortname_cr_fork):
    def fork(chosenContentShortname_cr_fork,
             outpcontentShortName_cr_fork,
             contentName_cr_fork,
             creditSlider2,
             verb_ILO2,
             text_ILO2,
             updateComment_cr_fork,
             email,
             program_skillCC1
             ):
        content2ForkShortname = chosenContentShortname_cr_fork
        content2ForkContent = call(webserviceAccessParamsContent, 'core_course_search_courses',
                                   criterianame='search', criteriavalue=content2ForkShortname)['courses']
        content2ForkContentInfo = [
            crs for crs in content2ForkContent if crs['shortname'] == content2ForkShortname][0]
        content2ForkContentID = content2ForkContentInfo['id']
        userEmail = email
        chosenCategory = program_skillCC1

        # User input
        newContentShortname = outpcontentShortName_cr_fork  # New shortname
        newContentName = contentName_cr_fork

        numberOfHours = creditSlider2  # Integer --- Number of hours
        # ILOs like in the TEAL app
        ilo = "#"+verb_ILO2.replace(" ", "")+"# "+text_ILO2

        customFields = [
            {'shortname': 'author', 'value': userEmail},
            {'shortname': 'number_of_hours', 'value': numberOfHours},
            {'shortname': 'cah3_skill_classification', 'value': chosenCategory},
            {'shortname': 'ilo', 'value': ilo},

        ]
        updateComment = updateComment_cr_fork
        existingContent = call(webserviceAccessParamsContent, 'core_course_search_courses',
                               criterianame='search', criteriavalue=newContentShortname)['courses']
        if len(existingContent) == 0:
            params = {}
            params['templateShortName'] = content2ForkShortname
            params['categoryName'] = chosenCategory
            params['fullname'] = newContentName
            params['shortname'] = newContentShortname
            params['webserviceAccessParams'] = webserviceAccessParamsContent
            params['customfields'] = customFields
            result = create_course_4m_moodle_template(params)
            contentID = result['created_content_id']
            parameters = {'webserviceAccessParams': webserviceAccessParamsContent, 'access_parameters': {
                'gToken': githubToken, 'gUser': content_githubUser}, 'repoName': newContentShortname, 'updateComment': 'initial commit'}
            outputMsg = course_content_GitHub_push(
                webserviceAccessParamsContent, mgGH, engineContent, parameters)
            print(result)
        else:
            outputMsg = 'Content with the shortname similar to ' + \
                newContentShortname+' exists. Please pick another short name'
            result = []
        return outputMsg, result

    if (n_clicks != 0):
        shortNameCheck = bool(
            re.search('^[a-z0-9_]*$', outpcontentShortName_cr_fork))
        emptyCheck = program_skillCC1 != None and contentName_cr_fork != None and outpcontentShortName_cr_fork != None and creditSlider2 != None and authorName_cr_fork != None and updateComment_cr_fork != None

        if (emptyCheck and shortNameCheck):

            outputMsg, result = fork(chosenContentShortname_cr_fork,
                                     outpcontentShortName_cr_fork,
                                     contentName_cr_fork,
                                     creditSlider2,
                                     verb_ILO2,
                                     text_ILO2,
                                     updateComment_cr_fork,
                                     email,
                                     program_skillCC1
                                     )

            print("Fork function success!")
            print("outputMsg:", outputMsg)

            userName = email
            userRoleShortName = 'teal2po_content_creator'
            newContentShortname = outpcontentShortName_cr_fork

            manual_enroll_user_in_course(
                engineContent, webserviceAccessParamsContent, newContentShortname, userName, userRoleShortName)

            # Add direct link to editable content page
            contentID = result['created_content_id']
            course_url = siteURLpublicContent + \
                '/course/view.php?id={}'.format(contentID)

            if (outputMsg == "Content created"):
                div = html.Div([
                    html.P("Metadata for content with short name {} created.".format(
                        outpcontentShortName_cr_fork)),
                    html.A("Click here to edit the content if need",
                           href="{}".format(course_url), target="_blank"),

                ])
            else:
                div = html.Div([
                    html.P(outputMsg, style=style_err_msg),
                ])

        else:
            div = html.Div()
            if (not emptyCheck):
                div = html.Div("Please fill all fields")
            elif (not shortNameCheck):
                div = html.Div("Invalid short name format")

        return div, 1

    else:
        raise PreventUpdate


# ======================
# Section 3 : Create
# ======================

# choose domain
@callback(
    Output('chosenSubDomain_cr_create', 'options'),
    Input('chosenDomain_cr_create', 'value'),
    prevent_initial_call=True,
)
def func(chosenDomain_cr_create):
    if (chosenDomain_cr_create != None):
        subDomainNamesIDs = {dmn['name']: dmn['id']
                             for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_create]}
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
    Output('chosenSubSubDomain_cr_create', 'options'),
    Input('chosenSubDomain_cr_create', 'value'),
    Input('chosenDomain_cr_create', 'value'),
    prevent_initial_call=True,
)
def func(chosenSubDomain_cr_create, chosenDomain_cr_create):
    if (chosenSubDomain_cr_create != None and chosenDomain_cr_create != None):

        try:
            subDomainNamesIDs = {dmn['name']: dmn['id']
                                 for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_create]}
            subDomainNames = [*subDomainNamesIDs]
            subDomainNames.sort()
            print(subDomainNames)
            if len(subDomainNames) != 0:
                subSubDomainNamesIDs = {
                    dmn['name']: dmn['id'] for dmn in allCategories if dmn['parent'] == subDomainNamesIDs[chosenSubDomain_cr_create]}
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
    Output('output-after_domain_select_cr_create', 'children'),
    Input('btn-after_domain_select_cr_create', 'n_clicks'),
    State('chosenDomain_cr_create', 'value'),
    State('chosenSubDomain_cr_create', 'value'),
    State('chosenSubSubDomain_cr_create', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenDomain, chosenSubDomain, chosenSubSubDomain):

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
                html.P("Selected Category Name/Competancy"),
                html.Div([
                    html.Div([
                        dcc.Input(id="categoryName_cr_create", value=text1, type="text", readOnly=True, style={
                                  "margin": "5px", "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                    ], style={"width": "60%", "display": "inline-block", 'verticalAlign': 'top'}),
                    html.Div([
                        html.Button('Confirm', id='btn-proceed-after-domain-select_cr_create',
                                    n_clicks=0, style={"margin": "1%"}),
                    ], style={"width": "40%", "display": "inline-block", 'verticalAlign': 'top'}),
                ]),



                html.Div(id="boutput-create-content-msg_cr_create"),
            ])

    else:
        div = html.Div([
            html.P("Please pick domain first"),
        ])

    return div


# confirm after Selected Category Name/Competancy
@callback(
    Output('boutput-create-content-msg_cr_create', 'children'),
    Input('btn-proceed-after-domain-select_cr_create', 'n_clicks'),
    State('chosenDomain_cr_create', 'value'),
    State('chosenSubDomain_cr_create', 'value'),
    State('chosenSubSubDomain_cr_create', 'value'),
    State('categoryName_cr_create', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func1(n_clicks, chosenDomain_cr_create, chosenSubDomain_cr_create, chosenSubSubDomain_cr_create, categoryName_cr_create, email):

    if (chosenDomain_cr_create != None):
        if (chosenSubDomain_cr_create == None and chosenSubSubDomain_cr_create != None):
            div = html.Div([
                html.P("Please pick sub domain first"),
            ])

        else:
            text1 = chosenDomain_cr_create
            if (chosenSubDomain_cr_create != None and chosenSubSubDomain_cr_create == None):
                text1 = chosenSubDomain_cr_create
            elif (chosenSubDomain_cr_create != None and chosenSubSubDomain_cr_create != None):
                text1 = chosenSubSubDomain_cr_create

            div = html.Div([
                html.Br(),

                # html.P("Category Name/Competancy*******"),
                # dcc.Input(id="categoryName_cr_create",value=text1,type="text",readOnly=True),

                html.Hr(),

                html.Div([
                    html.Div([
                        # author is email here
                        html.P("Author", style={"height": "38px"}),
                    ], style={"width": "25%", "display": "inline-block", "verticalAlign": "top"}),
                    html.Div([

                        dcc.Input(id="authorName_cr_create", value=email, type="text", readOnly=True, style={
                                  "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                    ], style={"width": "40%", "display": "inline-block", "verticalAlign": "top"}),

                ]),


                html.Hr(),


                html.P("Please complete the following required fields."),

                html.Div([
                    html.P(['Content Short Name', UI_toolTipIcon("lrmUpdateCreateShortname")], style={
                           'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20, "height": "38px"}),
                    UI_toolTip("lrmUpdateCreateShortname",
                               "Only allowed \n [a-z,0-9,_] no spaces."),

                    html.P('Content Name', style={
                        'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20, "height": "38px"}),
                ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),


                html.Div([
                    dcc.Input(id="outpcontentShortName_cr_create", value="", type="text", style={
                              "width": "100%", "margin": "1px"}),
                    dcc.Input(id="contentName_cr_create", value="", type="text", style={
                              "width": "100%", "margin": "1px"}),
                ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'}),


                # html.P("Number of Hours"),
                # dcc.Input(id="numHrs_cr_create",value="", type="number",min=0.5, max=20, step=0.5),

                # html.P("Intended Learning Outcome"),
                # dcc.Textarea(id="ilo_cr_create",value="",style={"width":"50%"}),

                html.Br(),


                UI_ILOx(3, None, "text here", 1.5),
                # id:verb_ILO3
                # id:text_ILO3
                # id:creditSlider3

                html.P(["Update Comment", UI_toolTipIcon(
                    "lrmUpdateCreate2Comment")]),
                UI_toolTip("lrmUpdateCreate2Comment",
                           "Add a comment for the version controlling system."),

                dcc.Textarea(id="updateComment_cr_create"),

                html.Br(),

                html.Button('Create content',
                            id='btn-create-content_cr_create', n_clicks=0),
                html.Div(id="output-create-content-cr_create-msg_create"),
            ])

    else:
        div = html.Div([
            html.P("Please pick domain first"),
        ])

    return div


# click Create content
@callback(
    Output('output-create-content-cr_create-msg_create', 'children'),
    Output('loading_create-output', 'children'),
    Input('btn-create-content_cr_create', 'n_clicks'),
    State('categoryName_cr_create', 'value'),
    State('contentName_cr_create', 'value'),
    State('outpcontentShortName_cr_create', 'value'),
    State('creditSlider3', 'value'),
    State('verb_ILO3', 'value'),
    State('text_ILO3', 'value'),
    State('authorName_cr_create', 'value'),
    State('updateComment_cr_create', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, categoryName_cr_create, contentName_cr_create, outpcontentShortName_cr_create, creditSlider3, verb_ILO3, text_ILO3, authorName_cr_create, updateComment_cr_create, email):
    def create(
        outpcontentShortName_cr_create,
        contentName_cr_create,
        creditSlider3,
        categoryName_cr_create,
        email
    ):

        # User Inputs
        contentShortName = outpcontentShortName_cr_create
        contentName = contentName_cr_create
        numberOfHours = creditSlider3
        ilo = "#"+verb_ILO3.replace(" ", "")+"# "+text_ILO3
        print(ilo)
        chosenCategory = categoryName_cr_create
        userEmail = email
        customFields = [
            {'shortname': 'author', 'value': userEmail},
            {'shortname': 'number_of_hours', 'value': numberOfHours},
            {'shortname': 'cah3_skill_classification', 'value': chosenCategory},
            {'shortname': 'ilo', 'value': ilo},

        ]

        # Hard coded at config level depending on context
        templateShortName = templateHVPcontent  # 'template_course_specification'

        existingContent = call(webserviceAccessParamsContent, 'core_course_search_courses',
                               criterianame='search', criteriavalue=contentShortName)['courses']
        if len(existingContent) == 0:
            params = {}
            params['templateShortName'] = templateShortName
            params['categoryName'] = chosenCategory
            params['fullname'] = contentName
            params['shortname'] = contentShortName
            params['webserviceAccessParams'] = webserviceAccessParamsContent
            params['customfields'] = customFields
            result = create_course_4m_moodle_template(params)

            # call(webserviceAccessParamsContent,'core_course_edit_module',action='show',id=result['crsModuleInfo'][0]['id'])#toggle module view

            userName = userEmail
            userRoleShortName = 'teal2po_content_creator'

            manual_enroll_user_in_course(
                engineContent, webserviceAccessParamsContent, contentShortName, userName, userRoleShortName)
            contentID = result['created_content_id']
            parameters = {'webserviceAccessParams': webserviceAccessParamsContent, 'access_parameters': {
                'gToken': githubToken, 'gUser': content_githubUser}, 'repoName': contentShortName, 'updateComment': 'initial commit'}
            outputMsg = course_content_GitHub_push(
                webserviceAccessParamsContent, mgGH, engineContent, parameters)
            course_url = siteURLpublicContent + \
                '/course/view.php?id={}'.format(contentID)
        else:
            outputMsg = 'Content with the shortname similar to ' + \
                contentShortName+' exists. Please pick another short name'
            course_url = siteURLpublicContent + \
                '/course/view.php?id={}'.format(existingContent[0]['id'])

        return outputMsg, course_url

    if (n_clicks != 0):
        shortNameCheck = bool(
            re.search('^[a-z0-9_]*$', outpcontentShortName_cr_create))
        emptyCheck = categoryName_cr_create != None and contentName_cr_create != None and outpcontentShortName_cr_create != None and text_ILO3 != None and authorName_cr_create != None and updateComment_cr_create != None

        if (emptyCheck and shortNameCheck):
            outputMsg, course_url = create(
                outpcontentShortName_cr_create,
                contentName_cr_create,
                creditSlider3,
                categoryName_cr_create,
                email
            )
            print("Function success - create!")
            if (outputMsg == "Content created"):

                div = html.Div([
                    html.P("Metadata for content with short name {} created.".format(
                        outpcontentShortName_cr_create)),
                    # html.A(URLgithub, href=URLgithub, target="_blank"),
                    html.P("View/edit content"),
                    html.A(course_url, href=course_url, target="_blank"),
                    # html.A("Go back to main page to edit the content", href="{}/gnrl-lrm".format(serverURL), target="_blank"),

                ])
            else:
                print(outputMsg)
                div = html.Div([
                    html.P(outputMsg, style=style_err_msg),
                ])

        else:
            div = html.Div()
            if (not emptyCheck):
                div = html.Div("Please fill all fields")
            elif (not shortNameCheck):
                div = html.Div("Invalid short name format")

        return div, 1

    else:
        raise PreventUpdate


# user selects Solo level - verb list generated
# 1
@callback(
    Output("verb_ILO1", "options"),
    Input("solo_level_ILO1", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')

        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]

# 2


@callback(
    Output("verb_ILO2", "options"),
    Input("solo_level_ILO2", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')

        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]

# 3


@callback(
    Output("verb_ILO3", "options"),
    Input("solo_level_ILO3", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')

        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]


# program domain selected - course
@callback(
    Output("program_subdomainCC1", "options"),
    Input("program_domainCC1", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value != None):
        chosenDomain_cr_update = value
        subDomainNamesIDs = {dmn['name']: dmn['id']
                             for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_update]}
        subDomainNames = [*subDomainNamesIDs]
        subDomainNames.sort()

        if len(subDomainNames) != 0:
            options1 = subDomainNames
        else:
            options1 = []

        return [{'label': i, 'value': i} for i in options1]
    else:
        return [{'label': i, 'value': i} for i in []]


# program subdomain selected
@callback(
    Output("program_skillCC1", "options"),
    Input("program_domainCC1", "value"),
    Input("program_subdomainCC1", "value"),
    prevent_initial_call=True,
)
def func(program_domain, program_subdomain):
    if (program_subdomain != None):
        chosenDomain_cr_fork = program_domain
        chosenSubDomain_cr_fork = program_subdomain

        try:
            subDomainNamesIDs = {dmn['name']: dmn['id']
                                 for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_cr_fork]}
            subDomainNames = [*subDomainNamesIDs]
            subDomainNames.sort()
            print(subDomainNames)
            if len(subDomainNames) != 0:
                subSubDomainNamesIDs = {
                    dmn['name']: dmn['id'] for dmn in allCategories if dmn['parent'] == subDomainNamesIDs[chosenSubDomain_cr_fork]}
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

        return [{'label': i, 'value': i} for i in options1]
    else:
        return [{'label': i, 'value': i} for i in []]
