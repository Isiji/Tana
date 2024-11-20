#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Text, Date, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from Tana.models.base_model import BaseModel, Base
from datetime import datetime

class CountyReports(BaseModel, Base):
    __tablename__ = 'county_reports'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    contact_person = Column(String(128), nullable=False)
    mobile_number = Column(String(20), nullable=False)
    email = Column(String(128), nullable=True)
    report_data = Column(LargeBinary(length=4294967295), nullable=True)  # Adjusted to handle binary data (e.g., PDF reports)
    report_data_filename = Column(String(255), nullable=True)  # To store the filename
    date_report_uploaded = Column(Date, nullable=False, default=datetime.utcnow)
    parent_id = Column(Integer, ForeignKey('county_reports.id'), nullable=True)  # For nested folders

    # Parent relationship to allow nested folders
    parent = relationship("CountyReports", remote_side=[id], backref="subfolders")

    def __init__(self, name, contact_person, mobile_number, email, report_data, report_data_filename, date_report_uploaded, parent_id=None, created_at=None, *args, **kwargs):
        self.name = name
        self.contact_person = contact_person
        self.mobile_number = mobile_number
        self.email = email
        self.report_data = report_data
        self.report_data_filename = report_data_filename
        self.date_report_uploaded = date_report_uploaded
        self.parent_id = parent_id
        self.created_at = created_at or datetime.utcnow()
        super().__init__(*args, **kwargs)

