#!/usr/bin/env python
"""Committee module for the committees"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Tana.models.base_model import BaseModel, Base

class Committee(Base, BaseModel):
    """ This class defines the committee model """
    __tablename__ = 'committees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    # Relationship back to CommitteeRecord
    records = relationship('CommitteeRecord', back_populates='committee')
