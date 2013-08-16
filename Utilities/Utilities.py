# ------------------------------------------------------
#
#   Utilities.py
#   By: Fred Stakem
#   Created: 6.19.13
#
# ------------------------------------------------------


# Libs
import logging
import sys

# User defined
from Globals import *

# Main
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def getLogger(name='GenericLogger'):
    logger = logging.getLogger(name)
    logger.setLevel(globals.log_level)
    formatter = logging.Formatter(globals.log_format)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def log_test(logger, log_seperators):
    def log(func):
        def onCall(self):
            output = log_seperators[0]
            output += ' START ' + func.func_name + '() '
            output += log_seperators[0]
            logger.debug(output)
            
            func(self)
            
            output = log_seperators[0]
            output += ' FINISHED ' + func.func_name + '() '
            output += log_seperators[1]
            logger.debug(output)
            logger.debug('')
        return onCall
    return log

def debug_log(logger, debug_on=False):
    def debug(func):
        def onCall(self, *args, **kwargs):
            if debug_on:
                logger.debug('Before %s()' % (func.func_name))
                lines = ( str(self) ).split('\n')
                for line in lines:
                    logger.debug('\t%s' % (line))
                
            data = func(self, *args, **kwargs)
            
            if debug_on:
                logger.debug('After %s()' % (func.func_name))
                lines = ( str(self) ).split('\n')
                for line in lines:
                    logger.debug('\t%s' % (line))
                    
            return data
        return onCall
    return debug

def readDataFromFile(filename):
    f = open(filename, "r")
    file_data = f.read()
    f.close()
    
    return file_data



