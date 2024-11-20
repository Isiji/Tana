#!/usr/bin/python3
""" forms for the main"""
from flask_wtf import FlaskForm, Form, RecaptchaField
from wtforms import PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from flask_login import current_user, UserMixin, login_user, logout_user, login_required, LoginManager
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileStorage, FileField
from Tana.models.offices import Offices
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField

