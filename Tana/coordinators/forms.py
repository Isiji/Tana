from flask_wtf import FlaskForm
from wtforms import DateField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CountyOfficeUpdateForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    party_involved = StringField('Party Involved', validators=[DataRequired()])
    issues = TextAreaField('Issues', validators=[DataRequired()])
    delegation = StringField('Delegation', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    action_taken = TextAreaField('Action Taken', validators=[DataRequired()])
    submit = SubmitField('Submit')
