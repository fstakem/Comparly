# ------------------------------------------------------
#
#   Field.py
#   By: Fred Stakem
#   Created: 8.1.13
#
# ------------------------------------------------------


# Libs
from copy import deepcopy
from collections import OrderedDict

# User defined
from Globals import *
from Utilities import *
from Node import Node

# Main
class Field(Node):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, data=None, children=[], name=__name__):
        super(Field, self).__init__(children, name)
        self.data = data
        
    def containsFields(self, fields):
        for field in fields:
            if not self.containsField(field):
                return False
            
        return True
        
    def containsField(self, field):
        if (self.name == field.name and self.data == field.data) or \
           (self.name == field.name and field.data == None):
            return True
        
        for child in self.children:
            if child.containsField(field):
                return True
            
        return False
    
    def getFields(self, field_names):
        fields = []
        for name in field_names:
            fields.append( self.getField(name) )
        
        return fields
    
    def getField(self, field_name):
        field = None
        
        if self.name == field_name:
            field = self
    
        for child in self.children:
            child_field = child.getField(field_name)
            if child_field != None:
                return child_field
        
        return field
    
    def branchesEqual(self, other):
        if isinstance(other, self.__class__) and self.name == other.name and self.data == other.data:
            for child in self.children:
                not_equal = True
                for other_child in other.children:
                    if child.__eq__(other_child):
                        not_equal = False
                        break
                    
                if not_equal:
                    return False
                
            return True
                
        return False
    
    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.name == other.name and self.data == other.data:
            return True
                
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.name) ^ hash(self.data)
        
            


    
    
                
                
                
                
                
                
                
                
                
            
            