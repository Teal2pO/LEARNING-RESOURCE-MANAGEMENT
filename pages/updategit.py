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

chosenDomain_git = ''
chosenSubDomain_git = ''
chosenSubSubDomain_git = ''
chosenCategory = ''
domainNamesIDs = {dmn['name']: dmn['id']
                  for dmn in allCategories if dmn['parent'] == 0}
domainNames = [*domainNamesIDs]
domainNames.sort()

dash.register_page(__name__, path='/updategit')

layout = html.Div([
    # dcc.Link(html.Button("View/Edit content"), href="/{}-lrm".format(appPrefixname), refresh=True),
    html.Button('Proceed to version update',
                id='emailConfirm-updategit-btn', n_clicks=0),
    dcc.Link(html.Button("Home"), href="/teal-lrm/", refresh=True),

    html.Div(id='contentAfterEmail-updategit-output'),





    dcc.Loading(id="loading_git-loading", type="dot", fullscreen=True,
                children=html.Div(id="loading_git-output",
                                  style={'display': 'none'})
                ),


], style={'margin': '15px'})


# ===========================Callbacks
# email check when user click proceed
@callback(
    Output('contentAfterEmail-updategit-output', 'children'),
    Input('emailConfirm-updategit-btn', 'n_clicks'),
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

            html.H2([
                html.H2("‣ Update content version information", style={
                        "font-weight": "bold", "display": "inline"}),
                    UI_toolTipIcon("lrmUpdateGit"),
                    html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                           href="https://drive.google.com/file/d/1n8zENECE4WUlYWUJWBoVZ-ZCL3XFGngc/view?usp=sharing", target='_blank', style={"text-decoration": "none"}),
                    ]),

            UI_toolTip("lrmUpdateGit", "After you complete editing the content, use this section to update content details in the version controlling system. This step should be completed before moving content to the classrooms. Only the content creator is allowed to update the version information."),



            html.P(["Please pick domain", UI_toolTipIcon("lrmUpdateGitDomain")]),
            UI_toolTip("lrmUpdateGitDomain",
                       "Use CAH3 classification filters to find the content that you want to update the version information."),

            UI_dropdown("chosenDomain_git", domainNames, {
                        "margin": "5px", "width": "75%"}),

            html.P("Pick sub domain from Dropdown list"),
            UI_dropdown("chosenSubDomain_git", [], {
                        "margin": "5px", "width": "75%"}),

            html.P("Pick sub sub domain from Dropdown list"),
            UI_dropdown("chosenSubSubDomain_git", [], {
                        "margin": "5px", "width": "75%"}),

            html.Br(),

            html.Button(
                'Proceed', id='btn-after_domain_select_git', n_clicks=0),


            html.Div(id="output-after_domain_select_git"),
        ])

    else:
        div = html.P('Invalid user!')

    return div

# choose domain


@callback(
    Output('chosenSubDomain_git', 'options'),
    Input('chosenDomain_git', 'value'),
    prevent_initial_call=True,
)
def func(chosenDomain_git):
    if (chosenDomain_git != None):
        subDomainNamesIDs = {dmn['name']: dmn['id']
                             for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_git]}
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
    Output('chosenSubSubDomain_git', 'options'),
    Input('chosenSubDomain_git', 'value'),
    Input('chosenDomain_git', 'value'),
    prevent_initial_call=True,
)
def func(chosenSubDomain_git, chosenDomain_git):
    if (chosenSubDomain_git != None and chosenDomain_git != None):

        try:
            subDomainNamesIDs = {dmn['name']: dmn['id']
                                 for dmn in allCategories if dmn['parent'] == domainNamesIDs[chosenDomain_git]}
            subDomainNames = [*subDomainNamesIDs]
            subDomainNames.sort()
            print(subDomainNames)
            if len(subDomainNames) != 0:
                subSubDomainNamesIDs = {
                    dmn['name']: dmn['id'] for dmn in allCategories if dmn['parent'] == subDomainNamesIDs[chosenSubDomain_git]}
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


