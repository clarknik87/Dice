import unittest

from dice_parser.parser import DiceParser, ParseError
from dice_parser.dice_distr import DiceDistribution, DiceStats

std_array = {
    'str' : 10.0,
    'dex' : 16.0,
    'con' : 14.0,
    'int' : 10.0,
    'wis' : 10.0,
    'cha' : 11.0,
}

class TestParser(unittest.TestCase):
    def test_assignment_valid(self) -> None:
        p = DiceParser()
        self.assertTrue(p.parse('fireball = 8d6') is None)
        self.assertTrue(p.parse('fireball = 9d6') is None)

    def test_assignment_invalid(self) -> None:
        p = DiceParser(
            constants=std_array,
        )
        self.assertEqual(p.parse('str = 12'), ParseError.ERR_CONST_ASSIGNMENT)

    def test_parse_plus(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1+1'), 2)
        self.assertEqual(p.parse('1+1.5'), 2.5)
        self.assertEqual(p.parse('1+0'), 1)
        self.assertEqual(p.parse('0+1'), 1)
        self.assertEqual(p.parse('0+0'), 0)
        self.assertEqual(p.parse('1d1+6'), 7)

    def test_parse_minus(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1-1'), 0)
        self.assertEqual(p.parse('1-1.5'), -0.5)
        self.assertEqual(p.parse('1-0'), 1)
        self.assertEqual(p.parse('0-1'), -1)
        self.assertEqual(p.parse('0-0'), 0)
        self.assertEqual(p.parse('1d1-6'), -5)

    def test_parse_times(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1*1'), 1)
        self.assertEqual(p.parse('1*1.5'), 1.5)
        self.assertEqual(p.parse('1*0'), 0)
        self.assertEqual(p.parse('0*1'), 0)
        self.assertEqual(p.parse('0*0'), 0)
        self.assertEqual(p.parse('1d1*6'), 6)
        self.assertEqual(p.parse('1d4*2d4'), ParseError.ERR_TYPE_UNSUPPORTED)

    def test_parse_divide(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1/1'), 1)
        self.assertEqual(p.parse('1.5/1'), 1.5)
        self.assertEqual(p.parse('0/1'), 0)
        self.assertEqual(p.parse('1/0'), ParseError.ERR_ZERO_DIVISION)
        self.assertEqual(p.parse('1/2d4'), ParseError.ERR_TYPE_UNSUPPORTED)

    def test_parse_uminus(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('-1'), -1)
        self.assertEqual(p.parse('-6.0'), -6)
        self.assertEqual(p.parse('-1d1'), -1)

    def test_return_types(self) -> None:
        p = DiceParser(constants=std_array)
        self.assertTrue(isinstance(p.parse('1'), float))
        self.assertTrue(isinstance(p.parse('1.0'), float))
        self.assertTrue(isinstance(p.parse('1d20'), DiceDistribution))
        self.assertTrue(isinstance(p.parse('adv'), DiceDistribution))
        self.assertTrue(isinstance(p.parse('max(4,5d6)'), DiceDistribution))
        self.assertTrue(isinstance(p.parse('dis+5'), DiceDistribution))
        self.assertTrue(isinstance(p.parse('str'), float))
        self.assertTrue(isinstance(p.parse('sdfsdf'), ParseError))

    def test_parenthesis(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1+2*3'), 7)
        self.assertEqual(p.parse('(1+2)*3'), 9)
        self.assertEqual(p.parse('(1+3*2)*3'), 21)
        self.assertEqual(p.parse('((1+3)*2)*3'), 24)
        self.assertEqual(p.parse('((1d1+3)*2)*3'), 24)

    def test_parse_eq(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1 == 1'), 1.0)
        self.assertEqual(p.parse('1 == 0'), 0.0)
        self.assertEqual(p.parse('1d1 == 1'), 1.0)
        self.assertEqual(p.parse('0d1 == 0'), 1.0)
        self.assertEqual(p.parse('1d20 == 1'), 0.05)

    def test_parse_ne(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1 != 1'), 0.0)
        self.assertEqual(p.parse('1 != 0'), 1.0)
        self.assertEqual(p.parse('1d1 != 1'), 0.0)
        self.assertEqual(p.parse('0d1 != 0'), 0.0)
        self.assertEqual(p.parse('1d20 != 1'), 0.95)

    def test_parse_gt(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1 > 1'), 0.0)
        self.assertEqual(p.parse('1 > 0'), 1.0)
        self.assertEqual(p.parse('1d1 > 1'), 0.0)
        self.assertEqual(p.parse('0d1 > 0'), 0.0)
        self.assertEqual(p.parse('1d20 > 1'), 0.95)

    def test_parse_ge(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1 >= 1'), 1.0)
        self.assertEqual(p.parse('1 >= 0'), 1.0)
        self.assertEqual(p.parse('1d1 >= 1'), 1.0)
        self.assertEqual(p.parse('0d1 >= 0'), 1.0)
        self.assertEqual(p.parse('1d20 >= 1'), 1.0)

    def test_parse_lt(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1 < 1'), 0.0)
        self.assertEqual(p.parse('1 < 0'), 0.0)
        self.assertEqual(p.parse('1d1 < 1'), 0.0)
        self.assertEqual(p.parse('0d1 < 0'), 0.0)
        self.assertEqual(p.parse('1d20 < 1'), 0.0)

    def test_parse_le(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('1 <= 1'), 1.0)
        self.assertEqual(p.parse('1 <= 0'), 0.0)
        self.assertEqual(p.parse('1d1 <= 1'), 1.0)
        self.assertEqual(p.parse('0d1 <= 0'), 1.0)
        self.assertEqual(p.parse('1d20 <= 1'), 0.05)

    def test_functions(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('sqrt(4)'), 2)
        self.assertEqual(p.parse('ceil(4.1)'), 5)
        self.assertEqual(p.parse('round(4.1)'), 4)
        self.assertEqual(p.parse('floor(4.8)'), 4)
        self.assertEqual(p.parse('pow(2,4)'), 16)
        self.assertEqual(p.parse('int(2.4)'), 2)
        self.assertEqual(p.parse('float(2.4)'), 2.4)
    
    def test_roll_function(self) -> None:
        p = DiceParser()
        self.assertEqual(p.parse('roll(4d1)'), 4)
        self.assertEqual(p.parse('roll(6d1)'), 6)
        self.assertEqual(p.parse('roll(4d1+7)'), 11)
        self.assertEqual(p.parse('roll(7)'), ParseError.ERR_INVALID_FUNC_ARG)
        self.assertEqual(p.parse('roll(7,3)'), ParseError.ERR_INVALID_FUNC_ARG)

    def test_stats_function(self) -> None:
        p = DiceParser()
        self.assertIsInstance(p.parse('stats(1d20)'), DiceStats)
        r = p.parse('stats(1d20)')
        if isinstance(r, DiceStats):
            self.assertEqual(r.expr, '1d20')
            self.assertEqual(r.minimum, 1)
            self.assertEqual(r.maximum, 20)
            self.assertEqual(r.average, 10.5)
            self.assertAlmostEqual(r.stddev, 5.7663, places=3)
