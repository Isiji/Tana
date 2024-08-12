#!/usr/bin/python3
"""forms for the events"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired
from Tana.models.events import Events
from Tana import db_storage

# create a class to register an event
class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_description = TextAreaField('Event Description', validators=[DataRequired()])
    impact_level = SelectField('Impact Level', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired()])
    event_leader = StringField('Event Leader', validators=[DataRequired()])
    event_location = StringField('Event Location', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    polling_station_name = SelectField('Polling Station', validators=[DataRequired()], choices=[])
    submit = SubmitField('Register Event')


# create a form to view events that have been created
