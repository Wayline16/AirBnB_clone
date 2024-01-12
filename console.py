#!/usr/bin/python3
"""HBnB Console"""

import cmd
import re
import os
import sys
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

def parse(input_string):
    brackets = re.search(r"\[(.*?)\]", input_string)
    braces   = re.search(r"\{(.*?)\}", input_string)
    if braces is None:
        if brackets is None:
            return [item.strip(",") for item in split(input_string)]
        else:
            lexer_before_backets = input_string[:brackets.span()[0]].split()
            result_list = [item.strip(",") for item in lexer_before_backets]
            result_list.append(brackets.group())
    else:
        lexer_before_braces = input_string[:braces.span()[0]].split()
        result_list = [item.strip(",") for item in lexer_before_braces]
        result_list.append(braces.group())
        return result_list
    

class HBNBCommand(cmd.Cmd):
    """Defines HBNBCommand command interpreter"""
    
    prompt = "(hbnb) "
    __classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }
    
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit"""
        print("")
        return True
    
    def emptyline(self):
        """Do nothing for empty line"""
        pass
    
    def do_create(self, arg):
        """Create command to create a new class instance and prints its id"""
        line = parse(arg)
        if len(line) == 0:
            print("** class doesn't exist **")
        elif line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(line[0])().id)
            storage.save()
        
    def do_show(self, arg):
        """Show command to display a string representation of the class instance of the given id"""
        line = parse(arg)
        objectDictionary = storage.all()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif "{}.{}".format(line[0], line[1]) not in objectDictionary:
            print("** no instance found **")
        else:
            print(objectDictionary["{}.{}".format(line[0], line[1])])

    
    def do_destroy(self, arg):
        """Destroy command to delete a class instance of a given id"""
        line = parse(arg)
        objectDictionary = storage.all()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(line) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(line[0], line[1]) not in objectDictionary:
            print("** no instance found **")
        else:
            del objectDictionary["{}.{}".format(line[0], line[1])]
            storage.save()
            
    """def do_all(self, arg):
        All command to display string representations of all instances of given class
        line = parse(arg)
        if len(line) == 0:
            print([str(a) for a in storage.all().values()])
        elif line not in self.__classes:
            print("** class doesn't exist **")
        else:
            print([str(a) for b, a in storage.all().items() if line in b])"""
    
    def do_all(self, arg):
        """All command to display string representations of all instances of given class"""
        objects = storage.all().values()
        if not arg:
            print([str(obj) for obj in objects])
        elif arg in HBNBCommand.__classes:
            print([str(obj) for obj in objects if type(obj) == HBNBCommand.__classes[arg]])
        else:
            print("** class doesn't exist **")
        
    def do_update(self, arg):
        """Update command to update a class instance of a givenid by adding or updating a given attribute
            key/value pair or dictionary"""
        line = parse(arg)
        objectDictionary = storage.all()
        if len(line) == 0:
            print("** class name missing **")
            return False
        if line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(line) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(line[0], line[1]) not in objectDictionary.keys():
            print("** no instance found **")
            return False
        if len(line) == 2:
            print("** attribute name missing **")
            return False
        if len(line) == 3:
            try:
                type(eval(line[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        
        if len(line) == 4:
            obj = objectDictionary["{}.{}".format(line[0], line[1])]
            if line[2] in obj.__class__.__dict__.keys():
                valueType = type(obj.__class__.__dict__[line[2]])
                obj.__dict__[line[2]] = valueType(line[3])
            else:
                obj.__dict__[line[2]] = line[3]
        elif type(eval(line[2])) == dict:
            obj =objectDictionary["{}.{}".format(line[0], line[1])]
            for key, value in eval(line[2]).items():
                if (key in obj.__class__.__dict__.keys() and type(obj.__class__.__dict__[key]) in {str, int, float}):
                    valueType = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valueType(value)
                else:
                    obj.__dict__[key] = value
        storage.save()
        
    
if __name__ == "__main__":
    HBNBCommand().cmdloop()
    