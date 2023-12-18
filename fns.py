from static_globals import *
from github import Github
from requests import get, post
import json
import pandas as pd
import os
import re


def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        valid_email = True
    else:
        valid_email = False
    return valid_email

# GitHub Function Definitions


class tealMGitHub:
    def __init__(self):
        self = []

    def get_GitHub_user(self, params):
        self.g = Github(params['gToken'])
        return self.g

    def get_GitHub_organization_repos(self, params):
        self.g = Github(params['gToken'])
        self.organization = self.g.get_organization(params['gUser'])
        repoNames = [repo.name for repo in self.organization.get_repos()]
        return repoNames

    def get_repo_info(self, params):
        self.g = Github(params['gToken'])
        fileNames = []
        repoName = params['repoName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        branches = list(repo.get_branches())
        branchNames = [br.name for br in branches]
        contents = repo.get_contents("")

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                fls = repo.get_contents(file_content.path)
                contents.extend(fls)
            else:
                fileNames += [file_content.path]

        return {'branch_names': branchNames, 'file_names': fileNames}

    def get_repo_file_content(self, params):
        self.g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        b = repo.get_branch(branch=params['branchName'])
        contents = repo.get_contents(params['fileName'], ref=b.commit.sha)
        # self.contents = self.repo.get_file_contents(params['fileName'], ref=b.commit.sha)
        return {'repo': repo, 'contents': contents}

    def write_file_2_repo(self, params):
        self.g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        return repo.create_file(params['writeFile'], params['commitComment'], params['content2Write'], branch=params['branchName'])

    def delete_file(self, params):
        self.g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        b = repo.get_branch(branch=params['branchName'])
        contents = repo.get_contents(params['fileName'], ref=b.commit.sha)
        return repo.delete_file(contents.path, params['commitComment'], contents.sha, branch=params['branchName'])


def GithubViewDeleteApp_fn(func):

    def inner1(b):
        c = func(b)
        return c

    return inner1


def GithubViewDeleteApp(inputDict):
    function_to_be_called = GithubViewDeleteApp_fn(inputDict['functionName'])
    return function_to_be_called(inputDict['functionParameters'])


def create_update_GITHUB_organization_repos(mgGH, parameters):
    functionParameters = {'gToken': parameters['access_parameters']['gToken'], 'gUser': parameters['access_parameters']['gUser'], 'repoName': parameters['repoName'],
                          'branchName': 'main', 'writeFile': parameters['fileInfoDict']['filename'], 'content2Write': parameters['fileInfoDict']['filecontent'], 'commitComment': parameters['updateComment']}
    inputDict = {'functionName': mgGH.get_GitHub_organization_repos,
                 'functionParameters': parameters['access_parameters']}
    reposList = GithubViewDeleteApp(inputDict)
    if parameters['repoName'] in reposList:
        functionParameters['fileName'] = parameters['fileInfoDict']['filename']
        inputDict = {'functionName': mgGH.get_repo_file_content,
                     'functionParameters': functionParameters}
        try:
            fileOut = GithubViewDeleteApp(inputDict)
            content = fileOut['contents']
            repo = fileOut['repo']
            repo.update_file(content.path, parameters['updateComment'],
                             parameters['fileInfoDict']['filecontent'], content.sha, branch='main')
            message = 'Content updated'
        except:
            inputDictWrite = {'functionName': mgGH.write_file_2_repo,
                              'functionParameters': functionParameters}
            GithubViewDeleteApp(inputDictWrite)
            message = 'Content created'

    else:
        mgGH.organization.create_repo(parameters['repoName'], private=True)
        inputDictWrite = {'functionName': mgGH.write_file_2_repo,
                          'functionParameters': functionParameters}
        GithubViewDeleteApp(inputDictWrite)
        message = 'Content created'
    return message

# DB Access


class mugas_DB_functions:

    def __init__(self):
        self = []

    def sql_request(self, SQLengine, params):
        return pd.read_sql(params['sqlQuery'], SQLengine).to_dict(orient='records')

    def get_all_tables(self, sqlEngine):
        return pd.read_sql_query('SHOW TABLES', sqlEngine).to_dict(orient='records')

    def get_filtered_columns(self, SQLengine, params):
        db_table_name = params['db_table_name']
        filterDict = params['filterDict']
        filterPairs = [ky+'="{}"'.format(filterDict[ky])
                       for ky in [*filterDict]]
        sql_q = "SELECT {} FROM {} WHERE {}"
        return pd.read_sql(sql_q.format(','.join(params['returnColumns']), db_table_name, ' AND '.join(filterPairs)), SQLengine).to_dict(orient='records')

    def get_all_records_between_ranges(self, SQLengine, params):
        db_table_name = params['db_table_name']
        colName = params['colName']
        startVal = params['startVal']
        endVal = params['endVal']
        sql_q = "SELECT {} FROM {} WHERE {} BETWEEN {} AND {}"
        return pd.read_sql(sql_q.format(','.join(params['returnColumns']), db_table_name, colName, startVal, endVal), SQLengine).to_dict(orient='records')

    def get_filtered_records_between_ranges(self, SQLengine, params):
        db_table_name = params['db_table_name']
        filterDict = params['filterDict']
        filterPairs = [ky+'="{}"'.format(filterDict[ky])
                       for ky in [*filterDict]]
        colName = params['colName']
        startVal = params['startVal']
        endVal = params['endVal']
        sql_q = "SELECT {} FROM {} WHERE {} BETWEEN {} AND {} AND {}"
        return pd.read_sql(sql_q.format(','.join(params['returnColumns']), db_table_name, colName, startVal, endVal, ' AND '.join(filterPairs)), SQLengine).to_dict(orient='records')

    def get_all_records_column_values_in(self, SQLengine, params):
        db_table_name = params['db_table_name']
        colName = params['colName']
        colVals = params['colVals']
        sql_q = "SELECT {} FROM {} WHERE {} IN ({})"
        return pd.read_sql(sql_q.format(','.join(params['returnColumns']), db_table_name, colName, ', '.join([str(xx) for xx in colVals])), SQLengine).to_dict(orient='records')

    def get_filtered_records_column_values_in(self, SQLengine, params):
        db_table_name = params['db_table_name']
        colName = params['colName']
        colVals = params['colVals']
        filterDict = params['filterDict']
        filterPairs = [ky+'="{}"'.format(filterDict[ky])
                       for ky in [*filterDict]]
        sql_q = "SELECT {} FROM {} WHERE {} IN ({}) AND {}"
        return pd.read_sql(sql_q.format(','.join(params['returnColumns']), db_table_name, colName, ', '.join([str(xx) for xx in colVals]), ' AND '.join(filterPairs)), SQLengine).to_dict(orient='records')

    def delete_record(self, SQLengine, params):
        filterStrLst = [fltcol+'="{}"'.format(params['filterDict'][fltcol])
                        for fltcol in [*params['filterDict']]]
        filterStr = ' AND '.join(filterStrLst)
        sqlQuery = "DELETE FROM {} WHERE {}".format(
            params['db_table_name'], filterStr)
        sql.execute(sqlQuery, SQLengine)
        return 'Table {} updated successfully'.format(params['db_table_name'])

    def update_record(self, SQLengine, params):
        db_table_name = params['db_table_name']
        filterDict = params['filterDict']
        updateDict = params['updateDict']
        filterStrLst = [fltcol+'="{}"'.format(params['filterDict'][fltcol])
                        for fltcol in [*params['filterDict']]]
        filterStr = ' AND '.join(filterStrLst)
        updatePairs = ['{}="{}"'.format(ky, updateDict[ky])
                       for ky in [*updateDict]]
        sqlQuery = 'UPDATE {} SET {} WHERE {}'.format(
            db_table_name, ', '.join(updatePairs), filterStr)
        sql.execute(sqlQuery, SQLengine)
        return 'Table {} updated successfully'.format(db_table_name)

    def insert_record(self, sqlEngine, params):
        db_table_name = params['db_table_name']
        updateDict = params['updateDict']
        db_table_PDF = pd.read_sql(
            'SELECT * FROM {} WHERE id=(SELECT max(id) FROM {})'.format(db_table_name, db_table_name), sqlEngine)
        diffCols = set([*updateDict]).difference(set([*db_table_PDF]))
        if len(diffCols) == 0:
            lastIndex = db_table_PDF['id'].values[0]
            insert_entry_PDF = pd.DataFrame(
                columns=[*db_table_PDF], index=[int(lastIndex+1)]).drop(columns=['id'])
            insert_entry_PDF.loc[int(
                lastIndex+1), [*updateDict]] = [updateDict[ky] for ky in [*updateDict]]
            insert_entry_PDF.to_sql(
                db_table_name, sqlEngine, if_exists='append', index=True, index_label='id')
            msg = 'Table {} updated successfully'.format(db_table_name)
        else:
            msg = 'Insert columns'+', '.join(diffCols)+' not in table'
        return msg

    def bulk_update_table_entries(self, SQLengine, params):
        filterCols = params['filterCols']
        updateDataDictList = params['updateDictList']
        filterDict = {}
        for dct in updateDataDictList:
            filterDict = {ky: dct[ky] for ky in filterCols}
            msg = self.update_record(SQLengine, {
                                     'db_table_name': params['db_table_name'], 'filterDict': filterDict, 'updateDict': dct})
        return msg

    def bulk_delete_table_entries(self, SQLengine, params):
        deleteDataDictList = params['updateDictList']
        filterDict = {}
        for dct in deleteDataDictList:
            msg = self.delete_record(
                SQLengine, {'db_table_name': params['db_table_name'], 'filterDict': dct})
        return msg

    def bulk_insert_table_entries(self, SQLengine, params):
        updateDataDictList = params['updateDictList']
        for dct in updateDataDictList:
            msg = self.insert_record(
                SQLengine, {'db_table_name': params['db_table_name'], 'updateDict': dct})
        return msg

    def bulk_update_table_entries_with_logging(self, SQLengine, params):
        filterCols = params['filterCols']
        updateDataDictList = params['updateDictList']
        filterDict = {}
        for dct in updateDataDictList:
            filterDict = {ky: dct[ky] for ky in filterCols}
            msg = self.update_record(SQLengine, {
                                     'db_table_name': params['db_table_name'], 'filterDict': filterDict, 'updateDict': dct})
            dct[params['db_table_name']+'_updated_by'] = params['updatedBy']
            dct[params['db_table_name']+'_update_comment'] = params['updateComment']
            dct[params['db_table_name'] +
                '_updated_on'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            msg = self.insert_record(SQLengine, {
                                     'db_table_name': params['db_table_name']+'_update_history', 'updateDict': dct})
        return msg

    def bulk_delete_table_entries_with_logging(self, SQLengine, params):
        deleteDataDictList = params['updateDictList']
        filterDict = {}
        for dct in deleteDataDictList:
            msg = self.delete_record(
                SQLengine, {'db_table_name': params['db_table_name'], 'filterDict': dct})
            dct[params['db_table_name']+'_updated_by'] = params['updatedBy']
            dct[params['db_table_name']+'_update_comment'] = params['updateComment']
            dct[params['db_table_name'] +
                '_updated_on'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            msg = self.insert_record(SQLengine, {
                                     'db_table_name': params['db_table_name']+'_update_history', 'updateDict': dct})
        return msg

    def bulk_insert_table_entries_with_logging(self, SQLengine, params):
        updateDataDictList = params['updateDictList']
        for dct in updateDataDictList:
            msg = self.insert_record(
                SQLengine, {'db_table_name': params['db_table_name'], 'updateDict': dct})
            dct[params['db_table_name']+'_updated_by'] = params['updatedBy']
            dct[params['db_table_name']+'_update_comment'] = params['updateComment']
            dct[params['db_table_name'] +
                '_updated_on'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            msg = self.insert_record(SQLengine, {
                                     'db_table_name': params['db_table_name']+'_update_history', 'updateDict': dct})
        return msg

    def create_table_4m_csv_with_update_history(self, SQLengine, params):
        dataPDF = pd.read_csv(params['filePath'])
        tableName = params['db_table_name']
        print(tableName)
        dataPDF.to_sql(tableName, SQLengine, if_exists='replace',
                       index=True, index_label=tableName+'_id')
        dataPDF[tableName+'_update_comment'] = 'Entry created'
        dataPDF.to_sql(tableName+'_update_history', SQLengine, if_exists='replace',
                       index=True, index_label=tableName+'_update_history_id')
        return 'Tables {} and {} Created'.format(tableName, tableName+'_update_history')

    def create_table_4m_csv(self, SQLengine, params):
        dataPDF = pd.read_csv(params['filePath'])
        tableName = params['db_table_name']
        dataPDF.to_sql(tableName, SQLengine, if_exists='replace',
                       index=True, index_label=tableName+'_id')
        return 'Tables {} Created'.format(tableName)

    def create_DB_from_csv_directory(self, SQLengine, params):
        historyTablesPath = params['withHistoryTablesPath']
        tablesWithoutHistoryPath = params['withoutHistoryTablesPath']
        tableNamesWithHistory = os.listdir(historyTablesPath)
        tableNamesWithoutHistory = os.listdir(tablesWithoutHistoryPath)
        for flnm in tableNamesWithHistory:
            tableName = flnm.split('.')[0]
            self.create_table_4m_csv_with_update_history(
                SQLengine, {'db_table_name': tableName, 'filePath': historyTablesPath+flnm})
        for flnm in tableNamesWithoutHistory:
            dataPDF = pd.read_csv(tablesWithoutHistoryPath+flnm)
            tableName = flnm.split('.')[0]
            dataPDF.to_sql(tableName, SQLengine, if_exists='replace',
                           index=True, index_label=tableName+'_id')
        return 'DB Created'


def DataBaseAccessApp_fn(func):

    def inner1(a, b):
        c = func(a, b)
        return c

    return inner1


def DataBaseAccessApp(sqlEngine, inputDict):
    function_to_be_called = DataBaseAccessApp_fn(inputDict['functionName'])
    return function_to_be_called(sqlEngine, inputDict['functionParameters'])


def update_record(SQLengine, params):
    db_table_name = params['db_table_name']
    filterDict = params['filterDict']
    updateDict = params['updateDict']
    filterStrLst = [fltcol+'="{}"'.format(params['filterDict'][fltcol])
                    for fltcol in [*params['filterDict']]]
    filterStr = ' AND '.join(filterStrLst)
    numericFieldsInfoDict = updateDict['numericFieldsInfoDict']
    textFieldsInfoDict = updateDict['textFieldsInfoDict']

    if len(textFieldsInfoDict) != 0:
        sqlqText = "UPDATE {} SET ".format(db_table_name) + ', '.join([xx+"='{}'".format(
            textFieldsInfoDict[xx]) for xx in [*textFieldsInfoDict]])+" WHERE {}".format(filterStr)
        sqlqText = sqlqText.replace('\\', '\\\\')
        SQLengine.execute(sqlqText)
    if len(numericFieldsInfoDict) != 0:
        sqlqNumeric = "UPDATE {} SET ".format(db_table_name) + ', '.join([xx+"={}".format(
            numericFieldsInfoDict[xx]) for xx in [*numericFieldsInfoDict]])+" WHERE {}".format(filterStr)
        SQLengine.execute(sqlqNumeric)

    return 'Table {} updated successfully'.format(db_table_name)


def insert_record(sqlEngine, params):
    db_table_name = params['db_table_name']
    updateDict = params['updateDict']
    db_table_PDF = pd.read_sql(
        'SELECT * FROM {} WHERE id=(SELECT max(id) FROM {})'.format(db_table_name, db_table_name), sqlEngine)
    diffCols = set([*updateDict]).difference(set([*db_table_PDF]))
    if len(diffCols) == 0:
        lastIndex = db_table_PDF['id'].values[0]
        insert_entry_PDF = pd.DataFrame(
            columns=[*db_table_PDF], index=[int(lastIndex+1)]).drop(columns=['id'])
        insert_entry_PDF.loc[int(lastIndex+1), [*updateDict]
                             ] = [updateDict[ky] for ky in [*updateDict]]
        insert_entry_PDF.to_sql(db_table_name, sqlEngine,
                                if_exists='append', index=True, index_label='id')
        msg = 'Table {} updated successfully'.format(db_table_name)
    else:
        msg = 'Insert columns'+', '.join(diffCols)+' not in table'
    return msg

# Webservice Access Function Definitions
# The Call funtion


def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.

    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict == None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict


def call(accessParams, fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.

    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update(
        {"wstoken": accessParams['KEY'], 'moodlewsrestformat': 'json', "wsfunction": fname})
    response = post(
        accessParams['URL']+accessParams['ENDPOINT'], parameters, verify=False)
    response = response.json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response


# tealM-Python Moodle Access Functions
def get_course_modules(webserviceAccessParams, courseShortName):
    chosenContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
        'courses'] if crs['shortname'] == courseShortName][0]
    chosenContentID = chosenContentDict['id']
    contentModules = [{'sectionid': secn['id'], 'sectionname': secn['name'], 'sectionmodules': [{'id': mod['id'], 'name': mod['name'], 'modname': mod['modname'], 'contextid': mod['contextid'],
                                                                                                 'instance': mod['instance'], 'url': mod['url']} for mod in secn['modules']]} for secn in call(webserviceAccessParams, 'core_course_get_contents', courseid=chosenContentID)]
    return contentModules


def create_course_4m_moodle_template(params):
    print('create_course_4m_moodle_template')
    print(params)
    output = {}
    templateShortName = params['templateShortName']
    categoryName = params['categoryName']
    contentName = params['fullname']
    contentShortName = params['shortname']
    webserviceAccessParams = params['webserviceAccessParams']
    customFields = params['customfields']
    categoryInfo = [cat for cat in call(webserviceAccessParams, 'core_course_get_categories ', criteria=[
                                        {'key': 'name', 'value': categoryName}]) if cat['name'] == categoryName][0]
    categoryID = categoryInfo['id']

    templateContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=templateShortName)[
        'courses'] if crs['shortname'] == templateShortName][0]
    templateCourseID = templateContentDict['id']
    course2AddDict = call(webserviceAccessParams, 'core_course_get_courses', options={
                          'ids': [templateCourseID]})[0]
    for ky in ['id', 'categorysortorder', 'displayname', 'showactivitydates', 'showactivitydates', 'showcompletionconditions', 'timecreated', 'timemodified']:  # ,'lang']:
        try:
            del course2AddDict[ky]
        except:
            output['message'] = 'No {} in keys'.format(ky)

    course2AddDict['shortname'] = contentShortName
    course2AddDict['fullname'] = contentName
    course2AddDict['categoryid'] = categoryID
    course2AddDict['lang'] = 'en'
    # [{ky:course2AddDict['customfields'][0][ky] for ky in ['shortname','value']}]
    course2AddDict['customfields'] = customFields
    print(course2AddDict)
    reponse = call(webserviceAccessParams,
                   'core_course_create_courses', courses=[course2AddDict])
    createdCrsId = reponse[0]['id']
    output['created_content_id'] = createdCrsId
    call(webserviceAccessParams, 'core_course_import_course',
         importfrom=templateCourseID, importto=createdCrsId)
    output['crs_URL'] = webserviceAccessParams['URL'] + \
        '/course/view.php?id={}'.format(createdCrsId)
    output['crsModuleInfo'] = call(
        webserviceAccessParams, 'core_course_get_contents', courseid=createdCrsId)[0]['modules']
    output['message'] = 'Content created from template {}'
    return output


def manual_enroll_user_in_course(engine, webserviceAccessParams, courseShortName, userName, userRoleShortName):
    contentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
        'courses'] if crs['shortname'] == courseShortName][0]
    contentID = contentDict['id']

    userInfo = [usr for usr in call(webserviceAccessParams, 'core_user_get_users', criteria=[
                                    {'key': 'username', 'value': userName}])['users'] if usr['username'] == userName][0]
    userID = userInfo['id']
    roleID = pd.read_sql('SELECT id FROM mdl_role WHERE shortname="{}"'.format(
        userRoleShortName), engine)['id'].values[0]  # TEAL2.O Teacher
    enrolmentList = [{'courseid': contentID,
                      'userid': userID, 'roleid': roleID}]

    return call(webserviceAccessParams, 'enrol_manual_enrol_users', enrolments=enrolmentList)


