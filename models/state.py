#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel):
    """State class"""
    __tablename__ = "states"
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ""

        @property
        def cities(self):
                """Getter for cities"""
                from models import storage
                from models.city import City
                city_list = []
                for key, value in storage.all(City).items():
                    if value.state_id == self.id:
                        city_list.append(value)
                return city_list
         

