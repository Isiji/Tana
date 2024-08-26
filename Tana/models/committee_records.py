
#!/usr/bin/env python3
"""Committee records module for the committee records"""  
from sqlalchemy import Column, String, Integer, ForeignKey, Date, LargeBinary
from Tana.models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship

class CommitteeRecord(Base, BaseModel):
    """This class defines the committee records model"""
    __tablename__ = 'committee_records'
    
    id = Column(Integer, primary_key=True)
    serial_number = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    title = Column(String(255), nullable=False)
    document = Column(LargeBinary(length=4294967295), nullable=True)
    recommendations = Column(LargeBinary(length=4294967295), nullable=True)
    document_filename = Column(String(255), nullable=True)  # New field for document filename
    recommendations_filename = Column(String(255), nullable=True)  # New field for recommendations filename
    committee_id = Column(Integer, ForeignKey('committees.id'), nullable=False)
    
    committee = relationship('Committee', back_populates='records')
    
    def __init__(self, serial_number, date, title, document, recommendations, document_filename=None, recommendations_filename=None, committee_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial_number = serial_number
        self.date = date
        self.title = title
        self.document = document
        self.recommendations = recommendations
        self.document_filename = document_filename
        self.recommendations_filename = recommendations_filename
        self.committee_id = committee_id
