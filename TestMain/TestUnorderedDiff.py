# ------------------------------------------------------
#
#   TestUnorderedDiff.py
#   By: Fred Stakem
#   Created: 8.12.13
#
# ------------------------------------------------------


# Libs
import unittest
from datetime import datetime

# User defined
from Globals import *
from Utilities import *
from Main import Field
from Main import Event
from Main import UnorderedDiff

#Main
class UnorderedDiffTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        self.tmp_debug_diff = globals.debug_diff
        globals.debug_diff = True
        
        self.event_data_a = [ [datetime(2013, 7, 11, 9, 51, 12), 'ubuntu kernel', None, None, 'imklog 5.8.11, log source = /proc/kmsg started.'],
                              [datetime(2013, 7, 11, 9, 51, 13), 'ubuntu kernel', None, None, '[    0.000000] Initializing cgroup subsys cpuset'],
                              [datetime(2013, 7, 11, 9, 51, 14), 'ubuntu NetworkManager', 887, None, 'SCPlugin-Ifupdown: init!'],
                              [datetime(2013, 7, 11, 9, 51, 15), 'ubuntu NetworkManager', 887, None, 'SCPluginIfupdown: management mode: unmanaged'],
                              [datetime(2013, 7, 11, 9, 51, 16), 'ubuntu NetworkManager', 887, 'info', 'modem-manager is now available'],
                              [datetime(2013, 7, 11, 9, 51, 17), 'ubuntu NetworkManager', 887, 'info', 'WiFi hardware radio set enabled'],
                              [datetime(2013, 7, 11, 9, 51, 18), 'ubuntu NetworkManager', 887, 'info', 'WiFi hardware radio set enabled'],
                              [datetime(2013, 7, 11, 9, 51, 19), 'ubuntu NetworkManager', 887, 'warn', 'DNS: plugin dnsmasq update failed'],
                              [datetime(2013, 7, 11, 9, 51, 21), 'ubuntu colord', None, None, 'Profile added: icc-0bd9f292ce7882699e93ff844071783d'], ]
        
        self.event_data_b = [ [datetime(2013, 8, 6, 7, 12, 35), 'ubuntu kernel', None, None, 'imklog 5.8.11, log source = /proc/kmsg started.'],
                              [datetime(2013, 8, 6, 7, 12, 36), 'ubuntu kernel', None, None, '[    0.000000] Initializing cgroup subsys cpuset'],
                              [datetime(2013, 8, 6, 7, 12, 37), 'ubuntu NetworkManager', 887, None, 'SCPlugin-Ifupdown: init!'],
                              [datetime(2013, 8, 6, 7, 12, 38), 'ubuntu NetworkManager', 887, None, 'SCPluginIfupdown: management mode: managed'],
                              [datetime(2013, 8, 6, 7, 12, 39), 'ubuntu NetworkManager', 887, 'info', 'modem-manager is now available'],
                              [datetime(2013, 8, 6, 7, 12, 41), 'ubuntu NetworkManager', 887, 'info', 'modem-manager is now available'],
                              [datetime(2013, 8, 6, 7, 12, 42), 'ubuntu NetworkManager', 887, 'info', 'modem-manager is now available'],
                              [datetime(2013, 8, 6, 7, 12, 43), 'ubuntu NetworkManager', 887, 'info', 'WiFi hardware radio set enabled'],
                              [datetime(2013, 8, 6, 7, 12, 44), 'ubuntu NetworkManager', 887, 'error', 'DNS: plugin dnsmasq update failed'],
                              [datetime(2013, 8, 6, 7, 12, 44), 'ubuntu colord', None, None, 'Profile added: icc-0bd9f292ce7882699e93ff844071783d'], ]
        
    def tearDown(self):
        globals.debug_diff = self.tmp_debug_diff
          
    @log_test(logger, globals.log_separator)
    def testCompare(self):
        UnorderedDiffTest.logger.debug('Test the comparison of event logs.')
        
        # Test data
        events_a = self.createEventLog(self.event_data_a)
        events_b = self.createEventLog(self.event_data_b)
        filter = {'component': None, 'component_id': None, 'level': None, 'sub_msg':None }
        filter_fields = self.createFilterFields(filter)
            
        # Run test
        matches_both, matches_a_only, matches_b_only = UnorderedDiff.compare(events_a, events_b, filter_fields)
          
        # Show test output
        UnorderedDiffTest.logger.debug('Found events only in A: %d' % (len(matches_a_only))) 
        UnorderedDiffTest.logger.debug('Found events only in B: %d' % (len(matches_b_only)))  
        UnorderedDiffTest.logger.debug('Found events in A and B: %d' % (len(matches_both)))  
            
        # Verify results
        assert len(matches_both) == 7, 'Found an incorrect number of events in both A and B.'
        assert len(matches_a_only) == 2, 'Found the incorrect number of A only events.'
        assert len(matches_b_only) == 2, 'Found the incorrect number of B only events.'
        
        UnorderedDiffTest.logger.debug('Test succeeded!')
            
    @log_test(logger, globals.log_separator)
    def testFilterCompare(self):
        UnorderedDiffTest.logger.debug('Test the comparison of event logs with filtering.')
        
        # Test data
        events_a = self.createEventLog(self.event_data_a)
        events_b = self.createEventLog(self.event_data_b)
        filter = {'component': 'ubuntu kernel', 'component_id': None, 'level': None, 'sub_msg':None }
        filter_fields = self.createFilterFields(filter)
            
        # Run test
        matches_both, matches_a_only, matches_b_only = UnorderedDiff.compare(events_a, events_b, filter_fields)
          
        # Show test output
        UnorderedDiffTest.logger.debug('Found events only in A: %d' % (len(matches_a_only))) 
        UnorderedDiffTest.logger.debug('Found events only in B: %d' % (len(matches_b_only)))  
        UnorderedDiffTest.logger.debug('Found events in A and B: %d' % (len(matches_both)))  
            
        # Verify results
        assert len(matches_both) == 2, 'Found an incorrect number of events in both A and B.'
        assert len(matches_a_only) == 0, 'Found the incorrect number of A only events.'
        assert len(matches_b_only) == 0, 'Found the incorrect number of B only events.'
        
        UnorderedDiffTest.logger.debug('Test succeeded!')
        
    def createEventLog(self, data):
        events = []
        for i, ed in enumerate(data):
            events.append( self.createEvent(i, ed[0], ed[1], ed[2], ed[3], ed[4]))
        
        return events
     
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
    
   
 

        

    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     