def course_content_GitHub_push(webserviceAccessParams, mgGH, SQLengine, parameters):
    # parameters={'access_parameters':{'gToken':githubToken, 'gUser':contentOrganization}, 'repoName':chosenContentShortname, 'updateComment':updateComment}
    contentShortName = parameters['repoName']  # .lower()
    chosenContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=contentShortName)[
        'courses'] if crs['shortname'] == contentShortName][0]
    contentMetaDataSummaryJSON = json.dumps(chosenContentDict, indent=2)
    parameters['fileInfoDict'] = {
        'filename': 'contentMetaDataSummary.json', 'filecontent': contentMetaDataSummaryJSON}
    create_update_GITHUB_organization_repos(mgGH, parameters)
    chosenContentId = chosenContentDict['id']

    chosenContentFullDict = call(
        webserviceAccessParams, 'core_course_get_courses', options={'ids': [chosenContentId]})
    contentMetaDataJSON = json.dumps(chosenContentFullDict, indent=2)
    parameters['fileInfoDict'] = {
        'filename': 'contentMetaData.json', 'filecontent': contentMetaDataJSON}
    create_update_GITHUB_organization_repos(mgGH, parameters)

    chosenContentSecns = call(
        webserviceAccessParams, 'core_course_get_contents', courseid=chosenContentId)
    contentSecnsJSON = json.dumps(chosenContentSecns, indent=2)
    parameters['fileInfoDict'] = {
        'filename': 'contentSecnsSummary.json', 'filecontent': contentSecnsJSON}
    msg = create_update_GITHUB_organization_repos(mgGH, parameters)

    for section in [{'id': secn['id'], 'name': secn['name'], 'modules': secn['modules']} for secn in call(webserviceAccessParams, 'core_course_get_contents', courseid=chosenContentId)]:
        for module in section['modules']:
            fileDict = pd.read_sql('SELECT * FROM mdl_{} WHERE id={}'.format(
                module['modname'], module['instance']), SQLengine).to_dict(orient='records')[0]

            if module['modname'] == 'hvp':
                mainLibraryID = fileDict['main_library_id']
                fileDict['main_library_id'] = pd.read_sql(
                    'SELECT * FROM mdl_hvp_libraries WHERE id={}'.format(mainLibraryID), SQLengine).to_dict(orient='records')[0]

            fileJSON = json.dumps(fileDict, indent=2)
            # parametersV2={'moduleType':'hvp','access_parameters':parameters['access_parameters'], 'repoName':contentShortName, 'fileInfoDict':{'filename':'section_'+str(section['id'])+'_content/'+module['modname']+'.json', 'filecontent':fileJSON}, 'updateComment':parameters['updateComment']}
            parametersV2 = {'access_parameters': parameters['access_parameters'], 'repoName': contentShortName, 'fileInfoDict': {'filename': 'section_'+str(section['id'])+'_content/'+'mod_'+str(
                module['id'])+'_'+module['modname']+'_'+str(module['instance'])+'.json', 'filecontent': fileJSON}, 'updateComment': parameters['updateComment']}
            msg = create_update_GITHUB_organization_repos(mgGH, parametersV2)

    return msg


