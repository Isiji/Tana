#!/usr/bin/python3
"""routes for the drivers"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

drivers = Blueprint('drivers', __name__)

#route for the driver dashboard
@drivers.route('/driver_dashboard')
def driver_dashboard():
    """route for the driver dashboard"""
    return render_template('driver.html', title='Driver Dashboard')