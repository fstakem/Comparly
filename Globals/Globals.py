# ------------------------------------------------------
#
#   Globals.py
#   By: Fred Stakem
#   Created: 6.19.13
#
# ------------------------------------------------------


# Libs
import logging

# User defined
# None

# Globals
log_level = logging.DEBUG
log_format = '%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s'
header_line = '*****************'
footer_line = header_line
log_separator = (header_line, footer_line)

debug_diff = False