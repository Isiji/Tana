#!/usr/bin/python3
"""config file for the app"""
import os
import json

with open('/etc/config.json') as config_file:
   config = json.load(config_file)

class Config:
    """Config class for the app"""
    SECRET_KEY = config.get('SECRET_KEY')  # Replace with your own secret key
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_FILE_PATH = os.path.join(os.getcwd(), 'Tana', 'representation', 'tanawards.csv')

    # Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ('MAIL_USERNAME')  # Replace with your actual email
    MAIL_PASSWORD = ('MAIL_PASSWORD')  # Replace with your actual email password
    MAIL_DEFAULT_SENDER = 'noreply@demo.com'  # Replace with your default sender email

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx', 'csv', 'pdf'}
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
