from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FileField
from wtforms.validators import DataRequired, Optional

class MinistryForm(FlaskForm):
    name = StringField('Ministry Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    documents_presented = FileField('Upload Documents', validators=[Optional()])
    date_documents_presented = DateField('Date Documents Presented', validators=[DataRequired()])
