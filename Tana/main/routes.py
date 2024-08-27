#!/usr/bin/python3
"""main class for the module"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask import session

main = Blueprint('main', __name__)

#route for the homepage
@main.route('/')
@main.route('/home')
def home():
    """homepage route for the user"""
    return render_template('home.html')