def create_course_categories_moodle(webserviceAccessParams, categoryStructureDict):
    response = []
    category_structure_PDF = pd.DataFrame(categoryStructureDict)
    categoryLevels = [*category_structure_PDF]
    categoryIds = {}
    proviousLevel = []
    previousLevel = ''
    for level in categoryLevels:
        levelCategoryData = []
        catGps = list(set(category_structure_PDF[level].to_list()))
        catGps.sort()
        for catName in catGps:
            if level == categoryLevels[0]:
                parentId = 0
            else:
                parentLevel = list(set(
                    category_structure_PDF[category_structure_PDF[level] == catName][previousLevel].to_list()))[0]
                parentId = categoryIds[parentLevel]
            levelCategoryData.append({'name': catName, 'idnumber': '', 'description': '',
                                     'descriptionformat': 1, 'parent': parentId, 'theme': ''})
        # print(levelCategoryData)
        resp = call(webserviceAccessParams,
                    'core_course_create_categories', categories=levelCategoryData)
        for dct in resp:
            categoryIds[dct['name']] = dct['id']

        previousLevel = level
        response.append(resp)
    return


def delete_course_categories_moodle(webserviceAccessParams, idList):
    deleteCategories = [{'id': id, 'recursive': 1} for id in idList]
    resp = call(webserviceAccessParams,
                'core_course_delete_categories', categories=deleteCategories)
    return resp

