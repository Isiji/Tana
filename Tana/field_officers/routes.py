#!/usr/bin/python3
"""routes for the field officers"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

fieldofficers = Blueprint('fieldofficers', __name__)

#route for the field officers dashboard
@fieldofficers.route('/field_officers')
def field_officers():
    return render_template('field_officers.html')
