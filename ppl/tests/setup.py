"""
$Id$

Common setup for the tests
"""

import sys
from os.path import abspath, dirname

root = dirname(dirname(dirname(abspath(__file__))))

if root not in sys.path:
    sys.path = [root,] + sys.path

