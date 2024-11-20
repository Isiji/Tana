#!/usr/bin/python3
"""routes for the secretaries"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

secretaries = Blueprint('secretaries', __name__)

#route for the secretary dashboard
@secretaries.route('/secretary_dashboard')
@login_required
def secretary_dashboard():
    """route for the secretary dashboard"""
    return render_template('secretary.html', title='Secretary Dashboard')