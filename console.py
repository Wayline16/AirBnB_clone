#!/usr/bin/python3
"""HBnB Console"""

import cmd


class HBNBCommand(cmd.Cmd):
    """Defines HBNBCommand command interpreter"""
    
    prompt = "(hbnb) "
    
    def do_quit(self, arg):
        """Command to exit"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit"""
        print("")
        return True
    
    def emptyline(self):
        """Do nothing for empty line"""
        pass

    
if __name__ == "__main__":
    HBNBCommand().cmdloop()
    