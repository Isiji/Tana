#!/usr/bin/python3
"""Tasks class module for the tasks"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Tasks(BaseModel, Base):
    """This class defines the tasks model"""
    __tablename__ = 'tasks'
    task_title = Column(String(128), nullable=False)
    task_description = Column(String(128), nullable=False)
    task_date = Column(Date, nullable=False)
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=False)
    assigned_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    due_date = Column(Date, nullable=False)

    assigned_to_user = relationship("users", foreign_keys=[assigned_to], back_populates="tasks_assigned_to")
    assigned_by_user = relationship("users", foreign_keys=[assigned_by], back_populates="tasks_assigned")

    def __init__(self, *args, **kwargs):
        """Initialization of the tasks model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a task"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
