# Description: Routes for handling reminders in the application.
from flask import current_app, Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from Tana.models.reminder import Reminder
from Tana.reminder.forms import ReminderForm
from Tana import db_storage, mail
from datetime import datetime
from flask_mail import Message

reminders = Blueprint('reminders', __name__)

# route for adding a reminder
@reminders.route('/add_reminder', methods=['GET', 'POST'])
@login_required
def add_reminder():
    """Route for adding a reminder"""
    form = ReminderForm()
    
    if form.validate_on_submit():
        reminder_datetime = datetime.combine(form.reminder_date.data, form.reminder_time.data)
        if reminder_datetime <= datetime.now():
            flash('Reminder date and time must be in the future.', 'danger')
            return redirect(url_for('reminders.add_reminder'))
        
        reminder = Reminder(
            reminder_name=form.reminder_name.data,
            reminder_description=form.reminder_description.data,
            reminder_date=form.reminder_date.data,
            reminder_time=form.reminder_time.data,
            user_id=current_user.id
        )
        db_storage.new(reminder)
        db_storage.save()
        
        # Flash in-app success message
        flash('Reminder set successfully', 'success')
        
        # Send email notification
        send_reminder_email(current_user.email, reminder)
        
        # Redirect to avoid form resubmission on page refresh
        return redirect(url_for('reminders.add_reminder'))

    # Fetch all reminders for the current user
    user_reminders = db_storage.get_session().query(Reminder).filter_by(user_id=current_user.id).all()

    return render_template('reminders.html', title='Reminders', form=form, reminders=user_reminders)

# Define the route for sending a reminder  
def send_reminder_email(user_email, reminder):
    """Send email notification for a new reminder"""
    msg = Message('New Reminder Set', sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[user_email])
    msg.body = f"Hello,\n\nYou have set a new reminder '{reminder.reminder_name}' for {reminder.reminder_date} at {reminder.reminder_time}.\n\nBest regards,\nYour App Team"
    try:
        mail.send(msg)
        print("Reminder email sent successfully.")
    except Exception as e:
        print(f"Failed to send reminder email: {e}")
        current_app.logger.error(f"Failed to send reminder email: {e}") 