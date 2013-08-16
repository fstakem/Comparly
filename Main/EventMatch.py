# ------------------------------------------------------
#
#   EventMatch.py
#   By: Fred Stakem
#   Created: 8.12.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Utilities import *
from Jsonable import Jsonable

# Main
class EventMatch(Jsonable):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
     
    def __init__(self, fields=[]):
        super(Jsonable, self).__init__()
        self.fields = fields
        self.matches_a = []
        self.matches_b = []
               
    def __eq__(self, other):
        if set(self.fields) == set(other.fields):
            return True
        
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        output = ''
        for field in self.fields:
            output += 'Field name: %s  Field data: %s\n' % (field.name, field.data) 
            
        output += 'Matches set A: %d  Matches set B: %d' % (len(self.matches_a), len(self.matches_b))    
            
        return output
    

    
    
    