#!/usr/bin/python3
"""representation class module for the representation"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship, backref

class Representation(BaseModel, Base):
    __tablename__ = 'representation'
    id = Column(Integer, primary_key=True)
    constituency = Column(String(128), nullable=False)
    ward = Column(String(128), nullable=False)
    polling_station = Column(String(128), nullable=False)

    
    def __init__(self, *args, **kwargs):
        """Initialization of the representation model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """string represenation of a representation"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
        
        