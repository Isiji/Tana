#!/usr/bin/python3
"""routes for the chief field officers"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

chieffieldofficers = Blueprint('chieffieldofficers', __name__)

# create route for the chief field officer dashboard
@chieffieldofficers.route('/chieffieldofficer_dashboard')
@login_required
def chieffieldofficer_dashboard():
    """route for the chief field officer dashboard"""
    return render_template('chieffieldofficer.html', title='Chief Field Officer Dashboard')

# create route for the chief field officer to view all field officers
@chieffieldofficers.route('/field_officers')
@login_required
def field_officers():
    """route for the chief field officer to view all field officers"""
    field_officers = db_storage.get_field_officers()
    return render_template('field_officers.html', field_officers=field_officers)

# create route for the chief field officer to view a specific field officer by name in the database
@chieffieldofficers.route('/field_officers/<name>')
@login_required
def field_officer(name):
    """route for the chief field officer to view a specific field officer by name"""
    field_officer = db_storage.get_field_officer_by_name(name)
    return render_template('field_officer.html', field_officer=field_officer)

