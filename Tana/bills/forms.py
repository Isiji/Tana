#!/usr/bin/python3
"""Forms for the bills"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, DateField, BooleanField
from wtforms.validators import DataRequired, Optional

class BillsForm(FlaskForm):
    """Form for adding bills"""
    name = StringField('Bill Name', validators=[DataRequired()])
    submitted_date = DateField('Submitted Date', validators=[DataRequired()])
    first_reading = BooleanField('First Reading')
    first_reading_date = DateField('First Reading Date', validators=[Optional()])
    second_reading = BooleanField('Second Reading')
    second_reading_date = DateField('Second Reading Date', validators=[Optional()])
    third_reading = BooleanField('Third Reading')
    third_reading_date = DateField('Third Reading Date', validators=[Optional()])
    presidential_assent = BooleanField('Presidential Assent')
    presidential_assent_date = DateField('Presidential Assent Date', validators=[Optional()])
    commencement = BooleanField('Commencement')
    commencement_date = DateField('Commencement Date', validators=[Optional()])
    document = FileField('Document', validators=[Optional()])
    submit = SubmitField('Submit')

class Emptyform(FlaskForm):
    """Empty form"""
    pass