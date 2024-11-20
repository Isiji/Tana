#!/usr/bin/python3
"""Questions class module for the questions, where the questions are stored"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Date, Enum as SaEnum, LargeBinary
from Tana.models.status import StatusEnum


class Questions(BaseModel, Base):
    """This class defines the questions model"""
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    document = Column(LargeBinary(length=4294967295), nullable=False)
    follow_up_document = Column(LargeBinary(length=4294967295), nullable=True)  # Add this line
    date = Column(Date, nullable=False)
    status = Column(SaEnum(StatusEnum), nullable=False)        
    filename = Column(String(255), nullable=False)
    follow_up_filename = Column(String(255), nullable=True)  # Add this line

    def __init__(self, *args, **kwargs):
        """Initialization of the questions model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a questions"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
