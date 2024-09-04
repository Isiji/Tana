#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional

class MinistriesForm(FlaskForm):
    name = StringField('Ministry Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    documents_presented = TextAreaField('Documents Presented', validators=[DataRequired()])
    date_documents_presented = DateField('Date Documents Presented', format='%Y-%m-%d', validators=[DataRequired()])


