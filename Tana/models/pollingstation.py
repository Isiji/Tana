#!/usr/bin/env python3
"""PollingStation class module for the polling stations, it has 
several attributes and relationships"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Tana.models.base_model import BaseModel, Base

class PollingStation(BaseModel, Base):
    __tablename__ = 'polling_stations'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    ward_id = Column(Integer, ForeignKey('wards.id'), nullable=False)
    ward = relationship("Ward", back_populates="polling_stations")
    events = relationship("Events", back_populates="polling_station")  # Use plural 'events' here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "[{:s}] ({:d}) {}".format(self.__class__.__name__, self.id, self.name)
