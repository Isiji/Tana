#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, request,jsonify, flash, render_template, redirect, url_for, session
from Tana.models.offices import Offices
from Tana.offices.forms import OfficeForm
from flask_login import login_required, current_user, login_user, logout_user
from Tana import bcrypt, db_storage
from Tana.models.members import users
import logging
from Tana.users.forms import RegistrationForm
from Tana import csrf


offices = Blueprint('offices', __name__)

#create a route for creating offices by the admin
@offices.route('/create_office', methods=['POST', 'GET'])
def create_office():
    """Route for the creation of offices."""
    form = OfficeForm()
    if form.validate_on_submit():
        office = Offices(
            office_name=form.office_name.data,
            office_location=form.office_location.data,
            office_description=form.office_description.data,
            email=form.email.data,
            office_manager=form.office_manager.data
        )
        db_storage.new(office)
        db_storage.save()
        print(f"created office id: {office.id}")
        flash('Your office has been created! You can now view office details.', 'success')
        return redirect(url_for('offices.office_details', office_id=office.id))
    return render_template('create_office.html', title='Create Office', form=form)

#route for viewing office details by id
@offices.route('/office_details/<int:office_id>', methods=['GET', 'POST'])
@login_required
def office_details(office_id):
    """Route to display office details."""
    print(f"fetching office details for ID : {office_id}")
    office = db_storage.get_office_by_id(office_id)
    if office is None:
        flash('Office not found.', 'danger')
        return redirect(url_for('main.home'))
    
    members = db_storage.get_users_by_office_id(office_id)
    
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
    
    return render_template('office_details.html', title=office.office_name, office=office, members=members, form=form)

#route for office dashboard
@offices.route('/office_dashboard', methods=['POST', 'GET'], strict_slashes=False)
def office_dashboard():
    """route for the office dashboard"""
    if 'user_id'in session:
        user_id = session['user_id']
        office = db_storage.get(Offices, id=user_id)
        
        if office:
            office_name = office.office_name
            office_location = office.office_location
            office_description = office.office_description
            office_manager = office.office_manager
            email = office.email
            
            return render_template('office.html', title='Office Dashboard',office=office, office_name=office_name, office_location=office_location, office_description=office_description, office_manager=office_manager, email=email)
        else:
            logging.error('Office not found. error number 1')
            
    else:
        logging.error('Office not found. error number 2')
        return redirect(url_for('Users.register'))
    
#create a route for accesing a specific office by name of the office
@offices.route('/office/<string:office_name>', methods=['POST', 'GET'], strict_slashes=False)
def office(office_name):
    """route for the office dashboard"""
    office = db_storage.get(Offices, office_name=office_name)
    if office:
        office_name = office.office_name
        office_location = office.office_location
        office_description = office.office_description
        office_manager = office.office_manager
        email = office.email
        return render_template('office.html', title='Office Dashboard',office=office, office_name=office_name, office_location=office_location, office_description=office_description, office_manager=office_manager, email=email)
    else:
        logging.error('Office not found. error number 3')
        return redirect(url_for('main.home'))
    

#function that serves offices as list
@offices.route('/offices_list', methods=['GET'])
def get_offices_list():
    """Route to fetch the list of office names"""
    try:
        offices = db_storage.all(Offices)  # Fetch all offices from the database
        print(f"Offices fetched: {offices}")  # Debug statement to check the data
        if not offices:
            return jsonify([])  # Return an empty list if no offices are found
        office_names = [office.office_name for office in offices.values()]
        return jsonify(office_names)
    except Exception as e:
        # Log the exception if there's an error
        logging.error(f"Error fetching offices: {e}")
        return jsonify([]), 500

@offices.route('/delete_office/<int:office_id>', methods=['GET', 'POST'])
@login_required
def delete_office(office_id):
    """Route to delete an office."""
    office = db_storage.get_office_by_id(office_id)

    if request.method == 'POST':
        if office:
            # Delete all users associated with the office
            users_to_delete = db_storage.get_users_by_office_id(office_id)
            for user in users_to_delete:
                db_storage.delete(user)

            # Now delete the office
            db_storage.delete(office)
            db_storage.save()
            flash(f'Office "{office.office_name}" and all associated users have been deleted.', 'success')
        else:
            flash('Office not found.', 'danger')

        return redirect(url_for('Users.admin_dashboard'))

    # Render the delete office page (it would show details about the office to delete)
    return render_template('delete_office.html', title='Delete Office', office=office)
