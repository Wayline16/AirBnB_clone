#!/usr/bin/python3
"""BaseModel Class"""
import models
from datetime import datetime
from uuid import uuid4

class BaseModel:
    """BaseModel Class"""
    
    def __init__(self, *args, **kwargs):
        """Initializing the BaseModel
        *aqrgs wont be used
        if **kwargs is not empty - key/value pairs of attributes
        """
        TimeFormat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at  = datetime.today()
        
        if len(kwargs) != 0:
            for i, j in kwargs.items():
                if i == "created_at" or i == "updated_at":
                    self.__dict__[i] = datetime.strptime(j, TimeFormat)
                else:
                    self.__dict__[i] = j
        
    def __str__(self):
        """
        Return the string with the format - 
        [<class name>] (<self.id>) <self.__dict__>
        """
        ClassName = self.__class__.__name__
        return "[{} ({} {})]".format(ClassName, self.id, self.__dict__)
    
    def save(self):
        """
        Updates the public instance attribute updated_at with the current datetime
        """
        self.updated_at = datetime.today()
        
    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__ of the instance
        """
        Dictionary = self.__dict__.copy()
        Dictionary["created_at"] = self.created_at.isoformat()
        Dictionary["updated_at"] = self.updated_at.isoformat()
        Dictionary["__class__"] = self.__class__.__name__
        return Dictionary
        
 