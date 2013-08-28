# ------------------------------------------------------
#
#   TestCompareSyslog.py
#   By: Fred Stakem
#   Created: 8.16.13
#
# ------------------------------------------------------


# Libs
import unittest
from datetime import datetime
import numpy

# User defined
from Globals import *
from Utilities import *

from Corely import Field
from Corely import Event

from Comparly import UnorderedDiff
from Comparly import DistanceCalculator

from Lexly import Stream
from Lexly import RawEventSeparator
from Lexly import Token

from Lexly.Lexer import LexerState
from Lexly.Lexer import LexerStateTransition
from Lexly.Lexer import Lexer

from Lexly.Parser import Parser
from Lexly.Parser import DatetimeParser
from Lexly.Parser import StrParser
from Lexly.Parser import IntParser

#Main
class CompareSyslogTest(unittest.TestCase):
    
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
        globals.debug_diff = False
        self.show_errors = True
        self.fail_on_error = True
        test_files = { 'ubuntu_syslog_old': './logs/ubuntu_logs_7_11_13/syslog',
                       'ubuntu_auth_old': './logs/ubuntu_logs_7_11_13/auth.log', 
                       'ubuntu_kern_old': './logs/ubuntu_logs_7_11_13/kern.log',
                       'ubuntu_syslog_new': './logs/ubuntu_logs_8_12_13/syslog',
                       'ubuntu_auth_new': './logs/ubuntu_logs_8_12_13/auth.log', 
                       'ubuntu_kern_new': './logs/ubuntu_logs_8_12_13/kern.log'}
        self.test_file_old = test_files['ubuntu_syslog_old']
        self.test_file_new = test_files['ubuntu_syslog_new']
        self.filters = { 'syslog_time_filter': {'component': None, 'component_id': None, 'level': None, 'sub_msg':None },
                         'syslog_error_filter': {'component': None, 'component_id': None, 'level': 'error', 'sub_msg':None },
                         'auth_filter': {'component': None, 'component_id': None, 'level': None, 'sub_msg':None },
                         'kern_filter': {'component': None, 'component_id': None, 'level': None, 'sub_msg':None }}
        self.filter = self.filters['syslog_time_filter']
        self.lexer = None
        self.parser = None
        
    def tearDown(self):
        globals.debug_diff = self.tmp_debug_diff
          
    @log_test(logger, globals.log_separator)
    def testUnorderedDiff(self):
        CompareSyslogTest.logger.debug('Test the unordered diff of event logs.')
        
        # Test data
        old_raw_events = self.getData(self.test_file_old)
        CompareSyslogTest.logger.debug('Found %d events from the old log.' % (len(old_raw_events)))
        
        new_raw_events = self.getData(self.test_file_new)
        CompareSyslogTest.logger.debug('Found %d events from the new log.' % (len(new_raw_events)))
            
        self.lexer = self.createEventLexer()
        parsers = self.createEventParser()
        self.parser = parsers[0]
        
        # Run test
        CompareSyslogTest.logger.debug('Working on the old log.')
        old_events = self.parseData(old_raw_events)
        
        CompareSyslogTest.logger.debug('Working on the new log.')
        new_events = self.parseData(new_raw_events)
        
        filter_fields = self.createFilterFields(self.filter)
        CompareSyslogTest.logger.debug('Working on the diff comparison.')
        matches_both, matches_a_only, matches_b_only = UnorderedDiff.compare(old_events, new_events, filter_fields)
        
        # Show test output
        CompareSyslogTest.logger.debug('Found events only in A: %d' % (len(matches_a_only))) 
        CompareSyslogTest.logger.debug('Found events only in B: %d' % (len(matches_b_only)))  
        CompareSyslogTest.logger.debug('Found events in A and B: %d' % (len(matches_both)))
        
        CompareSyslogTest.logger.debug('Test succeeded!')
        
    def parseData(self, raw_events):
        events = []
        all_errors = []
        for i, raw_event in enumerate(raw_events):
            self.lexEvent(raw_event)
            tokens = self.lexer.getAllTokens()
            errors = self.lexer.getAllErrors()
            
            if len(errors) > 0:
                all_errors.append((i, errors))
            else:
                self.parser.start(tokens)
                
                # Verify results 
                errors = self.parser.getAllErrors()
                if len(errors) > 0:
                    all_errors.append((i, errors))
                else:
                    events.append( Event(i, self.parser.getAllFields()) )
                
        CompareSyslogTest.logger.debug('Found the following errors while parsing the data.')   
        for error_set in all_errors:
            CompareSyslogTest.logger.debug('Found %d error(s) parsing event %d.' % (len(error_set[1]), error_set[0]))
            if self.show_errors:
                for error in error_set[1]:
                    CompareSyslogTest.logger.debug('Error:\n%s' % (error.to_pretty_json()))
                    
        # Verify results            
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during parsing.'
            
        return events
             
    def lexEvent(self, event):
        token = Token('event', Token.ALWAYS_DATA, False, event)
        self.lexer.start(token)
        tokens = self.lexer.getAllTokens()
        return tokens
        
    def getData(self, filename):
        CompareSyslogTest.logger.debug('Using test data from file %s.' % (filename))
        test_data = Utilities.readDataFromFile(filename)
        CompareSyslogTest.logger.debug('Found %d bytes in the data file.' % (len(test_data)))
        
        separator = RawEventSeparator('\n', 'Unit Test RawEventSeparator')
        CompareSyslogTest.logger.debug('Created raw event separator:\n%s' % (separator.to_pretty_json()))
        events = separator.seperateEvents(test_data)
        CompareSyslogTest.logger.debug('Found %d events in the data.' % (len(events)))
        
        return events
          
    def createEventLexer(self):
        # End state
        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
        end_state = LexerState([], end_token, True, 'End State')
        
        # Msg lexer
        end_transition = LexerStateTransition('EOS', 0, 0, True, end_state, 'Msg to End Transition')
        msg_token = Token('msg', Token.SOMETIMES_DATA, False, 'Outer Msg Token')
        msg_state = LexerState([end_transition], msg_token, False, 'Outer Msg State')
        msg_sub_lexers, msg_start_state = self.createMsgLexers()
        msg_lexer = Lexer(msg_start_state, 'msg', msg_sub_lexers, 'Outer Msg Lexer')
        
        # Source lexer
        msg_transition = LexerStateTransition(':', 0, 1, True, msg_state, 'Source to Msg Transition')
        source_token = Token('source', Token.ALWAYS_DATA, False, 'Outer Source Token')
        source_state = LexerState([msg_transition], source_token, True, 'Outer Source State')
        source_sub_lexers, source_start_state = self.createSourceLexers()
        source_lexer = Lexer(source_start_state, 'source', source_sub_lexers, 'Outer Source Lexer')
        
        # Datetime lexer
        source_transition = LexerStateTransition('\d{2}:\d{2}:\d{2}', 8, 8, True, source_state, 'Datetime to Source Transition')
        datetime_token = Token('datetime', Token.ALWAYS_DATA, False, 'Outer Datetime Token')
        datetime_state = LexerState([source_transition], datetime_token, False, 'Outer Datetime State')
        datetime_sub_lexers, datetime_start_state = self.createDatetimeLexers()
        datetime_lexer = Lexer(datetime_start_state, 'datetime', datetime_sub_lexers, 'Outer Datetime Lexer')
        
        # Event lexer
        datetime_transition = LexerStateTransition('.', 0, -1, True, datetime_state, 'Event to Datetime Transition')
        event_token = Token('event', Token.NEVER_DATA, False, 'Event Token')
        event_state = LexerState([datetime_transition], event_token, False, 'Event State')
        event_lexer = Lexer(event_state, 'event', [datetime_lexer, source_lexer, msg_lexer], 'Event Lexer')
        
        return event_lexer
    
    def createDatetimeLexers(self):
        # End state
        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
        end_state = LexerState([], end_token, True, 'End State')
        
        # Second lexer
        end_transition = LexerStateTransition('EOS', 0, 0, False, end_state, 'Second to End Transition')
        second_token = Token('second', Token.ALWAYS_DATA, True, 'Second Token')
        second_state = LexerState([end_transition], second_token, False, 'Second State')
        second_lexer = Lexer(None, 'second', [], 'Second Lexer')
        
        # Minute lexer
        second_transition = LexerStateTransition(':', 0, 1, False, second_state, 'Minute to Second Transition')
        minute_token = Token('minute', Token.ALWAYS_DATA, True, 'Minute Token')
        minute_state = LexerState([second_transition], minute_token, False, 'Minute State')
        minute_lexer = Lexer(None, 'minute', [], 'Minute Lexer')
        
        # Hour lexer
        minute_transition = LexerStateTransition(':', 0, 1, False, minute_state, 'Hour to Minute Transition')
        hour_token = Token('hour', Token.ALWAYS_DATA, True, 'Hour Token')
        hour_state = LexerState([minute_transition], hour_token, False, 'Hour State')
        hour_lexer = Lexer(None, 'hour', [], 'Hour Lexer')
        
        # Day lexer
        hour_transition = LexerStateTransition('\s+', 0, 1, True, hour_state, 'Day to Hour Transition')
        day_token = Token('day', Token.ALWAYS_DATA, True, 'Day Token')
        day_state = LexerState([hour_transition], day_token, False, 'Day State')
        day_lexer = Lexer(None, 'day', [], 'Day Lexer')
        
        # Month lexer
        day_transition = LexerStateTransition('\s+', 0, 1, True, day_state, 'Month to Day Transition')
        month_token = Token('month', Token.ALWAYS_DATA, True, 'Month Token')
        month_state = LexerState([day_transition], month_token, False, 'Month State')
        month_lexer = Lexer(None, 'month', [], 'Month Lexer')
        
        # Datetime lexer
        month_transition = LexerStateTransition('.', 0, -1, True, month_state, 'Datetime to Month Transition')
        datetime_token = Token('datetime', Token.NEVER_DATA, False, 'Datetime Token')
        datetime_state = LexerState([month_transition], datetime_token, False, 'Datetime State')
        datetime_lexer = Lexer(None, 'datetime', [], 'Datetime Lexer')
        
        return ((datetime_lexer, month_lexer, day_lexer, hour_lexer, minute_lexer, second_lexer), datetime_state)
    
    def createSourceLexers(self):
        # End state
        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
        end_state = LexerState([], end_token, True, 'End State')
        
        # Component id lexer
        comp_id_to_end_transition = LexerStateTransition('EOS', -1, 0, True, end_state, 'Component ID to End Transition')
        comp_id_token = Token('component_id', Token.SOMETIMES_DATA, True, 'Component ID Token')
        comp_id_state = LexerState([comp_id_to_end_transition], comp_id_token, False, 'Component ID State')
        comp_id_lexer = Lexer(None, 'component_id', [], 'Component ID Lexer')
        
        # Component lexer
        comp_to_end_transition = LexerStateTransition('EOS', 0, 0, True, end_state, 'Component to End Transition')
        comp_id_transition = LexerStateTransition('\[', 0, 1, True, comp_id_state, 'Component to Component ID Transition')
        comp_token = Token('component', Token.ALWAYS_DATA, True, 'Component Token')
        comp_state = LexerState([comp_to_end_transition, comp_id_transition], comp_token, False, 'Component State')
        comp_lexer = Lexer(None, 'component', [], 'Component Lexer')
        
        # Source lexer
        comp_transition = LexerStateTransition('.', 0, -1, False, comp_state, 'Source to Component Transition')
        source_token = Token('source', Token.NEVER_DATA, False, 'Source Token')
        source_state = LexerState([comp_transition], source_token, False, 'Source State')
        source_lexer = Lexer(None, 'source', [], 'Source Lexer')
        
        return ((source_lexer, comp_lexer, comp_id_lexer), source_state)
    
    def createMsgLexers(self):
        # End state
        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
        end_state = LexerState([], end_token, True, 'End State')
        
        # Sub msg lexer
        end_transition = LexerStateTransition('EOS', 0, 1, True, end_state, 'Sub Msg to End Transition')
        sub_msg_token = Token('sub_msg', Token.SOMETIMES_DATA, True, 'Sub Msg Token')
        sub_msg_state = LexerState([end_transition], sub_msg_token, False, 'Sub Msg State')
        sub_msg_lexer = Lexer(None, 'sub_msg', [], 'Sub Msg Lexer')
        
        # Level lexer
        level_to_sub_msg_transition = LexerStateTransition('>', 0, 1, True, sub_msg_state, 'Level to Sub Msg Transition')
        level_token = Token('level', Token.SOMETIMES_DATA, True, 'Level Token')
        level_state = LexerState([level_to_sub_msg_transition], level_token, False, 'Level State')
        level_lexer = Lexer(None, 'level', [], 'Level Lexer')
        
        # Msg lexer
        #precise_seconds_transition = LexerStateTransition('\[', -1, 1, False, precise_seconds_state, 'Msg to Precise Seconds Transition')
        level_transition = LexerStateTransition('[<]', -1, 1, False, level_state, 'Msg to Level Transition')
        sub_msg_transition = LexerStateTransition('[^<]', -1, 0, False, sub_msg_state, 'Msg to Sub Msg Transition')
        end_transition = LexerStateTransition('EOS', 0, 1, True, end_state, 'Msg to End Transition')
        msg_token = Token('msg', Token.NEVER_DATA, False, 'Msg Token')
        msg_state = LexerState([level_transition, sub_msg_transition, end_transition], msg_token, True, 'Msg State')
        msg_lexer = Lexer(None, 'msg', [], 'Msg Lexer')
        
        return ((msg_lexer, level_lexer, sub_msg_lexer), msg_state)
    
    def createEventParser(self):
        # Sub msg parser
        sub_msg_parser = StrParser('sub_msg', [], ['sub_msg'], 'Sub Msg Parser')
        
        # Level parser
        level_parser = StrParser('level', [], ['level'], 'Level Parser')
        
        # Msg parser
        msg_parser = Parser('msg', [level_parser, sub_msg_parser], [], 'Msg Parser')
        
        # Component id parser
        component_id_parser = IntParser('component_id', [], ['component_id'], 'Component ID Parser')
        
        # Component parser
        component_parser = StrParser('component', [], ['component'], 'Component Parser')
        
        # Source parser
        source_parser = Parser('source', [component_parser, component_id_parser], [], 'Source Parser')
        
        # Datetime parser
        datetime_parser = DatetimeParser('timestamp', [], ['month', 'day', 'hour', 'minute', 'second'], 'Datetime Parser')
        
        # Event parser
        event_parser = Parser('event', [datetime_parser, source_parser, msg_parser], [], 'Event Parser')
            
        parsers = (event_parser, datetime_parser, source_parser, component_parser, component_id_parser, 
                   msg_parser, level_parser, sub_msg_parser)
        
        return parsers
    
    def createFilterFields(self, filter):
        fields = []
        for key, value in filter.iteritems():
            fields.append( Field(value, [], key) )
            
        return fields
    
 
        
        
        
        
        
        
        
        