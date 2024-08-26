#!/usr/bin/python3
"""Bills class module for the bills, it includes a field for the 
document and the filename of the document"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Date, Boolean, LargeBinary

class Bills(BaseModel, Base):
    __tablename__ = 'bills'
    name = Column(String(128), nullable=False)
    submitted_date = Column(Date, nullable=False)
    first_reading = Column(Boolean, default=False)
    first_reading_date = Column(Date, nullable=True)
    second_reading = Column(Boolean, default=False)
    second_reading_date = Column(Date, nullable=True)
    third_reading = Column(Boolean, default=False)
    third_reading_date = Column(Date, nullable=True)
    presidential_assent = Column(Boolean, default=False)
    presidential_assent_date = Column(Date, nullable=True)
    commencement = Column(Boolean, default=False)
    commencement_date = Column(Date, nullable=True)
    document = Column(LargeBinary(length=4294967295), nullable=False)
    filename = Column(String(255), nullable=False)
    
    def __init__(self, *args, **kwargs):
        """Initialization of the bills model"""
        super().__init__(*args, **kwargs)
