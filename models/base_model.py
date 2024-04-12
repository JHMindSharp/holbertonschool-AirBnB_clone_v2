#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String


Base = declarative_base()


class BaseModel:
    """
     A base class for all hbnb models
     Atributes:
         id (sqlalchemy column)
         created_at (sqlalchemy datetime)
         updated_at (sqlalchemy datetime)
     """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.now()
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.now()
            kwargs.pop('__class__', None)

            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictio = {}
        dictio.update(self.__dict__)
        dictio.pop('_sa_instance_state', None)

        dictio['__class__'] = (str(type(self)).split('.')[-1]).split('\'')[0]

        dictio['created_at'] = self.created_at.isoformat()
        dictio['updated_at'] = self.updated_at.isoformat()

        return dictio

    def delete(self):
        """Delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
