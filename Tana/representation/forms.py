#!/usr/bin/python3
"""Forms module for the representation"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
