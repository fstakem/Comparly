# ------------------------------------------------------
#
#   CompBase.py
#   By: Fred Stakem
#   Created: 8.12.13
#
# ------------------------------------------------------


# Libs
import json

# User defined
# None

# Main
class CompBase(object):
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)