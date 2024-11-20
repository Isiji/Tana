#!/usr/bin/python3
"""Forms for the oversight"""
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField, StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional

class OversightForm(FlaskForm):
    """Oversight form"""
    name = StringField('report name', validators=[DataRequired()] )
    OAG_Report = FileField('OAG Report', validators=[Optional()])
    date_updated = DateField('Date Updated', validators=[DataRequired()])
    Ground_report = TextAreaField('Ground Report', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit')
