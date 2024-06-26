#!/usr/bin/python3
"""HumanResource class module for the humanresource"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class HumanResource(BaseModel, Base):
    """This class defines the humanresource model"""
    __tablename__ = 'humanresource'
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("users", back_populates="human_resources")
    office_id = Column(Integer, ForeignKey('offices.id'))
    job_title = Column(String(128), nullable=False)
    employment_date = Column(Date , nullable=False)
    salary = Column(Integer, nullable=False)
    office = relationship("Offices", back_populates="human_resources")
    role = Column(Enum('admin', 'employee'))
                  
    def __init__(self, *args, **kwargs):
        """Initialization of the humanresource model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a humanresource"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)