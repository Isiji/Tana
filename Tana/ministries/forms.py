from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired

class MinistryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email')
    documents_presented = FileField('Documents Presented')
    date_documents_presented = DateField('Date Documents Presented', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Ministry')
