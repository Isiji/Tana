#!/usr/bin/python3
""" employees should be able to register and time in and out of work"""

from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, Time, String, DateTime, Integer, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship, backref
class EmployeeRegister(BaseModel, Base):
    __tablename__ = 'employee_register'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    time_in = Column(String(8), nullable=False)  # or Time if supported
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    def __init__(self, *args, **kwargs):
        """Initialization of the employee register model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation of an employee register"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