# proceed after domain/subdomain/subsubdomain select
@callback(
    Output('output-after_domain_select_git', 'children'),
    Input('btn-after_domain_select_git', 'n_clicks'),
    State('chosenDomain_git', 'value'),
    State('chosenSubDomain_git', 'value'),
    State('chosenSubSubDomain_git', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenDomain_git, chosenSubDomain_git, chosenSubSubDomain_git):
    print(chosenDomain_git)
    print(chosenSubDomain_git)
    print(chosenSubSubDomain_git)

    if (chosenDomain_git != None):
        if (chosenSubDomain_git == None and chosenSubSubDomain_git != None):
            div = html.Div([
                html.P("Please pick sub domain first"),
            ])

        else:
            text1 = chosenDomain_git
            if (chosenSubDomain_git != None and chosenSubSubDomain_git == None):
                text1 = chosenSubDomain_git
            elif (chosenSubDomain_git != None and chosenSubSubDomain_git != None):
                text1 = chosenSubSubDomain_git

            div = html.Div([
                html.Br(),
                html.P("Selected Category Name/Competancy"),



                html.Div([
                    html.Div([
                        dcc.Input(id="categoryName_git", value=text1, type="text", readOnly=True, style={
                                  "margin": "5px", "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                    ], style={"width": "60%", "display": "inline-block", 'verticalAlign': 'top'}),
                    html.Div([
                        html.Button('Proceed', id='btn-proceed-after-domain-select_git',
                                    n_clicks=0, style={"margin": "1%"}),
                    ], style={"width": "40%", "display": "inline-block", 'verticalAlign': 'top'}),
                ]),

                html.Div(id="output-create-content_git-msg"),

            ])

    else:
        div = html.Div([
            html.P("Please pick domain first"),
        ])

    return div


# check Selected Category Name/Competancy and click proceed
@callback(
    Output('output-create-content_git-msg', 'children'),
    Input('btn-proceed-after-domain-select_git', 'n_clicks'),
    State('categoryName_git', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, categoryName_git):
    if (n_clicks != 0):
        if (categoryName_git != None):

            chosenCategory = categoryName_git
            chosenCategoryID = call(webserviceAccessParamsContent, 'core_course_get_categories ', criteria=[
                                    {'key': 'name', 'value': chosenCategory}])[0]['id']
            categoryContentListPDF = pd.read_sql(
                'SELECT id, category, shortname, fullname FROM mdl_course WHERE category={}'.format(chosenCategoryID), engineContent)
            categoryContentList = categoryContentListPDF['shortname'].to_list()
            categoryContentList.sort()

            div2 = html.Div([

                html.P(["Select content short name",
                       UI_toolTipIcon("lrmUpdateGitShortname")]),
                UI_toolTip("lrmUpdateGitShortname",
                           "Pick shortname of the content. You can only update the version information for the content created by yourself."),

                html.Div([
                    html.Div([
                        UI_dropdown("chosenContentShortname_git",
                                    categoryContentList),
                    ], style={"width": "60%", "display": "inline-block", 'verticalAlign': 'top', 'margin-top': '5px'}),
                    html.Div([
                        html.Button('Proceed', id='btn-show_content_git',
                                    n_clicks=0, style={"margin": "1%"}),
                    ], style={"width": "40%", "display": "inline-block", 'verticalAlign': 'top'}),
                ]),

                html.Div(id="output-gitstuff"),
            ]),

        else:
            div2 = html.Div("Please fill all fields")

        return div2

    else:
        raise PreventUpdate


# show content button click
@callback(
    # Output('output-create-content_git', 'children'),
    Output('output-gitstuff', 'children'),
    Input('btn-show_content_git', 'n_clicks'),
    State('chosenContentShortname_git', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenContentShortname_git, email):
    if (n_clicks != 0):
        existingContent = call(webserviceAccessParamsContent, 'core_course_search_courses',
                               criterianame='search', criteriavalue=chosenContentShortname_git)['courses']
        chosenContentInfoDict = [
            crs for crs in existingContent if crs['shortname'] == chosenContentShortname_git][0]
        chosenContentID = chosenContentInfoDict['id']

        # contentURL=siteURL+'/course/view.php?id={}'.format(chosenContentID)
        contentURL = call(webserviceAccessParamsContent, 'core_course_get_contents',
                          courseid=chosenContentID)[0]['modules'][0]['url']
        contentURL = contentURL.replace("https://127.0.0.1", serverURL)

        # div=html.Div([
        # html.Iframe(src=contentURL,style={"height": "1067px", "width": "100%"})
        # ])

        div2 = html.Div([

            html.Br(),
            html.Div([
                html.Div([
                    # author is email here
                    html.P("Current user", style={"height": "30px"}),
                ], style={"width": "25%", "display": "inline-block", "verticalAlign": "top"}),
                html.Div([

                    dcc.Input(id="usernameGit", value=email, type="text", readOnly=True, style={
                              "width": "100%", "background-color": "#eaeaea", "border": "2px white solid"}),
                ], style={"width": "40%", "display": "inline-block", "verticalAlign": "top"}),

            ]),

            html.Br(),


            html.P(["Enter comment", UI_toolTipIcon("lrmUpdateGitComment")]),
            UI_toolTip("lrmUpdateGitComment",
                       "Add a comment for the version controlling system."),

            dcc.Textarea(id="gitComment"),
            html.Br(),
            html.Button('Update version history',
                        id='btn-gitcommit', n_clicks=0),
            html.Div(id="output-gitcommit"),
        ])

        return div2
    else:
        raise PreventUpdate


# commit
@callback(
    Output('output-gitcommit', 'children'),
    Output('loading_git-output', 'children'),
    Input('btn-gitcommit', 'n_clicks'),
    State('usernameGit', 'value'),
    State('gitComment', 'value'),
    State('chosenContentShortname_git', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, usernameGit, gitComment, chosenContentShortname_git):
    if (n_clicks != 0):
        print("I'm running")
        userName = usernameGit
        updateComment = gitComment
        chosenContentShortname = chosenContentShortname_git

        existingContent = call(webserviceAccessParamsContent, 'core_course_search_courses',
                               criterianame='search', criteriavalue=chosenContentShortname)['courses']
        chosenContentInfoDict = [
            crs for crs in existingContent if crs['shortname'] == chosenContentShortname][0]
        chosenContentID = chosenContentInfoDict['id']

        # Check if user exists
        userInfo = call(webserviceAccessParamsContent, 'core_user_get_users', criteria=[
                        {'key': 'username', 'value': userName}])['users']  # [0]
        userExists = (len(userInfo) != 0)

        if not userExists:
            msg = ('User '+userName+' does not exist')
            div = html.Div([
                html.P(msg)
            ])

        # Go back to the form
        else:
            contentAuthors = [
                fld['value'] for fld in chosenContentInfoDict['customfields'] if fld['shortname'] == 'author'][0]
            parameters = {'webserviceAccessParams': webserviceAccessParamsContent, 'access_parameters': {
                'gToken': githubToken, 'gUser': content_githubUser}, 'repoName': chosenContentShortname, 'updateComment': updateComment}

            if (contentAuthors != []):
                if userName in contentAuthors:
                    msg = course_content_GitHub_push(
                        webserviceAccessParamsContent, mgGH, engineContent, parameters)
                    div = html.Div([
                        html.P(msg)
                    ])

                else:
                    msg = (
                        'User '+userName+' does not have permission to edit the content created by '+contentAuthors)
                    div = html.Div([
                        html.P(msg)
                    ])
            else:
                div = html.Div([
                    html.P("Content owner undefined")
                ])

        return div, 1

    else:
        raise PreventUpdate
