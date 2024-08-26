#!/usr/bin/python3
"""County office update module for the county office update"""
from sqlalchemy import Column, String, Date, Text, Integer
from Tana.models.base_model import BaseModel, Base



class CountyOfficeUpdate(Base, BaseModel):
    __tablename__ = 'county_office_update'
    
    date = Column(Date, nullable=False)
    party_involved = Column(String(255), nullable=False)
    issues = Column(Text, nullable=False)
    delegation = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=False)
    action_taken = Column(Text, nullable=False)
    
    def __init__(self, *args, **kwargs):
        """Initialization of the county office update model"""
        super().__init__(*args, **kwargs)
