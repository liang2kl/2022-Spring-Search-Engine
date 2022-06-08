from sqlalchemy import create_engine, Column, Integer, Float, String
from database import Base

engine = create_engine('sqlite:///db.sqlite')

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    features = Column(String)
    distance = Column(Float)
    width = Column(Integer)
    height = Column(Integer)
    file_name = Column(String)
    colors = Column(String)
