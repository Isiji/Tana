#!/usr/bin/python3
"""bodyguards routes for the module"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

bodyguards = Blueprint('bodyguards', __name__)

# create route for the bodyguard dashboard
@bodyguards.route('/bodyguard_dashboard')
@login_required
def bodyguard_dashboard():
    """route for the bodyguard dashboard"""
    return render_template('bodyguard.html', title='Bodyguard Dashboard')