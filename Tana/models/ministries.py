from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from Tana.models.base_model import BaseModel, Base

class Ministries(BaseModel, Base):
    __tablename__ = 'ministries'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    contact_person = Column(String(128), nullable=False)
    mobile_number = Column(String(20), nullable=False)
    email = Column(String(128), nullable=True)
    documents_presented = Column(Text, nullable=False)
    date_documents_presented = Column(Date, nullable=False)

    def __init__(self, name, contact_person, mobile_number, email, documents_presented, date_documents_presented, *args, **kwargs):
        self.name = name
        self.contact_person = contact_person
        self.mobile_number = mobile_number
        self.email = email
        self.documents_presented = documents_presented
        self.date_documents_presented = date_documents_presented
        super().__init__(*args, **kwargs)
