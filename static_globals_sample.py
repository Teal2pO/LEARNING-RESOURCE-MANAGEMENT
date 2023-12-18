# Server address
serverURL = "ADD_MAIN_SERVER_URL"
# App prefixes for URL generation and names
appPrefixname = "teal"
appPrefixNAME = "TEAL"


# ===============================Moodle data===============================
# content moodle
# Use https if SSL enabled in the server
siteURL = "https://127.0.0.1/{}_content".format(appPrefixname)
siteURLpublicContent = "{}/{}_content".format(serverURL, appPrefixname)
KEY = "ADD_THE_KEY"
URL = siteURL
ENDPOINT = "/webservice/rest/server.php"
webserviceAccessParamsContent = {
    'KEY': KEY, 'URL': siteURL, 'ENDPOINT': ENDPOINT}


# course moodle
siteURL = "https://127.0.0.1/{}_course".format(appPrefixname)
siteURLpublicCourse = "{}/{}_course".format(serverURL, appPrefixname)
KEY = "ADD_THE_KEY"
URL = siteURL
ENDPOINT = "/webservice/rest/server.php"
webserviceAccessParamsCourse = {
    'KEY': KEY, 'URL': siteURL, 'ENDPOINT': ENDPOINT}

# Classroom moodle hosted in the application server
siteURL = "https://127.0.0.1/{}_classroom".format(appPrefixname)
siteURLpublicClassroom = "{}/{}_classroom".format(serverURL, appPrefixname)
KEY = "ADD_THE_KEY"
ENDPOINT = "/webservice/rest/server.php"
webserviceAccessParamsClassroom_SERVER = {
    'KEY': KEY, 'URL': siteURL, 'PURL': siteURLpublicClassroom, 'ENDPOINT': ENDPOINT}


# ==========================Database connections=========================
# Database connection details to app to interact with database
# This should be the same database used by the moodle in siteURL

# content moodle
hostContent = "127.0.0.1"
portContent = 3306
dbnameContent = "DB_NAME"  # Ex: teal_content_db
userContent = "USER_NAME"
passwordContent = "ADD_PASSWORD"

# courses moodle
hostCourse = "127.0.0.1"
portCourse = 3306
dbnameCourse = "DB_NAME"
userCourse = "USER_NAME"
passwordCourse = "ADD_PASSWORD"

# classroom moodle in the application server - (Standard)
hostClassroom_SERVER = "127.0.0.1"
portClassroom_SERVER = 3306
dbnameClassroom_SERVER = "DB_NAME"
userClassroom_SERVER = "USER_NAME"
passwordClassroom_SERVER = "ADD_PASSWORD"


# -----------DB used by the program_course application------------
# courses app db
hostCourseApp = "127.0.0.1"
portCourseApp = 3306
dbnameCourseApp = "{}_courseAppDb".format(appPrefixname)
userCourseApp = "{}_courseAppUsr".format(appPrefixname)
passwordCourseApp = "ADD_PASSWORD"

# ==========================Linked Github repo details (content and course)=================

# Github login details to app to interact with github
githubToken = 'ADD_TOKEN' 
content_githubUser = "ADD_USER"
course_githubUser = "ADD_USER"

# ==========================Varibles for the web API (Do not change)====================
templateHVPcontent = 'template_interactive_book_hvp'
templateClassroom = 'template_classroom'
templateCourseSpecifications = 'template_course_specification'
# Teacher
limitedEditingTeacher = 'teal2oteacher'
EditingTeacher = 'editingteacher'
# =========================Admin emails specify here=======================
# Any email inside this list alowed to update all courses
adminEmails = ['admin@admin.com']
