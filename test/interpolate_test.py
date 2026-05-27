import unittest
from dataclasses import dataclass

from dice_parser.parser import DiceParser

std_array = {
    'str' : 10.0,
    'dex' : 16.0,
    'con' : 14.0,
    'int' : 10.0,
    'wis' : 10.0,
    'cha' : 11.0,
}

class TestStringInterpolation(unittest.TestCase):
    def test_null_case(self) -> None:
        expr_lst = [
            r'1d12+7',
            r'plain text',
            r'hello world {',
            r'}',
        ]
        parser = DiceParser()
        for expr in expr_lst:
            self.assertEqual(parser.interpolate(expr), expr)
    
    def test_basic_case(self) -> None:
        expr_lst = [
            ('1d20+{dex}', f'1d20+{float(std_array['dex'])}'),
            ('{str}, {cha}', f'{float(std_array['str'])}, {float(std_array['cha'])}'),
            ('adv+{wis}', f'adv+{float(std_array['wis'])}'),
            ('{str} text {', f'{float(std_array['str'])} text {{'),
            ('{} test', ' test'),
            ('{} test {', ' test {'),
        ]
        parser = DiceParser(variables=std_array)
        for expr in expr_lst:
            self.assertEqual(parser.interpolate(expr[0]), expr[1])
