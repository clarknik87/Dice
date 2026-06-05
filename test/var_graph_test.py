import unittest
from graphlib import CycleError
from dice_parser.parser import DiceParser, ParseError
from dice_parser.var_graph import user_var, var_graph

class TestGraph(unittest.TestCase):
    def test_variable_init(self) -> None:
        p = DiceParser(
            {
                'dex': '3',
                'str': '1',
                'wis': '5',
                'prof': 'level-2',
            },
            {
                'level': '4',
                'stealth': 'dex+prof',
            }
        )
        self.assertEqual(p.parse('dex'), 3)
        self.assertEqual(p.parse('str'), 1)
        self.assertEqual(p.parse('wis'), 5)
        self.assertEqual(p.parse('prof'), 2)
        self.assertEqual(p.parse('level'), 4)
        self.assertEqual(p.parse('stealth'), 5)

    def test_cycle_dependencies(self) -> None:
        p = DiceParser()
        p.parse('prof = 2')
        p.parse('other = prof+1')
        with self.assertRaises(CycleError):
            p.parse('prof = other-1')
    
    def test_update_dependencies(self) -> None:
        p = DiceParser(
            {
            },
            {
                'dex_scr': '18',
                'dex': '(dex_scr-10)/2',
                'prof': '2',
                'stealth': 'dex+prof',
            }
        )
        self.assertEqual(p.parse('dex_scr'), 18)
        self.assertEqual(p.parse('dex'), 4)
        self.assertEqual(p.parse('prof'), 2)
        self.assertEqual(p.parse('stealth'), 6)
        p.parse('prof = 3')
        self.assertEqual(p.parse('dex_scr'), 18)
        self.assertEqual(p.parse('dex'), 4)
        self.assertEqual(p.parse('prof'), 3)
        self.assertEqual(p.parse('stealth'), 7)
        p.parse('dex_scr = 20')
        self.assertEqual(p.parse('dex_scr'), 20)
        self.assertEqual(p.parse('dex'), 5)
        self.assertEqual(p.parse('prof'), 3)
        self.assertEqual(p.parse('stealth'), 8)

    def test_variables_with_builtin_functions(self) -> None:
        p = DiceParser(
            {
            },
            {
                'dex_scr': '18',
                'dex': 'floor(dex_scr-10)/2',
                'prof': '2',
                'stealth': 'dex+prof',
            }
        )
        self.assertEqual(p.parse('dex_scr'), 18)
        self.assertEqual(p.parse('dex'), 4)
        self.assertEqual(p.parse('prof'), 2)
        self.assertEqual(p.parse('stealth'), 6)
        p.parse('dex_scr = 16')
        self.assertEqual(p.parse('dex_scr'), 16)
        self.assertEqual(p.parse('dex'), 3)
        self.assertEqual(p.parse('prof'), 2)
        self.assertEqual(p.parse('stealth'), 5)

    def test_get_functions(self) -> None:
        vars = {
            'dex': '3',
            'str': '1',
            'wis': '5',
            'prof': 'level-2',
        }
        consts = {
            'level': '4',
            'stealth': 'dex+prof',
        }
        p = DiceParser(
            consts,
            vars
        )
        self.assertEqual(vars, p.get_variables_dict())
        self.assertEqual(consts, p.get_constants_dict())