# Course specification creation functions


def update_moodle_course_info_4m_course_db(SQLengine, webserviceAccessParams, courseCode4mTable):
    content2BUpdatedShortname = courseCode4mTable
    chosenContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=content2BUpdatedShortname)[
        'courses'] if crs['shortname'] == content2BUpdatedShortname][0]
    contentReplacingid = chosenContentDict['id']
    contentReplacingContents = call(
        webserviceAccessParams, 'core_course_get_contents', courseid=contentReplacingid)
    contentReplacing_hvpModules = [
        mod for secn in contentReplacingContents for mod in secn['modules'] if mod['modname'] == 'hvp']
    chosenhvpModuleID = contentReplacing_hvpModules[0]['instance']
    moduleInfoDict = pd.read_sql('SELECT * FROM mdl_hvp WHERE id={}'.format(
        chosenhvpModuleID), engine).to_dict(orient='records')
    # print(moduleInfoDict[0]['filtered'])
    json_content = moduleInfoDict[0]['json_content']
    filtered = moduleInfoDict[0]['json_content']  # ['filtered']
    parameters = {'courseCode4mTable': courseCode4mTable,
                  'filtered': filtered, 'json_content': json_content}
    # print(parameters)
    updatedJSONSDict = course_table_2_hvp_accordion(SQLengine, parameters)
    params = {}
    params['db_table_name'] = 'mdl_hvp'
    params['filterDict'] = {'id': chosenhvpModuleID}
    params['updateDict'] = {'numericFieldsInfoDict': {}, 'textFieldsInfoDict': {
        'name': content2BUpdatedShortname, 'filtered': updatedJSONSDict['filtered'], 'json_content': updatedJSONSDict['json_content']}}
    return update_record(SQLengine, params)


