# ------------------------------------------------------
#
#   TestDistanceCalculator.py
#   By: Fred Stakem
#   Created: 8.12.13
#
# ------------------------------------------------------


# Libs
import unittest
import json
from datetime import datetime

# User defined
from Globals import *
from Utilities import *

from Corely import Field
from Corely import Event

from Comparly import DistanceCalculator

#Main
class DistanceCalculatorTest(unittest.TestCase):
    
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
    def testCalculate(self):
        DistanceCalculatorTest.logger.debug('Test the distance calculation.')
        
        # Test data
        event_data_a = [datetime(2013, 7, 11, 9, 51, 17), 'ubuntu NetworkManager', 887, 'info', 'WiFi hardware radio set enabled']
        event_data_b = [datetime(2013, 8, 6, 7, 12, 43), 'ubuntu NetworkManager', 887, 'error', 'WiFi hardware radio set disabled']
        weights = { 'component': 3, 'component_id': 1, 'level': 2, 'sub_msg': 2}
        
        event_a = self.createEvent(0, event_data_a[0], event_data_a[1], event_data_a[2], event_data_a[3], event_data_a[4])
        event_b = self.createEvent(0, event_data_b[0], event_data_b[1], event_data_b[2], event_data_b[3], event_data_b[4])
        
        # Show test data
        DistanceCalculatorTest.logger.debug('Event A:\n%s' % event_a.to_pretty_json())
        DistanceCalculatorTest.logger.debug('Event B:\n%s' % event_b.to_pretty_json())
        DistanceCalculatorTest.logger.debug('Weights: %s' % weights)
        
        # Run test
        distance = DistanceCalculator.calculate(event_a, event_b, weights, False)
        normal_distance = DistanceCalculator.calculate(event_a, event_b, weights, True)
        
        # Show test output
        DistanceCalculatorTest.logger.debug('Calculated distance: %s' % str(distance))
        DistanceCalculatorTest.logger.debug('Calculated normalized distance: %s' % str(normal_distance))
            
        # Verify results
        assert distance == 4.0, 'Incorrect distance calculation.'
        assert normal_distance == 0.5, 'Incorrect distance calculation.'
        
        DistanceCalculatorTest.logger.debug('Test succeeded!')
        
        
    @log_test(logger, globals.log_separator)
    def testNormalizeWeights(self):
        DistanceCalculatorTest.logger.debug('Test the weight normalization.')
        
        # Test data
        weights = { 'component': 3, 'component_id': 1, 'level': 2, 'sub_msg': 2}
         
        # Show test data
        DistanceCalculatorTest.logger.debug('Weights:\n%s' % json.dumps(weights, indent=4))
        
        # Run test
        new_weights = DistanceCalculator.normalizeWeights(weights)
        
        # Show test output
        DistanceCalculatorTest.logger.debug('Normalized weights:\n%s' % json.dumps(new_weights, indent=4))
            
        # Verify results
        assert new_weights['component'] == 0.375, 'Incorrect weight adjustment.'
        assert new_weights['component_id'] == 0.125, 'Incorrect weight adjustment.'
        assert new_weights['level'] == 0.25, 'Incorrect weight adjustment.'
        assert new_weights['sub_msg'] == 0.25, 'Incorrect weight adjustment.'
        
        DistanceCalculatorTest.logger.debug('Test succeeded!')
        
    def createEvent(self, index, timestamp_data, component_data, component_id_data, level_data, sub_msg_data):
        sub_msg = Field(sub_msg_data, [], 'sub_msg')
        level = Field(level_data, [], 'level')
        msg = Field(None, [level, sub_msg], 'msg')
        component_id = Field(component_id_data, [], 'component_id')
        component = Field(component_data, [], 'component')
        source = Field(None, [component, component_id], 'source')
        timestamp = Field(timestamp_data, [], 'timestamp')
        msg = Field(None, [timestamp, source, msg], 'event')
        
        event = Event(index, msg)
        
        return event
    
    def createFilterFields(self, filter):
        fields = []
        for key, value in filter.iteritems():
            fields.append( Field(value, [], key) )
            
        return fields
        
        
        
        
        
            
      