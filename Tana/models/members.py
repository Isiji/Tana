#!/usr/bin/python3
"""Users class module for the users"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from Tana.models.roles import UserRole
from itsdangerous import URLSafeSerializer, BadSignature
from flask import current_app
from datetime import datetime, timedelta
class users(BaseModel, Base, UserMixin):
    """This class defines the users model, it has several attributes and relationships"""
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(Integer, nullable=False)
    ID_No = Column(Integer, nullable=False)
    role = Column(String(128), nullable=False)
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=True)

    diaries = relationship("Diary", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    offices = relationship("Offices", back_populates="users")
    events = relationship("Events", back_populates="user")
    # Removed the employee_registers relationship

    def __init__(self, *args, **kwargs):
        """Initialization of the users model"""
        super().__init__(*args, **kwargs)




    def __str__(self):
        """string representation of a user"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def get_reset_token(self, expires_sec=3600):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        expires_at = datetime.utcnow() + timedelta(seconds=expires_sec)
        return s.dumps({'user_id': self.id, 'expires_at': expires_at.isoformat()})

    @staticmethod
    def verify_reset_token(token):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            expires_at = datetime.fromisoformat(data['expires_at'])
            if expires_at >= datetime.utcnow():
                return users.get(data['user_id'])
        except (BadSignature, ValueError):
            return None

    @staticmethod
    def get_user_by_email(email):
        """get a user by email"""
        from Tana import db_storage

        return db_storage.get_user_by_email(email)

    @staticmethod
    def get_user_by_id(id):
        """get a user by id"""
        from Tana import db_storage

        return db_storage.get_user_by_id(id)
    def has_role(self, role):
        """check if a user has a role"""
        return self.role == role

    @staticmethod
    def create_user(name, email, password, phone, ID_No, role, office_id):
        """creates a user"""
        from Tana import db_storage

        if role not in UserRole._value2member_map_:
            raise ValueError("Invalid role")

        user = users(
            name=name,
            email=email,
            password=password,
            phone=phone,
            ID_No=ID_No,
            role=role,
            office_id=office_id,
        )

        db_storage.new(user)
        db_storage.save()
        return user
    @staticmethod
    def create_super_admin():
        """creates a superadmin user if not already existing"""
        from Tana import db_storage, bcrypt
        # Check if a super admin with this email already exists
        existing_super_admin = db_storage.get_user_by_email(email="wandedanton@gmail.com")

        if existing_super_admin:
            return existing_super_admin

        password_hash = bcrypt.generate_password_hash("password").decode('utf-8')
        super_admin = users(
            name="Danton",
            email="wandedanton@gmail.com",
            password=password_hash,
            phone='0727895448',
            ID_No=1234,
            role=UserRole.SUPER_ADMIN.value,
            office_id=None,
        )

        db_storage.new(super_admin)
        db_storage.save()
        return super_admin

    

    def can_register_user(self, role):
        """checks if the current user can register a user"""
        allowed_roles = {
            UserRole.SUPER_ADMIN: [
                UserRole.ADMIN, UserRole.DRIVER, UserRole.MANAGER, UserRole.BODYGUARD,
                UserRole.RESEARCHER, UserRole.SECRETARY, UserRole.CHIEF_FIELD_OFFICER,
                UserRole.CHIEF_SECURITY_OFFICER, UserRole.COORDINATOR, UserRole.FIELD_OFFICER,
                UserRole.P_A
            ],
            UserRole.ADMIN: [UserRole.P_A, UserRole.DRIVER, UserRole.BODYGUARD, UserRole.RESEARCHER, UserRole.COORDINATOR, UserRole.SECRETARY, UserRole.CHIEF_SECURITY_OFFICER, UserRole.CHIEF_FIELD_OFFICER, UserRole.FIELD_OFFICER],
            UserRole.P_A: [UserRole.DRIVER, UserRole.BODYGUARD, UserRole.RESEARCHER, UserRole.COORDINATOR, UserRole.SECRETARY, UserRole.CHIEF_SECURITY_OFFICER, UserRole.CHIEF_FIELD_OFFICER, UserRole.FIELD_OFFICER]
        }
        return role in allowed_roles.get(self.role, [])
