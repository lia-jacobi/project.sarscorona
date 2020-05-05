"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DemoFormProject import app
from DemoFormProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines



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

def get_states_choices():
    df_short_state = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/SARS1.csv'))
    df1 = df_short_state.groupby('Country').sum()
    l = df1.index
    m = list(zip(l , l))
    return m


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'home.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )




@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
    )


@app.route('/data')
def data():
    """Renders the about page."""
    return render_template(
        'data.html',
        title='data',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
    )







# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
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
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )


@app.route('/corona')
def corona():
    """Renders the about page."""

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/CORONA1.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template(
        'corona.html',
        raw_data_table = raw_data_table,
        title='corona',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
    )

@app.route('/sars')
def sars():
    """Renders the about page."""

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/SARS1.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template(
        'sars.html',
        raw_data_table = raw_data_table,
        title='sars',
        year=datetime.now().year,
        message='Explanation about the project and about the tools I used to write this project'
        )


@app.route('/query', methods=['GET', 'POST'])
def query():
    form = DataQueryFormStructure(request.form)
    
  
  
    #Set the list of states from the data set of all US states
    form.states.choices = get_states_choices() 
   

     
    if (request.method == 'POST' ):

        print('hello')
    

    return render_template('query.html', 
            form = form, 
            raw_data_table = "",
            fig_image = "",
            title='User Data Query',
            year=datetime.now().year,
            message='Please enter the parameters you choose, to analyze the database'
        )
