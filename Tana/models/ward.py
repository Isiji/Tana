#!/usr/bin/python3
"""Ward class module for the ward"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Ward(BaseModel, Base):
    __tablename__ = 'wards'
    name = Column(String(128), nullable=False, unique=True)
    constituency_id = Column(Integer, ForeignKey('constituencies.id'), nullable=False)
    constituency = relationship("Constituency", back_populates="wards")
    polling_stations = relationship("PollingStation", back_populates="ward")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "[{:s}] ({:d}) {}".format(self.__class__.__name__, self.id, self.name)
