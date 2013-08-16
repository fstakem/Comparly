# ------------------------------------------------------
#
#   TestField.py
#   By: Fred Stakem
#   Created: 8.13.13
#
# ------------------------------------------------------


# Libs
import unittest
from copy import deepcopy
from datetime import datetime

# User defined
from Globals import *
from Utilities import *
from Main import Field

#Main
class FieldTest(unittest.TestCase):
    
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
    def testContainsFields(self):
        FieldTest.logger.debug('Test if field contains sub fields.')
        
        # Test data
        field_a = Field('WiFi hardware radio set enabled', [], 'sub_msg')
        field_b = Field('Monitoring hardware for problems.', [], 'sub_msg')
        field_c = Field('wireless card', [], 'module')
        field_d = Field('info', [field_b, field_c], 'level')
        field_e = Field(None, [field_d], 'msg')
        
        # Show test data
        FieldTest.logger.debug('Created field E:\n%s' % field_e.to_pretty_json())
            
        # Run test
        correct_result = field_e.containsFields([field_b, field_c])
        incorrect_result = field_e.containsFields([field_a, field_b])
        
        # Show test output
        FieldTest.logger.debug('Correct result: %s' % correct_result)
        FieldTest.logger.debug('Incorrect result: %s' % incorrect_result)
            
        # Verify results
        assert correct_result , 'The fields were not properly found.'
        assert not incorrect_result, 'The fields were found when not all should not have been.'
           
        FieldTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testContainsField(self):
        FieldTest.logger.debug('Test is field contains sub field.')
        
        # Test data
        field_a = Field('WiFi hardware radio set enabled', [], 'sub_msg')
        field_b = Field('Monitoring hardware for problems.', [], 'sub_msg')
        field_c = Field('info', [field_b], 'level')
        field_d = Field(None, [field_b], 'msg')
        
        # Show test data
        FieldTest.logger.debug('Created field D:\n%s' % field_d.to_pretty_json())
            
        # Run test
        correct_result = field_d.containsField(field_b)
        incorrect_result = field_d.containsField(field_a)
        
        # Show test output
        FieldTest.logger.debug('Correct result: %s' % correct_result)
        FieldTest.logger.debug('Incorrect result: %s' % incorrect_result)
            
        # Verify results
        assert correct_result , 'The field was not properly found.'
        assert not incorrect_result, 'The field was found when it should not have been.'
           
        FieldTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testGetFields(self):
        FieldTest.logger.debug('Test retrieving sub fields.')
        
        # Test data
        field_data_a = 'Monitoring hardware for problems.'
        field_name_a = 'sub_msg'
        field_a = Field(field_data_a, [], field_name_a)
        
        field_data_b = 'info'
        field_name_b = 'level'
        field_b = Field(field_data_b, [field_a], field_name_b)
        
        field_c = Field(None, [field_b], 'msg')
        
        # Show test data
        FieldTest.logger.debug('Created field C:\n%s' % field_c.to_pretty_json())
            
        # Run test
        results = field_c.getFields([field_name_a, field_name_b])
        
        # Show test output
        for i, field in enumerate(results):
            FieldTest.logger.debug('Found field %d:\n%s' % (i, field.to_pretty_json()))
            
        # Verify results
        assert results[0].name == field_name_a, 'The field name found is incorrect.'
        assert results[0].data == field_data_a, 'The field data found is incorrect.'
        assert results[0] == field_a, 'The field found is incorrect.'
        
        assert results[1].name == field_name_b, 'The field name found is incorrect.'
        assert results[1].data == field_data_b, 'The field data found is incorrect.'
        assert results[1] == field_b, 'The field found is incorrect.'
           
        FieldTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testGetField(self):
        FieldTest.logger.debug('Test retrieving a sub field.')
        
        # Test data
        field_data = 'Monitoring hardware for problems.'
        field_name = 'sub_msg'
        field_a = Field(field_data, [], field_name)
        field_b = Field('info', [field_a], 'level')
        field_c = Field(None, [field_b], 'msg')
        
        # Show test data
        FieldTest.logger.debug('Created field C:\n%s' % field_c.to_pretty_json())
            
        # Run test
        result = field_c.getField(field_name)
        
        # Show test output
        FieldTest.logger.debug('Found field:\n%s' % result.to_pretty_json())
            
        # Verify results
        assert result.name == field_name, 'The field name found is incorrect.'
        assert result.data == field_data, 'The field data found is incorrect.'
        assert result == field_a, 'The field found is incorrect.'
           
        FieldTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testBranchesEqual(self): 
        FieldTest.logger.debug('Test branch equality.')
        
        # Test data
        field_a = Field('Monitoring hardware for problems.', [], 'sub_msg')
        field_b = Field('info', [field_a], 'level')
        field_c = Field(None, [field_b], 'msg')
        
        field_d = Field('Monitoring hardware for problems.', [], 'sub_msg')
        field_e = Field('info', [field_d], 'level')
        field_f = Field('Msg Data', [field_e], 'msg')
        
        # Show test data
        FieldTest.logger.debug('Created field C:\n%s' % field_c.to_pretty_json())
        FieldTest.logger.debug('Created field F:\n%s' % field_f.to_pretty_json())
                
        # Verify results
        assert not field_c.branchesEqual(field_f), 'Field C should not equal field F.'
        assert field_b.branchesEqual(field_e), 'Field B should equal field E.'
        
        FieldTest.logger.debug('Test succeeded!')
       
    @log_test(logger, globals.log_separator)
    def testEquality(self):
        FieldTest.logger.debug('Test equality.')
        
        # Test data
        field_a = Field('ubuntu kernel', [], 'component')
        field_b = deepcopy(field_a)
        field_c = Field('ubuntu NetworkManager', [], 'component')
        
        # Show test data
        FieldTest.logger.debug('Created field A:\n%s' % field_a.to_pretty_json())
        FieldTest.logger.debug('Created field B:\n%s' % field_b.to_pretty_json())
        FieldTest.logger.debug('Created field C:\n%s' % field_c.to_pretty_json())
                
        # Verify results
        assert field_a == field_b, 'Field A should equal field B.'
        assert not(field_a == field_c), 'Field A should not equal field C.'
        
        FieldTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testInequality(self):
        FieldTest.logger.debug('Test inequality.')
        
        # Test data
        field_a = Field('ubuntu kernel', [], 'component')
        field_b = deepcopy(field_a)
        field_c = Field('ubuntu NetworkManager', [], 'component')
        
        # Show test data
        FieldTest.logger.debug('Created field A:\n%s' % field_a.to_pretty_json())
        FieldTest.logger.debug('Created field B:\n%s' % field_b.to_pretty_json())
        FieldTest.logger.debug('Created field C:\n%s' % field_c.to_pretty_json())
                
        # Verify results
        assert not(field_a != field_b), 'Field A should equal field B.'
        assert field_a != field_c, 'Field A should not equal field C.'
        
        FieldTest.logger.debug('Test succeeded!')
        

        
 

        

    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     