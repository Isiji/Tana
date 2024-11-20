from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, Email

class FolderForm(FlaskForm):
    folder_name = StringField('Folder Name', validators=[DataRequired()])
    submit = SubmitField('Create Folder')


class ReportDataForm(FlaskForm):
    name = StringField('Report Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    report_file = FileField('Upload Report', validators=[DataRequired()])
    date_report_uploaded = DateField('Date Report Uploaded', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Add Report')
