#!/bin/usr/python3
"""Forms module for the users"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DateTimeField,Field, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Tana.models.members import users
from flask_login import current_user, UserMixin, login_user, logout_user, login_required, LoginManager
from flask_wtf.file import FileField, FileAllowed
from Tana import bcrypt, db_storage
from Tana.models.roles import UserRole
from datetime import date


# create a class to register a user by admin

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10, message="Phone number must be 10 digits")], render_kw={"placeholder": "07xxxxxxxx"})
    ID_No = IntegerField('ID Number', validators=[DataRequired()])
    
    role = SelectField('Role', choices=[
        (UserRole.ADMIN.value, 'Admin'),
        (UserRole.P_A.value, 'Personal Assistant'),
        (UserRole.SUPER_ADMIN.value, 'Super Admin'),
        (UserRole.DRIVER.value, 'Driver'),
        (UserRole.BODYGUARD.value, 'Bodyguard'),
        (UserRole.RESEARCHER.value, 'Researcher'),
        (UserRole.COORDINATOR.value, 'Coordinator'),
        (UserRole.SECRETARY.value, 'Secretary'),
        (UserRole.CHIEF_SECURITY_OFFICER.value, 'Chief Security Officer'),
        (UserRole.CHIEF_FIELD_OFFICER.value, 'Chief Field Officer'),
        (UserRole.FIELD_OFFICER.value, 'Field Officer'),
        (UserRole.OTHER.value, 'Other')
    ], validators=[DataRequired()])
    
    office_id = StringField('Office ID')  # Adjust as needed
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = db_storage.get_user_by_email(email.data)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_ID_No(self, ID_No):
        user = db_storage.get_user_by_id(ID_No.data)
        if user:
            raise ValidationError('That ID Number is taken. Please choose a different one.')
class UpdateAccountForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db_storage.get(users, email=email.data)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            

class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = db_storage.get(users, email=email.data)
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = db_storage.get_user_by_email(email.data)
        if user is None:
            raise ValidationError('That email is not registered. Please register first.')
#class for employee register

class EmployeeRegisterForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    time_in = StringField('Time In', validators=[DataRequired()], render_kw={"placeholder": "HH:MM"})
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[('present', 'Present'), ('absent', 'Absent'), ('leave', 'On Leave')], validators=[DataRequired()])
    submit = SubmitField('Register')

class FileUploadForm(FlaskForm):
    polling_station = StringField('Polling Station', validators=[DataRequired()])
    ward = StringField('Ward', render_kw={'readonly': True})
    constituency = StringField('Constituency', render_kw={'readonly': True})
    file = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DiaryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    content = StringField('Content', validators=[DataRequired(), Length(max=128)])
    entry_date = DateField('Entry Date', format='%Y-%m-%d', validators=[DataRequired()], default=date.today)


class DeleteForm(FlaskForm):
    pass
