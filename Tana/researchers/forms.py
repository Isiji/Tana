from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommitteeRecordForm(FlaskForm):
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    document = FileField('Document')
    recommendations = FileField('Recommendations')
    submit = SubmitField('Submit')
    
    
class CommitteeForm(FlaskForm):
    name = StringField('Committee Name', validators=[DataRequired()])
    submit = SubmitField('Add Committee')
