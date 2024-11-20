#!/usr/bin/python3
"""Database storage module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import sys
from sqlalchemy.exc import SQLAlchemyError
from Tana.models.base_model import Base
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana.models.offices import Offices
from Tana.models.reminder import Reminder
from Tana.models.diary import Diary
from Tana.models.calendarEvents import CalendarEvents
from Tana.models.events import Events
from Tana.models.pollingstation import PollingStation
from Tana.models.ward import Ward
from Tana.models.constituency import Constituency
from Tana.models.bills import Bills
from Tana.models.employee_register import EmployeeRegister
from Tana.models.events import Events
from Tana.models.motions import Motions
from Tana.models.questions import Questions
from Tana.models.secondaryoversight import SecondaryOversight
from Tana.models.statements import Statements
from Tana.models.county_office_update import CountyOfficeUpdate
from Tana.models.committee_records import CommitteeRecord
from Tana.models.committees import Committee
from Tana.models.ministries import Ministries
from Tana.models.status import StatusEnum
from Tana.models.county_reports import CountyReports



class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self, app=None):
        """Initializes the database storage"""
        if app is not None:
            self.__engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)
        else:
            self.__engine = create_engine('postgresql+psycopg2://tana_user:Tana123.@localhost/tana', pool_pre_ping=True)
        
        if 'test' in sys.argv:
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def all(self, cls=None):
        """Returns a dictionary of all objects"""
        objects = {}
        try:
            if cls is not None:
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = "{}.{}".format(cls.__name__, obj.id)
                    objects[key] = obj
            else:
                classes = [users, UserRole, StatusEnum, CountyReports, Offices, Ministries, CommitteeRecord, Committee, CountyOfficeUpdate, Reminder, Diary, CalendarEvents, Events, PollingStation, Ward, Constituency, Bills, EmployeeRegister, Motions, Questions, SecondaryOversight, Statements]
                for cls in classes:
                    query_result = self.__session.query(cls).all()
                    for obj in query_result:
                        key = "{}.{}".format(cls.__name__, obj.id)
                        objects[key] = obj
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
        return objects

    def new(self, obj):
        """Adds the object to the current database session"""
        try:
            self.__session.add(obj)
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def save(self):
        """Commits all changes to the database"""
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_user(self, email):
        """Returns the user object"""
        try:
            query_result = self.__session.query(users).filter_by(email=email).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_office(self, office):
        """Returns the office object"""
        try:
            query_result = self.__session.query(Offices).filter_by(office_name=office).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get(self, cls, **kwargs):
        """Returns the object based on the class and keyword arguments"""
        try:
            query_result = self.__session.query(cls).filter_by(**kwargs).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_user_by_email(self, email):
        """Retrieve a user by their email."""
        try:
            query_result = self.__session.query(users).filter_by(email=email).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def rollback(self):
        """Rolls back the current session"""
        try:
            self.__session.rollback()
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        try:
            query_result = self.__session.query(users).filter_by(id=user_id).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def delete(self, obj=None):
        """Deletes the object from the current database session"""
        try:
            if obj:
                self.__session.delete(obj)
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def reload(self):
        """Creates all tables in the database"""
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine)
            self.__session = scoped_session(session_factory)
            self.__session.configure(bind=self.__engine)
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def close(self):
        """Closes the current session"""
        try:
            self.__session.remove()
            self.__session.close()
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_users_by_office_id(self, office_id):
        """Returns a list of users by office ID"""
        try:
            query_result = self.__session.query(users).filter_by(office_id=office_id).all()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_office_by_id(self, office_id):
        """Returns the office object by ID"""
        try:
           

            query_result = self.__session.query(Offices).filter_by(id=office_id).first()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)

    def get_all_offices(self):
        """Returns a list of all office objects"""
        try:
            return self.__session.query(Offices).all()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
            return []

    def get_offices_for_user(self, user_id):
        """Returns offices associated with a specific user"""
        try:
            return self.__session.query(Offices).filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
            return []

    def get_all_users(self):
        """Returns a list of all user objects"""
        try:
            return self.__session.query(users).all()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
            return []

    def get_or_create(self, model, defaults=None, **kwargs):
        """Returns an existing object or creates a new one if it doesn't exist"""
        try:
            instance = self.__session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance, False
            else:
                params = {**kwargs, **(defaults or {})}
                instance = model(**params)
                self.new(instance)
                self.save()
                return instance, True
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)

    def get_diaries_by_user(self, user_id):
        """Returns diaries associated with a specific user"""
        try:
            return self.__session.query(Diary).filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
            return []

    def get_constituency_by_name(self, name):
        """Returns a constituency object by name"""
        try:
            return self.__session.query(Constituency).filter_by(name=name).first()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)

    def get_ward_by_name(self, name):
        """Returns a ward object by name"""
        try:
            return self.__session.query(Ward).filter_by(name=name).first()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)

    def get_pollingstation_by_name(self, name):
        """Returns a polling station object by name"""
        try:
            return self.__session.query(PollingStation).filter_by(name=name).first()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)

    def get_ward_by_id(self, ward_id):
        """Returns a ward object by ID"""
        try:
            return self.__session.query(Ward).filter_by(id=ward_id).first()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)

    def get_constituency_by_id(self, constituency_id):
        """Returns a constituency object by ID"""
        try:
            return self.__session.query(Constituency).filter_by(id=constituency_id).first()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)


    def find_one(self, model, **kwargs):
            """Find a single instance of model that matches the given kwargs."""
            try:
                return self.__session.query(model).filter_by(**kwargs).first()
            except SQLAlchemyError as e:
                print("An Error Occurred:", e)
    
    def get_session(self):
        return self.__session
    
    def get_researchers(self):
        """Returns a list of all researchers"""
        try:
            return self.__session.query(users).filter_by(role='Researcher').all()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
            return []

    def get_field_officers(self):
        """Returns a list of all field officers"""
        try:
            return self.__session.query(users).filter_by(role='Field Officer').all()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
            return []
        
    def get_field_officer_by_name(self, name):
        """Returns a field officer by name"""
        try:
            return self.__session.query(users).filter_by(name=name).first()
        except SQLAlchemyError as e:
            print("An Error Occurred:", e)
            
            
    def filter(self, cls, *criterion):
        """Returns a list of objects filtered by the given criterion"""
        try:
            query_result = self.__session.query(cls).filter(*criterion).all()
            return query_result
        except SQLAlchemyError as e:
            print("An Error Occured:", e)
            return []
