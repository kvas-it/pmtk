"""
Common initialization for the tests
"""

from os.path import abspath, dirname
import sys

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
