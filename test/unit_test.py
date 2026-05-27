import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import dice_parser

import unittest

from dice_distr_test import TestDiceDisribution
from interpolate_test import TestStringInterpolation
from parser_test import TestParser

if __name__ == '__main__':
    unittest.main()
