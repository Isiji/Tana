#!/usr/bin/python3
"""config file for the app"""
import os

class Config:
    """Config class for the app"""
    SECRET_KEY = "Tana"  # Replace with your own secret key
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://Tana:Tana123.@localhost/Tana'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_FILE_PATH = os.path.join(os.getcwd(), 'Tana', 'representation', 'tanawards.csv')

    # Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tanarivercountysenateoffice@gmail.com'  # Replace with your actual email
    MAIL_PASSWORD = 'jksj ztze hjjv skyk'  # Replace with your actual email password
    MAIL_DEFAULT_SENDER = 'noreply@demo.com'  # Replace with your default sender email

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx', 'csv', 'pdf'}
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
