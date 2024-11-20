from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime, date, time

class ReminderForm(FlaskForm):
    reminder_name = StringField('Reminder Name', validators=[DataRequired()])
    reminder_description = TextAreaField('Reminder Description', validators=[DataRequired()])
    reminder_date = DateField('Reminder Date', format='%Y-%m-%d', validators=[DataRequired()])
    reminder_time = TimeField('Reminder Time (24hr format)', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Set Reminder')

    def validate_reminder_date(self, reminder_date):
        if reminder_date.data < date.today():
            raise ValidationError('Reminder date must be in the future.')

    def validate_reminder_time(self, reminder_time):
        if self.reminder_date.data == date.today() and reminder_time.data <= datetime.now().time():
            raise ValidationError('Reminder time must be in the future if set for today.')
