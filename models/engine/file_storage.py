#!/usr/bin/python3
"""FileStorage Class"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """FileStorage Class
    __file_path (str): The name/path of the file to save objects to.
    __objects (dict): A dictionary of objects. Will store by <class name>.id
    """
    
    __file_path = "file.json"
    __objects = {}
    
    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects
    
    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        ObjectClassName = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ObjectClassName, obj.id)] = obj
        
    """def save(self):
        Serializes __objects to the JSON file(path;__file-path)
        Dictionary = FileStorage.__objects
        ObjectDictionary = {obj: Dictionary[obj].to_dict for obj in Dictionary.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(ObjectDictionary, f)"""
            
    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        ObjectDictionary = {}
        for key, obj in FileStorage.__objects.items():
            ObjectDictionary[str(key)] = obj.to_dict()

        with open(FileStorage.__file_path, "w") as f:
            json.dump(ObjectDictionary, f)
    
    
    def reload(self):
        """Deserializes the JSON file to __objects if __file_path exists,
        Do nothing if __file_path doesn't exist
        """
        try:
            with open(FileStorage.__file_path) as f:
                ObjectDictionary =json.load(f)
                for object in ObjectDictionary.values():
                    ClassName = object["__class__"]
                    del object["__class__"]
                    self.new(eval(ClassName)(**object))
        except FileNotFoundError:
            return