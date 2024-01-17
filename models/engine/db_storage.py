#!/usr/bin/python3
"""database storage engine"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.place import place_amenity

classes = {
    "User": User,
    "State": State,
    "City": City,
    "Place": Place,
    "Review": Review,
    "Amenity": Amenity,
}


class DBStorage:
    """'database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """constructor"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of all objects"""
        new_dict = {}
        if cls is None:
            for key, value in classes.items():
                for obj in self.__session.query(value):
                    new_dict[obj.__class__.__name__ + "." + obj.id] = obj
        else:
            for obj in self.__session.query(classes[cls]):
                new_dict[obj.__class__.__name__ + "." + obj.id] = obj
        return new_dict

    def new(self, obj):
        """adds a new object to the database"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refressh(obj)
            except:
                self.__session.rollback()
                raise Exception
        else:
            raise Exception

    def save(self):
        """saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object from the database"""
        if obj is not None:
            self.__session.query(type(obj)).filter(type(obj).id == obj.id).delete()

    def reload(self):
        """reloads the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """closes the session"""
        self.__session.close()

    def get(self, cls, id):
        """returns an object based on class and id"""
        if cls is not None and id is not None:
            for obj in self.__session.query(classes[cls]):
                if obj.id == id:
                    return obj
        return None

