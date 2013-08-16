# ------------------------------------------------------
#
#   Event.py
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
class Event(Jsonable):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
     
    def __init__(self, order=0, field=None):
        super(Jsonable, self).__init__()
        self.order = order
        self.field = field
        
    
    
    