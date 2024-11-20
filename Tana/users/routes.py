#!/usr/bin/env python3
"""Users route for the users"""
import os
from flask import Blueprint, session, jsonify, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana.engine.storage import DBStorage
from Tana.users.forms import UpdateAccountForm, ResetRequestForm, LoginForm,ResetPasswordForm, RegistrationForm, DeleteForm, EmployeeRegisterForm
from flask_login import current_user, login_required, login_user, logout_user
from Tana import bcrypt, db_storage, allowed_file
from Tana.models.employee_register import EmployeeRegister
from Tana.users.forms import DiaryForm, FileUploadForm
from Tana.models.pollingstation import PollingStation
from Tana.models.ward import Ward
from Tana.models.constituency import Constituency
from werkzeug.utils import secure_filename
from Tana.models.offices import Offices
import logging
from datetime import datetime, date
from Tana.models.diary import Diary
from flask_mail import Message
from Tana import mail, create_app
from Tana.users.utils import generate_token, validate_token, hash_password

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Users = Blueprint('Users', __name__)

# create a route for homepage
@Users.route('/')
@Users.route('/home')
def home():
    """homepage route for the user"""
    return render_template('home.html')

# create route for user to update user information
@Users.route('/account', methods=['GET', 'POST'])
def account():
    """account route for the user"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        db_storage = DBStorage()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db_storage.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('Users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


#route for user registration

@Users.route('/register/<int:office_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def register(office_id):
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users.create_user(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
            ID_No=form.ID_No.data,
            role=form.role.data,
            office_id=office_id
        )
        db_storage.new(user)
        db_storage.save()
        flash('User registered successfully.', 'success')
        return redirect(url_for('offices.office_details', office_id=office_id))
    return render_template('register.html', title='Register User', form=form)

@Users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#route for employee register using employee register form
@Users.route('/employee_register', methods=['GET', 'POST'])
@login_required
def employee_register():
    form = EmployeeRegisterForm()

    if request.method == 'GET':
        # Pre-fills the form with current user info
        form.user_id.data = current_user.id
        form.name.data = current_user.name
        form.date.data = datetime.now().date()
        form.time_in.data = datetime.now().strftime('%H:%M')

    if form.validate_on_submit():
        try:
            user_id = form.user_id.data
            name = form.name.data
            time_in = form.time_in.data
            date = form.date.data
            status = form.status.data

            # Create a new EmployeeRegister object
            new_employee = EmployeeRegister(
                user_id=user_id,
                name=name,
                time_in=time_in, 
                date=date,
                status=status
            )
            
            # Add and commit the new employee to the database
            db_storage.new(new_employee)
            db_storage.save()

            # Send email notification
            msg = Message('Register Marked',
                          sender='tanarivercountysenateoffice@gmail.com',  # Replace with your email
                          recipients=['wandedanton@gmail.com', 'mungatana47@gmail.com'])  # Replace with recipient email
            msg.body = f"""
            An employee has marked their register.:

            Name: {name}
            User ID: {user_id}
            Time In: {time_in}
            Date: {date}
            Status: {status}
            """
            mail.send(msg)

            flash('registered successfully and notification sent!', 'success')
            return redirect(url_for('Users.employee_records'))
        except Exception as e:
            logging.error(f"Error registering employee: {e}")
            flash('An error occurred while registering the employee. Please try again.', 'danger')

    return render_template('employee_register.html', title='Employee Register', form=form)

#route for getting all employee records
@Users.route('/employee_records', methods=['GET'])
@login_required
def employee_records():
    """Route to display employee records"""
    name_filter = request.args.get('name', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    status_filter = request.args.get('status', '')

    employees = db_storage.all(EmployeeRegister).values()

    # Debugging: Print initial employees list
    print("All Employees:", employees)

    if name_filter:
        employees = [e for e in employees if name_filter.lower() in e.name.lower()]
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        employees = [e for e in employees if e.date >= start_date]

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        employees = [e for e in employees if e.date <= end_date]

    if status_filter:
        # Debugging: Print status filter and matching employees
        print("Status Filter:", status_filter)
        employees = [e for e in employees if e.status.lower() == status_filter.lower()]
        print("Filtered Employees by Status:", employees)

    # Sort employees by date (most recent first)
    employees = sorted(employees, key=lambda e: e.date, reverse=True)

    # Debugging: Print final filtered employees list
    print("Final Filtered Employees:", employees)

    return render_template('employee_records.html', title='Employee Records', employees=employees)

#route for uploading a document
@Users.route('/upload', methods=['GET', 'POST'])
def upload():
    """ Route to upload a file """
    form = FileUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Process the file and populate database
            flash('File uploaded successfully', 'success')
            return redirect(url_for('Users.upload'))
        else:
            flash('Invalid file type', 'danger')
    return render_template('upload.html', form=form)

#route for downloading a document
@Users.route('/search', methods=['GET'])
def search():
    """ Route to search for a file """
    polling_station_name = request.args.get('polling_station')
    polling_station = PollingStation.query.filter_by(name=polling_station_name).first()
    if polling_station:
        ward = polling_station.ward
        constituency = ward.constituency
        return jsonify({'ward': ward.name, 'constituency': constituency.name})
    return jsonify({'error': 'Polling station not found'}), 404

#route for downloading a document
@Users.route('/login', methods=['GET', 'POST'])
def login():
    """ this is the login route"""
    if current_user.is_authenticated:
        return redirect(url_for('Users.redirect_based_on_role'))  # Redirect to role-based redirect after login

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data


        user = db_storage.get_user_by_email(email)

        if user is None or not bcrypt.check_password_hash(user.password, password):
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('Users.login'))  # Redirect to login page if credentials are invalid

        login_user(user, remember=form.remember.data)

        session['user_id'] = user.id
        session['role'] = user.role
        session['email'] = user.email

        return redirect(url_for('Users.redirect_based_on_role'))  # Redirect to role-based redirection

    # If form is not submitted or validation fails, render login template
    print("current user is not authenticated")
    all_users = db_storage.all(users)
    print("All users:", all_users)
    print("Form is valid:", form.validate_on_submit())
    print("Form errors:", form.errors)
    print("Form data:", form.data)
    
    return render_template('login.html', title='Login', form=form)

#route for redirecting users when they log in
@Users.route('/redirect_based_on_role', methods=['GET', 'POST'])
@login_required
def redirect_based_on_role():
    """Route to redirect based on the user role"""
    current_app.logger.info(f"Redirecting user {current_user.email} with role {current_user.role}.")
    print(f"Redirecting user {current_user.email} with role {current_user.role}.")
    if current_user.has_role(UserRole.ADMIN.value):
        return redirect(url_for('Users.admin_dashboard'))
    elif current_user.has_role(UserRole.DRIVER.value):
        return redirect(url_for('drivers.driver_dashboard'))
    elif current_user.has_role(UserRole.BODYGUARD.value):
        return redirect(url_for('bodyguards.bodyguard_dashboard'))
    elif current_user.has_role(UserRole.RESEARCHER.value):
        return redirect(url_for('researchers.researcher_dashboard'))
    elif current_user.has_role(UserRole.COORDINATOR.value):
        return redirect(url_for('coordinators.coordinator_dashboard'))
    elif current_user.has_role(UserRole.SECRETARY.value):
        return redirect(url_for('secretaries.secretary_dashboard'))
    elif current_user.has_role(UserRole.CHIEF_SECURITY_OFFICER.value):
        return redirect(url_for('chief_security_officers.chief_security_officer_dashboard'))
    elif current_user.has_role(UserRole.SUPER_ADMIN.value):
        return redirect(url_for('Users.admin_dashboard'))
    elif current_user.has_role(UserRole.P_A.value):
        return redirect(url_for('Users.admin_dashboard'))

    elif current_user.has_role(UserRole.FIELD_OFFICER.value):
        return redirect(url_for('fieldofficers.field_officers'))
    elif current_user.has_role(UserRole.CHIEF_FIELD_OFFICER.value):
        return redirect(url_for('chieffieldofficers.chieffieldofficer_dashboard'))
    else:
        return redirect(url_for('main.home'))



#route for the admin dashboard
@Users.route('/admin_dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    """Route for the admin dashboard"""
    form = DeleteForm()
    if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.ADMIN.value) or current_user.has_role(UserRole.P_A.value):
        if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.P_A.value):
            offices = db_storage.get_all_offices()
        else:
            offices = db_storage.get_offices_for_user(current_user.id)

        if not offices:
            flash("No offices available for this user.", "info")  # Add a flash message if no offices found

        return render_template('admin_dashboard.html', title='Admin Dashboard', offices=offices, form=form)
    else:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main.home'))



@Users.route('/create_diary', methods=['GET', 'POST'])
def create_diary():
    """route to create a diary"""
    form = DiaryForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        entry_date = form.entry_date.data

        diary = Diary(
            title=title,
            content=content,
            entry_date=entry_date,
            user_id=current_user.id
        )

        db_storage.new(diary)
        db_storage.save()

        flash('Diary created successfully!', 'success')
        return redirect(url_for('Users.view_diaries'))
    
    return render_template('create_diary.html', title='Create Diary', form=form)

#create a route to view diaries
#route to view diaries
@Users.route('/view_diaries', methods=['GET'])
def view_diaries():
    """route to view all diaries"""
    diaries = db_storage.all(Diary).values()
    return render_template('diary.html', title='View Diaries', diaries=diaries)

#route to delete a diary
@Users.route('/delete_diary/<int:diary_id>', methods=['GET', 'POST'])
def delete_diary(diary_id):
    """route to delete a diary"""
    diary = db_storage.get(Diary, diary_id)
    if diary is None:
        return redirect(url_for('Users.view_diaries'))
    db_storage.delete(diary)
    db_storage.save()
    return redirect(url_for('Users.view_diaries'))

#route to edit a diary
@Users.route('/edit_diary/<int:diary_id>', methods=['GET', 'POST'])
def edit_diary(diary_id):
    """Route to edit a diary entry"""
    diary = db_storage.get(Diary, id=diary_id)
    if not diary:
        flash('Diary not found', 'danger')
        return redirect(url_for('Users.view_diaries'))
    
    # Add logic for handling form submission to edit the diary
    if request.method == 'POST':
        # Update the diary fields here
        diary.title = request.form['title']
        diary.content = request.form['content']
        db_storage.save()
        flash('Diary updated successfully', 'success')
        return redirect(url_for('Users.view_diaries'))
    
    return render_template('edit_diary.html', title='Edit Diary', diary=diary)

#create route to reset password
@Users.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    print("reset request is hit now waiting to validate form")
    form = ResetRequestForm()
    print("reset form is submitted")
    if form.validate_on_submit():
        print("form is validated, now handling the logic")
        # Handle form submission logic
        email = form.email.data
        user = db_storage.get_user_by_email(email)
        print("user has been retrieved by email")
        if user:
            token = generate_token(user.id, current_app.config['SECRET_KEY'], expiration_minutes=30)
            reset_url = url_for('Users.reset_token', token=token, _external=True)
            msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[email])
            msg.body = f'To reset your password, visit the following link: {reset_url}'
            
            try:
                mail.send(msg)
                current_app.logger.info(f"Password reset email sent to {email}")
                flash('An email has been sent with instructions to reset your password.', 'info')
            except Exception as e:
                current_app.logger.error(f"Failed to send password reset email to {email}: {str(e)}")
                flash('Failed to send password reset email. Please try again later.', 'danger')
            
            return redirect(url_for('Users.login'))
        else:
            flash('User not found. Please check the email address.', 'danger')
    
    return render_template('reset_request.html', form=form)

# route to reset the password
@Users.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """ this function is used to reset the password"""
    form = ResetPasswordForm()
    validation_response = validate_token(token, current_app.config['SECRET_KEY'])
    if isinstance(validation_response, str):
        return validation_response, 401
    
    user_id = validation_response['user_id']
    user = db_storage.get_user_by_id(user_id)
    if not user:
        return "User not found", 404
    
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hash_password
        db_storage.save()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('Users.login'))
    
    return render_template('reset_password.html', form=form)

#route for checking the token
@Users.route('/protected_route', methods=['GET'])
def protected_route():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401
    
    validation_response = validate_token(token,current_app.config['SECRET_KEY'])
    if isinstance(validation_response, str):
        return jsonify({"message": validation_response}), 401
    
    # Token is valid, proceed with the request
    user_id = validation_response['user_id']
    # Continue processing the request...
    return jsonify({"message": "Access granted"})

#route for sending reset email
def send_reset_email(user):
    """ this function is used to send the reset email"""
    token = user.get_reset_token()
    logging.debug(f'Token: {token}')
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('Users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    logging.debug('Reset email sent')

#create a route for admin to see all the users
@Users.route('/all_users', methods=['GET'])
@login_required
def all_users():
    """Route for the admin to view all users"""
    if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.ADMIN.value):
        all_users_list = db_storage.all(users).values()
        form = DeleteForm()
        return render_template('users.html', title='Users', users=all_users_list, form=form)
    else:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('main.home'))

# Route for deleting a user (accessible by Admin and Super Admin)
@Users.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Route to delete a user"""
    form = DeleteForm()
    if current_user.has_role(UserRole.SUPER_ADMIN.value) or current_user.has_role(UserRole.ADMIN.value):
        user_to_delete = db_storage.get_user_by_id(user_id)
        if user_to_delete:
            try:
                db_storage.delete(user_to_delete)
                db_storage.save()
                flash(f'User {user_to_delete.name} has been deleted.', 'success')
            except Exception as e:
                flash(f'Error deleting user: {e}', 'danger')
        else:
            flash('User not found.', 'danger')
    else:
        flash('You do not have permission to delete users.', 'danger')
    return redirect(url_for('Users.all_users'))# Route for deleting a user (accessible by Admin and Super Admin)
