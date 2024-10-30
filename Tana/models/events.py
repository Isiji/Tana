from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from Tana.models.base_model import BaseModel, Base

class Events(BaseModel, Base):
    __tablename__ = 'events'
    event_name = Column(String(128), nullable=False)
    impact_level = Column(String(10), nullable=False)
    event_leader = Column(String(128), nullable=False)
    event_location = Column(String(128), nullable=False)
    contact_person = Column(String(128), nullable=False)  # Changed to String
    event_description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    polling_station_id = Column(Integer, ForeignKey('polling_stations.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    polling_station = relationship("PollingStation", back_populates="events")
    user = relationship("users", back_populates="events")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

IMPACT_LEVELS = ['High', 'Medium', 'Low']
