import os
import csv
import pytz
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import configure_mappers
from Tana.config import Config
from Tana.engine.storage import DBStorage
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation
from Tana.models.members import users
from Tana.models.committees import Committee  
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from Tana.models.ministries import Ministries

db_storage = DBStorage()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'Users.login'
login_manager.login_message_category = 'info'
cors = CORS()
mail = Mail()
jwt = JWTManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    user = db_storage.get_user_by_id(user_id)
    if user:
        return user
    else:
        office = db_storage.get_office(users)
        if office:
            return office
    return None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx', 'csv', 'pdf', 'docx', 'doc'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
    
    db_storage
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)

    @app.before_request
    def add_current_time():
        nairobi_tz = pytz.timezone('Africa/Nairobi')
        request.current_time = datetime.now(nairobi_tz).strftime("%Y-%m-%d %H:%M:%S")

    @app.context_processor
    def inject_current_time():
        return dict(current_time=request.current_time)

    with app.app_context():
        db_storage.reload()
        configure_mappers()
        
        # Ensure super admin user is created if not exists
        if not db_storage.get_user('wandedanton@gmail.com'):
            users.create_super_admin()

        # CSV processing logic
        csv_file_path = app.config.get('CSV_FILE_PATH', '')
        if os.path.exists(csv_file_path):
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    constituency_name = row['constituency']
                    ward_name = row['ward']
                    polling_station_name = row['polling_station']

                    # Check if Constituency already exists
                    constituency = db_storage.get(Constituency, name=constituency_name)
                    if not constituency:
                        constituency = Constituency(name=constituency_name)
                        db_storage.new(constituency)
                    
                    # Check if Ward already exists within the Constituency
                    ward = db_storage.get(Ward, name=ward_name, constituency_id=constituency.id)
                    if not ward:
                        ward = Ward(name=ward_name, constituency_id=constituency.id)
                        db_storage.new(ward)
                    
                    # Check if PollingStation already exists
                    polling_station = db_storage.get(PollingStation, name=polling_station_name, ward_id=ward.id)
                    if not polling_station:
                        polling_station = PollingStation(name=polling_station_name, ward_id=ward.id)
                        db_storage.new(polling_station)

            db_storage.save()

        # Insert hardcoded committees
        COMMITTEES = [
            {'id': 1, 'name': 'Energy Committee'},
            {'id': 2, 'name': 'Delegated Legislation Committee'},
            {'id': 3, 'name': 'Pan African Parliament Committee'},
            {'id': 4, 'name': 'Bunge Sports Club'},
            {'id': 5, 'name': 'CPAC'},
            {'id': 6, 'name': 'CPIC'}
        ]

        for committee in COMMITTEES:
            existing_committee = db_storage.get(Committee, id=committee['id'])
            if not existing_committee:
                new_committee = Committee(id=committee['id'], name=committee['name'])
                db_storage.new(new_committee)
        db_storage.save()

        # Register blueprints
        from Tana.users.routes import Users
        from Tana.events.routes import events_bp
        from Tana.offices.routes import offices
        from Tana.reminder.routes import reminders
        from Tana.main.routes import main
        from Tana.bodyguards.routes import bodyguards
        from Tana.secretaries.routes import secretaries
        from Tana.coordinators.routes import coordinators
        from Tana.drivers.routes import drivers
        from Tana.chief_field_officers.routes import chieffieldofficers
        from Tana.field_officers.routes import fieldofficers
        from Tana.researchers.routes import researchers
        from Tana.bills.routes import bills_bp
        from Tana.legislation.routes import legislation_bp
        from Tana.oversight.routes import oversight_bp
        from Tana.representation.routes import representation
        from Tana.ministries.routes import ministry_bp
        from Tana.CountyReports.routes import report_bp

        app.register_blueprint(Users)
        app.register_blueprint(events_bp)
        app.register_blueprint(offices)
        app.register_blueprint(reminders)
        app.register_blueprint(main)
        app.register_blueprint(bodyguards)
        app.register_blueprint(secretaries)
        app.register_blueprint(coordinators)
        app.register_blueprint(drivers)
        app.register_blueprint(chieffieldofficers)
        app.register_blueprint(fieldofficers)
        app.register_blueprint(researchers)
        app.register_blueprint(bills_bp)
        app.register_blueprint(legislation_bp)
        app.register_blueprint(oversight_bp)
        app.register_blueprint(representation)
        app.register_blueprint(ministry_bp)
        app.register_blueprint(report_bp)
        
    return app
