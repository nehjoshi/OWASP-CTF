from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class signup(FlaskForm):
    uname=StringField('Username')
    email=EmailField('Email id')
    password=PasswordField('Password')
    submit=SubmitField('Submit')

class loginf(FlaskForm):
    email=EmailField('Email id')
    password=PasswordField('Password')
    submit = SubmitField('Submit')

class password(FlaskForm):
    email=EmailField('Email id')