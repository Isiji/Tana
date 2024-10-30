#!/usr/bin/env python3  
"""Statements class module for the statements, where the statements are stored"""
from sqlalchemy import Column, String, Integer, Date, Enum as SaEnum, LargeBinary, Text
from Tana.models.base_model import BaseModel, Base
from Tana.models.status import StatusEnum

class Statements(BaseModel, Base):
    """This class defines the statements model"""
    __tablename__ = 'statements'
    name = Column(String(255), nullable=False)
    document = Column(LargeBinary(length=4294967295), nullable=False)
    follow_up_letter = Column(LargeBinary(length=4294967295), nullable=True)  # New field for follow-up letters
    date = Column(Date, nullable=False)
    status = Column(SaEnum(StatusEnum), nullable=False)
    filename = Column(String(255), nullable=False)
    
    def __init__(self, document, follow_up_letter, date, status, *args, **kwargs):
        """Initialization of the statements model"""
        super().__init__(*args, **kwargs)
        self.document = document
        self.follow_up_letter = follow_up_letter
        self.date = date
        self.status = status
        
    def __str__(self):
        """String representation of a statement"""
        return f"{self.__class__.__name__} (ID: {self.id}, Date: {self.date}, Status: {self.status})"
