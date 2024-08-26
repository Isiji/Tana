#!/usr/bin/python3
"""Diary class module for the diary"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

class Diary(BaseModel, Base):
    """This class defines the diary model"""
    __tablename__ = 'diary'
    title = Column(String(128), nullable=False)
    content = Column(String(128), nullable=False)
    entry_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("users", back_populates="diaries")

    def __init__(self, *args, **kwargs):
        """Initialization of the diary model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a diary"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

