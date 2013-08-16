# ------------------------------------------------------
#
#   Node.py
#   By: Fred Stakem
#   Created: 7.26.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Utilities import *
from Jsonable import Jsonable

# Main
class Node(Jsonable):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
     
    def __init__(self, children=[], name=__name__):
        super(Jsonable, self).__init__()
        self.name = name
        self.children = children
        
    def isLeaf(self):
        if len(self.children) == 0:
            return True
        
        return False
        
    
        
