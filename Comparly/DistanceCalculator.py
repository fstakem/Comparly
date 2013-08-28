# ------------------------------------------------------
#
#   DistanceCalculator.py
#   By: Fred Stakem
#   Created: 8.21.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Globals import *
from Utilities import *

# Main
class DistanceCalculator(object):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod  
    def calculate(cls, event_a, event_b, weights, normalize):
        distance = 0.0
        if normalize:
            weights = cls.normalizeWeights(weights)
        
        for key, value in weights.iteritems():
            field_a = event_a.field.getField(key)
            field_b = event_b.field.getField(key)
            
            if (field_a != field_b) or (field_a == None and field_b == None):
                distance += value
            
        return distance
                
    @classmethod
    def normalizeWeights(cls, weights):
        normalized_weights = {}
        total = 0.0
        
        for value in weights.values():
            total += float(value)
            
        for key, value in weights.iteritems():
            normalized_weights[key] = value / total
        
        return normalized_weights
    
 
   
    
    
    
                
            