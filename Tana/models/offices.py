#!/usr/bin/python3
"""Users class for the users"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, Boolean, String, Integer
from sqlalchemy.orm import relationship

class Offices(BaseModel, Base):
    """This class defines the users model"""
    __tablename__ = 'offices'
    office_name = Column(String(128), nullable=False)
    office_location = Column(String(128), nullable=False)
    office_description = Column(String(128), nullable=False)
    office_manager = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    users = relationship("users", back_populates="offices")

    def __init__(self, *args, **kwargs):
        """Initialization of the users model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a user"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)