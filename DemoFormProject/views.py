"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DemoFormProject import app
from DemoFormProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, mpld3

from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
import io

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
from wtforms import StringField, PasswordField, HiddenField, SubmitField
from wtforms import IntegerField, DecimalField, FloatField, RadioField, BooleanField


from DemoFormProject.Models.QueryFormStructure import DataQueryFormStructure 
from DemoFormProject.Models.QueryFormStructure import LoginFormStructure 
from DemoFormProject.Models.QueryFormStructure import UserRegistrationFormStructure 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 

#פונקציה שמקבלת  מקובץ הדאטה שלי את רשימת המדינות שניתן יהיה לבחור מהן
def get_states_choices():
    df_short_state = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/SARS1.csv'))
    df1 = df_short_state.groupby('Country').sum()
    l = df1.index
    m = list(zip(l , l))
    return m


#עמוד הבית, המסך הראשון שהמשתמש רואה עם מידע כללי
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'home.html',
        title='Home Page',
        year=datetime.now().year,
    )

#פרטי הקשר שלי
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )



#עמוד ובו כתוב איך כתבתי את הפרויקט, באיזה מסגרת ובאיזה שפות וכלים השתמשתי
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
    )


#עמוד המכיל מידע כללי על הדאטה שלי, בתוכו יש דרך לעבור לשני עמודים אחרים שמכילים הם את קבצי הדאטה
@app.route('/data')
def data():
    """Renders the data page."""
    return render_template(
        'data.html',
        title='data',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
    )







# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
#עמוד בו המשתמש יכול להרשם לאתר שלי
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            return redirect('query')
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )
 
# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
#עמוד בו המשתמש נכנס עם שם המשתמשוהסיסמא שלו לאתר
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )


#עמוד שמכיל את קובץ הדאטה שבתוכו מספר החולים ומספר המתים מקורונה בכל מדינה
@app.route('/corona')
def corona():
    """Renders the corona page."""

    df = pd.read_excel(path.join(path.dirname(__file__), 'static/Data/CORONA.xlsx'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template(
        'corona.html',
        raw_data_table = raw_data_table,
        title='corona',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
    )

#עמוד שמכיל את קובץ הדאטה שבתוכו מספר החולים ומספר המתים מסארס בכל מדינה
@app.route('/sars')
def sars():
    """Renders the sars page."""

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/SARS1.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template(
        'sars.html',
        raw_data_table = raw_data_table,
        title='sars',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
        )


#דף הקוורי, המשתמש בוחר מדינות ולאחר מכן מקבל שני גרפים אחד מהגרפים על מספר מקרי מוות מקורונה והשני מסארס
@app.route('/query', methods=['GET', 'POST'])
def query():
    form = DataQueryFormStructure(request.form)
    chart1=""
    chart2=""
  
    #Set the list of states from the data set of all US states
    form.states.choices = get_states_choices() 

    #sars plot 
    if (request.method == 'POST' ):
        df_SARS=  pd.read_csv(path.join(path.dirname(__file__), 'static/Data/SARS1.csv'))
        l=df_SARS['Country']
        country_choices=list(zip(l,l))
        country_list= form.states.data
        df_SARS=df_SARS.set_index('Country')
        df_SARS=df_SARS.loc[country_list]
        df_cases=df_SARS
        df_cases['sars']=df_SARS['total cases ']
        df_cases=df_cases.drop('total cases ', 1)
        df_cases=df_cases.drop('total deaths ', 1)

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
 
        df_cases.plot(ax=ax1, kind='bar', color="black") 
        chart1 = mpld3.fig_to_html(fig1)

        
        #corona plot
        df_CORONA = pd.read_excel(path.join(path.dirname(__file__), 'static/Data/CORONA.xlsx'))
        counrtries = df_CORONA['Country,']
        country_list = form.states.data
        df_CORONA=df_CORONA.set_index('Country,')
        df_CORONA=df_CORONA.loc[country_list]
        df_corona_cases=df_CORONA
      
        df_corona_cases['corona']=df_CORONA['Total Cases']
        df_corona_cases=df_corona_cases.drop('Total Cases', 1)
        df_corona_cases=df_corona_cases.drop('Total deaths', 1)
        df_corona_cases = df_corona_cases.astype(float)
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)

        df_corona_cases.plot(ax=ax2, kind='bar',  color="black")
        chart2 = mpld3.fig_to_html(fig2)
     
    return render_template('query.html', 
            form = form, 
            raw_data_table = "",
            chart1=chart1,
            chart2=chart2,
            title='User Data Query',
            year=datetime.now().year,
            message='Please enter the parameters you choose, to analyze the database'
        )

#פעולה שמעבירה את הפלוט לתמונה
def plot_to_img(fig):
    pngImage= io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64, "
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String