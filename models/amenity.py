<<<<<<< HEAD
#!/usr/bin/python3
""" instances amenities """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.place import Place
from os import getenv

STORAGE = getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    """Permit to add the amenities for places"""
    __tablename__ = "amenities"
    if STORAGE == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            'Place', secondary=Place.place_amenity)

    else:
        name = ""
=======
#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """class amenity"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary='place_amenity')
>>>>>>> 60ca4276e3f31093411ae5ea38e01d16a177a801
