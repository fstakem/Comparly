# ------------------------------------------------------
#
#   TestEventMatch.py
#   By: Fred Stakem
#   Created: 8.15.13
#
# ------------------------------------------------------


# Libs
import unittest
from copy import deepcopy

# User defined
from Globals import *
from Utilities import *
from Main import Field
from Main import EventMatch

#Main
class EventMatchTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_separator)
    def testEquality(self):
        EventMatchTest.logger.debug('Test equality.')
        
        # Test data
        field_a = Field('Monitoring hardware for problems.', [], 'sub_msg')
        field_b = Field('info', [field_a], 'level')
        field_c = Field(None, [field_b], 'msg')
        
        event_match_a = EventMatch(field_c.getFields(['sub_msg', 'level']))
        event_match_b = deepcopy(event_match_a)
        event_match_c = EventMatch(field_c.getFields(['level']))
        
        # Show test data
        EventMatchTest.logger.debug('Created event match A:\n%s' % str(event_match_a))
        EventMatchTest.logger.debug('Created event match B:\n%s' % str(event_match_b))
        EventMatchTest.logger.debug('Created event match C:\n%s' % str(event_match_c))
                
        # Verify results
        assert event_match_a == event_match_b, 'The event matches should be equal.'
        assert not (event_match_a == event_match_c), 'The event matches should not be equal.'
           
        EventMatchTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testInequality(self):
        EventMatchTest.logger.debug('Test equality.')
        
        # Test data
        field_a = Field('Monitoring hardware for problems.', [], 'sub_msg')
        field_b = Field('info', [field_a], 'level')
        field_c = Field(None, [field_b], 'msg')
        
        event_match_a = EventMatch(field_c.getFields(['sub_msg', 'level']))
        event_match_b = deepcopy(event_match_a)
        event_match_c = EventMatch(field_c.getFields(['level']))
        
        # Show test data
        EventMatchTest.logger.debug('Created event match A:\n%s' % str(event_match_a))
        EventMatchTest.logger.debug('Created event match B:\n%s' % str(event_match_b))
        EventMatchTest.logger.debug('Created event match C:\n%s' % str(event_match_c))
                
        # Verify results
        assert not (event_match_a != event_match_b), 'The fields were not properly found.'
        assert event_match_a != event_match_c, 'The fields were found when not all should not have been.'
           
        EventMatchTest.logger.debug('Test succeeded!')
        
        
        
        
 