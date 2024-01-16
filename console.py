#!/usr/bin/python3
"""HBnB Console"""
 
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }


    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            line = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", line[1])
            if match is not None:
                command = [line[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(line[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

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
            print("** class name missing **")
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
        elif len(line) == 1:
            print("** instance id missing **")
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
        elif "{}.{}".format(line[0], line[1]) not in objectDictionary.keys():
            print("** no instance found **")
        else:
            del objectDictionary["{}.{}".format(line[0], line[1])]
            storage.save()

    def do_all(self, arg):
        """All command to display string representations of all instances of given class"""
        line = parse(arg)
        if len(line) > 0 and line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objectLine = []
            for obj in storage.all().values():
                if len(line) > 0 and line[0] == obj.__class__.__name__:
                    objectLine.append(obj.__str__())
                elif len(line) == 0:
                    objectLine.append(obj.__str__())
            print(objectLine)

    def do_count(self, arg):
        """Count command to return the number of instances of the given class"""
        line = parse(arg)
        count = 0
        for obj in storage.all().values():
            if line[0] == obj.__class__.__name__:
                count += 1
        print(count)

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
                valtype = type(obj.__class__.__dict__[line[2]])
                obj.__dict__[line[2]] = valtype(line[3])
            else:
                obj.__dict__[line[2]] = line[3]
        elif type(eval(line[2])) == dict:
            obj = objectDictionary["{}.{}".format(line[0], line[1])]
            for k, v in eval(line[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()