def create_course_4m_course_db(SQLengine, webserviceAccessParams, courseCode4mTable, templateShortName, userEmail):
    courseName = pd.read_sql('SELECT course_name FROM course WHERE course_code="{}"'.format(
        courseCode4mTable), engine)['course_name'].to_list()[0]
    # pd.read_sql('SELECT CAH3_skill_classification FROM course WHERE course_code="{}"'.format(courseCode4mTable),SQLengine)['CAH3_skill_classification'].to_list()[0]
    categoryName = 'Demo sub'
    params = {'webserviceAccessParams': webserviceAccessParams, 'templateShortName': templateShortName, 'categoryName': categoryName,
              'contentName': courseName, 'contentShortName': courseCode4mTable, 'customFields': [{'shortname': 'author', 'value': userEmail}]}
    output = create_course_4m_moodle_template(params)
    update_moodle_course_info_4m_course_db(
        SQLengine, webserviceAccessParams, courseCode4mTable)
    return output


def course_table_2_hvp_accordion(SQLengine, parameters):
    courseCode = parameters['courseCode4mTable']
    # print(courseCode)
    filtered = parameters['filtered']
    json_content = parameters['json_content']
    chosen_course_info_dict = pd.read_sql(
        'SELECT * FROM course WHERE course_code="{}"'.format(courseCode), SQLengine).to_dict(orient='records')[0]
    json_content_dict = json.loads(json_content)
    filtered_dict = json.loads(filtered)
    # print(json_content_dict)
    json_content_panelNames = {
        panel['title']: ip for ip, panel in enumerate(json_content_dict['panels'])}
    filtered_panelNames = {panel['title']: ip for ip,
                           panel in enumerate(filtered_dict['panels'])}
    panel2dbtablemap = {'CAH3 Skill Classification': 'CAH3_skill_classification', 'Total Number of Credits': 'course_credits',
                        'Objective': 'course_objective', 'Author': 'course_updated_by'}
    for chosenPanelName in [*panel2dbtablemap]:
        filtered_dict['panels'][filtered_panelNames[chosenPanelName]]['content']['params']['text'] = '<p>{}</p>'.format(
            chosen_course_info_dict[panel2dbtablemap[chosenPanelName]])
        json_content_dict['panels'][json_content_panelNames[chosenPanelName]
                                    ]['content']['params']['text'] = '<p>{}</p>'.format(chosen_course_info_dict[panel2dbtablemap[chosenPanelName]])
    chosenPanelName = 'Depth Level'
    filtered_dict['panels'][filtered_panelNames[chosenPanelName]]['content']['params']['text'] = '<p>SOLO Level={}</p>\n <p>BLOOMS Level={}</p>'.format(
        chosen_course_info_dict['SOLO_level'], chosen_course_info_dict['BLOOMS_level'])
    json_content_dict['panels'][json_content_panelNames[chosenPanelName]]['content']['params']['text'] = '<p>SOLO Level={}</p>\n <p>BLOOMS Level={}</p>'.format(
        chosen_course_info_dict['SOLO_level'], chosen_course_info_dict['BLOOMS_level'])
    xx1 = []
    for icr, cr in enumerate(chosen_course_info_dict['credit_to_ILO_map'].split(',')):
        xx1.append('<li>ILO{}: (CR-{}) {}</li>'.format(icr+1,
                   cr.replace(' ', ''), chosen_course_info_dict['ILO'+str(icr+1)]))
    chosenPanelName = 'Intended Learning Outcomes (ILOs)'
    filtered_dict['panels'][filtered_panelNames[chosenPanelName]
                            ]['content']['params']['text'] = '<ul>\n'+'\n '.join(xx1)+'</ul>'
    json_content_dict['panels'][json_content_panelNames[chosenPanelName]
                                ]['content']['params']['text'] = '<ul>\n'+'\n '.join(xx1)+'</ul>'
    return {'json_content': json.dumps(json_content_dict), 'filtered': json.dumps(filtered_dict)}
