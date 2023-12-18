# globals are the varibles derivated from static globals
from fns import *
from static_globals import *
from pandas.io import sql
from sqlalchemy import *
import os
from github import Github
import json
import pandas as pd
import csv
import plotly.graph_objects as go
from csv import DictWriter
import datetime
import smtplib
import datetime

import mysql.connector
import sqlalchemy

import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)


engineContent = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(
    userContent, passwordContent, hostContent, dbnameContent))
engineCourse = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(
    userCourse, passwordCourse, hostCourse, dbnameCourse))


mgGH = tealMGitHub()
mgDB = mugas_DB_functions()


allCategories = call(webserviceAccessParamsContent,
                     'core_course_get_categories')
listCategory = [cat['name'] for cat in allCategories if cat['depth'] == 3]
listCategory.sort()


taxonomyPDF = pd.read_csv('datafolder/SOLO_BLOOMS_Taxonomy.csv').fillna("")
