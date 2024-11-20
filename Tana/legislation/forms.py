#!/usr/bin/python3
"""forms for the legislation"""
from flask_wtf import FlaskForm
from wtforms import StringField,DateField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Optional

class MotionsForm(FlaskForm):
    """Motions form"""
    name = StringField('Name', validators=[DataRequired()])
    document = FileField('Document', validators=[Optional()])
    follow_up_document = FileField('Follow-up Document', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')


class StatementsForm(FlaskForm):
    name = StringField('Statement Title', validators=[DataRequired()])
    document = FileField('Upload Document')  # Document is not required for edits
    follow_up_letter = FileField('Follow-Up Letter')  # New optional field for follow-up letter
    date = DateField('Statement Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Statement Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class LegislationForm(FlaskForm):
    """Legislation form"""
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class QuestionsForm(FlaskForm):
    """Questions form"""
    name = StringField('Name', validators=[DataRequired()])
    document = FileField('Document', validators=[Optional()])
    follow_up_document = FileField('Follow-Up Document')  # Add this line
    date = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')
