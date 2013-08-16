# ------------------------------------------------------
#
#   UnorderedDiff.py
#   By: Fred Stakem
#   Created: 8.12.13
#
# ------------------------------------------------------


# Libs
from Globals import *

# User defined
from Utilities import *
from EventMatch import EventMatch
from Field import Field

# Main
class UnorderedDiff(object):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
     
    def __init__(self):
        pass
      
    @classmethod  
    def compare(cls, events_a, events_b, filter_fields):
        cls.logger.debug('Starting the unordered diff comparison.')
        
        # Input
        field_names = cls.getFieldNames(filter_fields)
             
        # Output
        matches_both = []
        matches_a_only = []
        matches_b_only = []
        
        cls.logger.debug('Found %d events in the first log.' % (len(events_a)))
        cls.logger.debug('Found %d events in the second log.' % (len(events_b)))
        cls.logger.debug('Found %d fields used for filtering.' % (len(filter_fields)))
        
        for i, field in enumerate(filter_fields):
            cls.logger.debug('Filter field %d:\n%s' % (i, field.to_pretty_json()))
        
        # Filter events
        cls.logger.debug('Filtering the events.')
        events_a = cls.filterEvents(events_a, filter_fields)
        events_b = cls.filterEvents(events_b, filter_fields)
         
        cls.logger.debug('Using %d events from the first log.' % (len(events_a)))
        cls.logger.debug('Using %d events from the second log.' % (len(events_b)))
          
        # Iterate over log A  
        for i, event_a in enumerate(events_a):
            fields_filtered_on = event_a.field.getFields(field_names)
            match = EventMatch(fields_filtered_on)
            
            if globals.debug_diff:
                cls.logger.debug('')
                cls.logger.debug('Working on event %d from the first log.' % (i))
                cls.logger.debug('Events left in second log: %d' % (len(events_b)))
                cls.logger.debug('Match:\n%s' % (str(match)))
            
            # Search for previous match
            for m in matches_both:
                if m == match:
                    match = m
                    if globals.debug_diff:
                        cls.logger.debug('Found a previous match for the current event.')
                    break
             
            # Put the current event into the match
            match.matches_a.append(event_a)    
                    
            # Iterate over log B looking for matches to log A event
            non_matching_events = []
            for event_b in events_b:
                if event_b.field.containsFields(match.fields):
                    match.matches_b.append(event_b)
                else:
                    non_matching_events.append(event_b)
             
            # Set the data so only searching though unmatched values from log B     
            events_b = non_matching_events
            
            # Put the match into the appropriate list
            if len(match.matches_b) == 0:
                matches_a_only.append(match)
                if globals.debug_diff:
                    cls.logger.debug('Only found an event in log A.')
            else:
                matches_both.append(match)
                if globals.debug_diff:
                    cls.logger.debug('Found an event in log A and log B.')
                    
        # Group output    
        for event_b in events_b:
            fields_filtered_on = event_b.field.getFields(field_names)
            match = EventMatch(fields_filtered_on)
            match.matches_b.append(event_b)
            matches_b_only.append(match)   
           
        cls.logger.debug('Finished the comparison.') 
        
        return (matches_both, matches_a_only, matches_b_only)
        
    @classmethod
    def getFieldNames(cls, filter_fields):
        names = []
        for field in filter_fields:
            names.append(field.name)
            
        return names
        
    @classmethod
    def filterEvents(cls, events, filter_fields):
        tmp_events = []
        
        for event in events:
            if event.field.containsFields(filter_fields):
                tmp_events.append(event)
                      
        return tmp_events
    
   
            
                    
            
            
            
            
            
            
            
            
        
    
        
