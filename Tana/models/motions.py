from sqlalchemy import Column, String, Integer, Date, Enum, LargeBinary
from Tana.models.base_model import BaseModel, Base

class Motions(BaseModel, Base):
    """This class defines the motions model"""
    __tablename__ = 'motions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    document = Column(LargeBinary(length=4294967295), nullable=False)
    follow_up_document = Column(LargeBinary(length=4294967295), nullable=True)
    date = Column(Date, nullable=False)
    status = Column(Enum("Pending", "Approved", "Rejected"), nullable=False)
    filename = Column(String(255), nullable=False)
    follow_up_filename = Column(String(255), nullable=True)

    def __init__(self, *args, **kwargs):
        """Initialization of the motions model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """String representation of a motion"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
