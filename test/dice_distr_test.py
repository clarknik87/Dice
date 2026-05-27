import unittest
from dataclasses import dataclass

from dice_parser.dice_distr import DiceDistribution

@dataclass
class DiceResult:
    formula : str|DiceDistribution
    minimum : int|None
    maximum : int|None
    expected: float|None
    variance: float|None
    std_dev : float|None

class TestDiceDisribution(unittest.TestCase):
    def assert_dice_result(self, formulas: list[DiceResult]) -> None:
        for case in formulas:
            if isinstance(case.formula, str):
                distr = DiceDistribution(case.formula)
            elif isinstance(case.formula, DiceDistribution):
                distr = case.formula
            else:
                raise TypeError(f"unable to construct distr from type {type(case.formula)}")

            if case.minimum is not None:
                self.assertEqual(distr.minimum(), case.minimum)
            if case.maximum is not None:
                self.assertEqual(distr.maximum(), case.maximum)
            if case.expected is not None:
                self.assertAlmostEqual(distr.expected_value(), case.expected, places=3)
            if case.variance is not None:
                self.assertAlmostEqual(distr.variance(), case.variance, places=3)
            if case.std_dev is not None:
                self.assertAlmostEqual(distr.standard_dev(), case.std_dev, places=3)

    def test_nds_ctor(self) -> None:
        formulas = [
            DiceResult('1d2', 1, 2, 1.5, 0.25, 0.5),
            DiceResult('1d4', 1, 4, 2.5, 1.2499, 1.1180),
            DiceResult('1d6', 1, 6, 3.5, 2.9166, 1.7078),
            DiceResult('1d20', 1, 20, 10.5, 33.2502, 5.7663),
            DiceResult('6d2', 6, 12, 9, 1.500, 1.2247),
            DiceResult('16d1', 16, 16, 16, 0.0, 0.0),
            DiceResult('4d6', 4, 24, 14, 11.6671, 3.4157),
            DiceResult('3d8', 3, 24, 13.5, 15.7500, 3.9686),
            DiceResult('0d20', 0, 0, 0, 0.0, 0.0),
        ]
        self.assert_dice_result(formulas)

    def test_adv_ctor(self) -> None:
        formulas = [
            DiceResult('adv', 1, 20, 13.825, 22.1944, 4.7111),
        ]
        self.assert_dice_result(formulas)

    def test_dis_ctor(self) -> None:
        formulas = [
            DiceResult('dis', 1, 20, 7.175, 22.1944, 4.7111),
        ]
        self.assert_dice_result(formulas)

    def test_max_ctor(self) -> None:
        formulas = [
            DiceResult('max(2d20)', 1, 20, 13.825, 22.1944, 4.7111),
            DiceResult('max(4d4)', 1, 4, 3.6172, 0.3769, 0.6139),
            DiceResult('max(6d1)', 1, 1, 1, 0.0, 0.0),
            DiceResult('max(1d20)', 1, 20, 10.5, 33.2502, 5.7663),
            DiceResult('max(0d20)', 0, 0, 0, 0.0, 0.0),
        ]
        self.assert_dice_result(formulas)

    def test_min_ctor(self) -> None:
        formulas = [
            DiceResult('min(2d20)', 1, 20, 7.175, 22.1944, 4.7111),
            DiceResult('min(4d4)', 1, 4, 1.3828, 0.3769, 0.6139),
            DiceResult('min(6d1)', 1, 1, 1, 0.0, 0.0),
            DiceResult('min(1d20)', 1, 20, 10.5, 33.2502, 5.7663),
            DiceResult('min(0d20)', 0, 0, 0, 0.0, 0.0),
        ]
        self.assert_dice_result(formulas)

    def test_complex_max_ctor(self) -> None:
        formulas = [
            DiceResult('max(1,2d20)', 1, 20, 13.825, 22.1944, 4.7111),
            DiceResult('max(2,4d4)', 2, 8, 6.5156, 1.6404, 1.2808),
            DiceResult('max(5,6d1)', 5, 5, 5, 0.0, 0.0),
            DiceResult('max(1,1d20)', 1, 20, 10.5, 33.2502, 5.7663),
            DiceResult('max(0,1d20)', 0, 0, 0, 0.0, 0.0),
            DiceResult('max(0,0d20)', 0, 0, 0, 0.0, 0.0),
        ]
        self.assert_dice_result(formulas)

    def test_complex_min_ctor(self) -> None:
        formulas = [
            DiceResult('min(1,2d20)', 1, 20, 7.175, 22.1944, 4.7111),
            DiceResult('min(2,4d4)', 2, 8, 3.4844, 1.6404, 1.2808),
            DiceResult('min(5,6d1)', 5, 5, 5, 0.0, 0.0),
            DiceResult('min(1,1d20)', 1, 20, 10.5, 33.2502, 5.7663),
            DiceResult('max(0,1d20)', 0, 0, 0, 0.0, 0.0),
            DiceResult('max(0,0d20)', 0, 0, 0, 0.0, 0.0),
        ]
        self.assert_dice_result(formulas)

    def test_invalid_ctor(self) -> None:
        with self.assertRaises(ValueError):
            DiceDistribution()

    def test_invalid_expr(self) -> None:
        expr_list = [
            'asdflkjsdf',
            'ad10',
            'min(7dc10)',
            'max(c,3d20)',
            'advg',
            'disb',
            '0adv',
            'xdis',
            '1adv3',
            'cdisb',
            '2d0',
            '0d0',
            '-1d6',
            'max(-2d20)',
            'min(-1d10)',
            'max(2,-3d4)',
            'min(3,-5d6)',
            'max(3,2d20)',
            'min(4,1d10)'
        ]
        for expr in expr_list:
            with self.assertRaises(ValueError):
                DiceDistribution(expr)

    def test_eq_overload(self) -> None:
        # Test comparison with int
        self.assertAlmostEqual(DiceDistribution('1d1') == 1, 1.0)
        self.assertAlmostEqual(DiceDistribution('1d20') == 1, 0.05)
        # test comparison with float
        self.assertAlmostEqual(DiceDistribution('1d20') == 1.0, 0.05)
        with self.assertRaises(ValueError):
            _ = (DiceDistribution('1d20') == 1.1)
        # test comparison with other DiceDistribution
        self.assertAlmostEqual(DiceDistribution('1d1') == DiceDistribution('1d1'), 1.0)
        self.assertAlmostEqual(DiceDistribution('1d1') == DiceDistribution('1d10'), 0.1)
        self.assertAlmostEqual(DiceDistribution('1d2') == DiceDistribution('1d2'), 0.5)
        self.assertAlmostEqual(DiceDistribution('1d20') == DiceDistribution('1d20'), 0.05)
        # test comparison with invalid type
        with self.assertRaises(TypeError):
            _ = (DiceDistribution('1d20') == "1d4")

    def test_ne_overload(self) -> None:
        # Test comparison with int
        self.assertAlmostEqual(DiceDistribution('1d1') != 2, 1.0)
        self.assertAlmostEqual(DiceDistribution('1d20') != 1, 0.95)
        # test comparison with float
        self.assertAlmostEqual(DiceDistribution('1d20') != 1.0, 0.95)
        with self.assertRaises(ValueError):
            _ = (DiceDistribution('1d20') != 1.1)
        # test comparison with other DiceDistribution
        self.assertAlmostEqual(DiceDistribution('1d1') != DiceDistribution('1d1'), 0.0)
        self.assertAlmostEqual(DiceDistribution('1d1') != DiceDistribution('1d10'), 0.9)
        self.assertAlmostEqual(DiceDistribution('1d2') != DiceDistribution('1d2'), 0.5)
        self.assertAlmostEqual(DiceDistribution('1d20') != DiceDistribution('1d20'), 0.95)
        # test comparison with invalid type
        with self.assertRaises(TypeError):
            _ = (DiceDistribution('1d20') == "1d4")
    
    def test_le_overload(self) -> None:
        # Test comparison with int
        self.assertAlmostEqual(DiceDistribution('1d1') <= 1, 1.0)
        self.assertAlmostEqual(DiceDistribution('1d20') <= 2, 0.10)
        # test comparison with float
        self.assertAlmostEqual(DiceDistribution('1d20') <= 1.0, 0.05)
        with self.assertRaises(ValueError):
            _ = (DiceDistribution('1d20') <= 1.1)
        # test comparison with other DiceDistribution
        self.assertAlmostEqual(DiceDistribution('1d1') <= DiceDistribution('1d1'), 1.0)
        self.assertAlmostEqual(DiceDistribution('1d10') <= DiceDistribution('1d1'), 0.1)
        self.assertAlmostEqual(DiceDistribution('1d2') <= DiceDistribution('1d2'), 0.75)
        self.assertAlmostEqual(DiceDistribution('1d20') <= DiceDistribution('1d20'), 0.525)
        # test comparison with invalid type
        with self.assertRaises(TypeError):
            _ = (DiceDistribution('1d20') <= "1d4") # type: ignore

    def test_lt_overload(self) -> None:
        # Test comparison with int
        self.assertAlmostEqual(DiceDistribution('1d1') < 1, 0.0)
        self.assertAlmostEqual(DiceDistribution('1d20') < 2, 0.05)
        # test comparison with float
        self.assertAlmostEqual(DiceDistribution('1d20') < 2.0, 0.05)
        with self.assertRaises(ValueError):
            _ = (DiceDistribution('1d20') < 1.1)
        # test comparison with other DiceDistribution
        self.assertAlmostEqual(DiceDistribution('1d1') < DiceDistribution('1d1'), 0.0)
        self.assertAlmostEqual(DiceDistribution('1d10') < DiceDistribution('2d1'), 0.1)
        self.assertAlmostEqual(DiceDistribution('1d2') < DiceDistribution('1d2'), 0.25)
        self.assertAlmostEqual(DiceDistribution('1d20') < DiceDistribution('1d20'), 0.475)
        # test comparison with invalid type
        with self.assertRaises(TypeError):
            _ = (DiceDistribution('1d20') < "1d4") # type: ignore
    
    def test_ge_overload(self) -> None:
        # Test comparison with int
        self.assertAlmostEqual(DiceDistribution('1d1') >= 1, 1.0)
        self.assertAlmostEqual(DiceDistribution('1d20') >= 2, 0.95)
        # test comparison with float
        self.assertAlmostEqual(DiceDistribution('1d20') >= 2.0, 0.95)
        with self.assertRaises(ValueError):
            _ = (DiceDistribution('1d20') >= 1.1)
        # test comparison with other DiceDistribution
        self.assertAlmostEqual(DiceDistribution('1d1') >= DiceDistribution('1d1'), 1.0)
        self.assertAlmostEqual(DiceDistribution('1d1') >= DiceDistribution('1d10'), 0.1)
        self.assertAlmostEqual(DiceDistribution('1d2') >= DiceDistribution('1d2'), 0.75)
        self.assertAlmostEqual(DiceDistribution('1d20') >= DiceDistribution('1d20'), 0.525)
        # test comparison with invalid type
        with self.assertRaises(TypeError):
            _ = (DiceDistribution('1d20') <= "1d4") # type: ignore

    def test_gt_overload(self) -> None:
        # Test comparison with int
        self.assertAlmostEqual(DiceDistribution('1d1') > 1, 0.0)
        self.assertAlmostEqual(DiceDistribution('1d20') > 2, 0.90)
        # test comparison with float
        self.assertAlmostEqual(DiceDistribution('1d20') > 2.0, 0.90)
        with self.assertRaises(ValueError):
            _ = (DiceDistribution('1d20') > 1.1)
        # test comparison with other DiceDistribution
        self.assertAlmostEqual(DiceDistribution('1d1') > DiceDistribution('1d1'), 0.0)
        self.assertAlmostEqual(DiceDistribution('1d1') > DiceDistribution('1d10'), 0.0)
        self.assertAlmostEqual(DiceDistribution('1d2') > DiceDistribution('1d2'), 0.25)
        self.assertAlmostEqual(DiceDistribution('1d20') > DiceDistribution('1d20'), 0.475)
        # test comparison with invalid type
        with self.assertRaises(TypeError):
            _ = (DiceDistribution('1d20') > "1d4") # type: ignore

    def test_neg_overload(self) -> None:
        formulas = [
            '1d6',
            'adv',
            'max(2d20)',
            'min(3,4d6)',
        ]
        for formula in formulas:
            d = DiceDistribution(formula)
            self.assertEqual(d, -(-d))

    def test_add_overload(self) -> None:
        formulas = [
            DiceResult(DiceDistribution('1d1')+1, 2, 2, 2, 0.0, 0.0),
            DiceResult(1+DiceDistribution('1d1'), 2, 2, 2, 0.0, 0.0),
            DiceResult(DiceDistribution('1d1')+0, 1, 1, 1, 0.0, 0.0),
            DiceResult(0+DiceDistribution('1d1'), 1, 1, 1, 0.0, 0.0),
            DiceResult(DiceDistribution('0d6')+2.0, 2, 2, 2.0, 0.0, 0.0),
            DiceResult(2.0+DiceDistribution('0d6'), 2, 2, 2.0, 0.0, 0.0),
            DiceResult(DiceDistribution('2d4')+4, 6, 12, 9.0, 2.5, 1.5811),
            DiceResult(4+DiceDistribution('2d4'), 6, 12, 9.0, 2.5, 1.5811),
            DiceResult(DiceDistribution('adv')+5, 6, 25, 18.825, 22.1944, 4.71109),
            DiceResult(5+DiceDistribution('adv'), 6, 25, 18.825, 22.1944, 4.71109),
            DiceResult(DiceDistribution('max(3,4d6)')+1, 4, 19, 13.2446, 8.1045, 2.8468),
        ]
        self.assert_dice_result(formulas)

    def test_sub_overload(self) -> None:
        formulas = [
            DiceResult(DiceDistribution('1d1')-1, 0, 0, 0, 0.0, 0.0),
            DiceResult(1-DiceDistribution('1d1'), 0, 0, 0, 0.0, 0.0),
            DiceResult(DiceDistribution('1d1')-0, 1, 1, 1, 0.0, 0.0),
            DiceResult(0-DiceDistribution('1d1'), -1, -1, -1, 0.0, 0.0),
            DiceResult(DiceDistribution('0d6')-2.0, -2, -2, -2.0, 0.0, 0.0),
            DiceResult(2.0-DiceDistribution('0d6'), 2, 2, 2.0, 0.0, 0.0),
            DiceResult(DiceDistribution('2d4')-4, -2, 4, 1.0, 2.5, 1.5811),
            DiceResult(4-DiceDistribution('2d4'), -4, 2, -1.0, 2.5, 1.5811),
            DiceResult(DiceDistribution('adv')-5, -4, 15, 8.825, 22.1944, 4.71109),
            DiceResult(5-DiceDistribution('adv'), -15, 4, -8.825, 22.1944, 4.71109),
            DiceResult(DiceDistribution('max(3,4d6)')-1, 2, 17, 11.2446, 8.1045, 2.8468),
        ]
        self.assert_dice_result(formulas)
    
    def test_mul_overload(self) -> None:
        formulas = [
            DiceResult(DiceDistribution('1d1')*1, 1, 1, 1, 0.0, 0.0),
            DiceResult(1*DiceDistribution('1d1'), 1, 1, 1, 0.0, 0.0),
            DiceResult(DiceDistribution('1d1')*0, 0, 0, 0, 0.0, 0.0),
            DiceResult(0*DiceDistribution('1d1'), 0, 0, 0, 0.0, 0.0),
            DiceResult(DiceDistribution('0d6')*2.0, 0, 0, 0.0, 0.0, 0.0),
            DiceResult(2.0*DiceDistribution('0d6'), 0, 0, 0.0, 0.0, 0.0),
            DiceResult(DiceDistribution('2d4')*4, 8, 32, 20.0, 40.0, 6.3246),
            DiceResult(4*DiceDistribution('2d4'), 8, 32, 20.0, 40.0, 6.3246),
            DiceResult(DiceDistribution('adv')*5, 5, 100, 69.125, 554.8594, 23.5555),
            DiceResult(5*DiceDistribution('adv'), 5, 100, 69.125, 554.8594, 23.5555),
            DiceResult(DiceDistribution('max(3,4d6)')*1, 3, 18, 12.2446, 8.1045, 2.8468),
        ]
        self.assert_dice_result(formulas)

    def test_roll(self) -> None:
        formulas = [
            DiceResult('1d1', 1, 1, None, None, None),
            DiceResult('1d4', 1, 4, None, None, None),
            DiceResult('1d6', 1, 6, None, None, None),
            DiceResult('1d10', 1, 10, None, None, None),
            DiceResult('1d20', 1, 20, None, None, None),
            DiceResult('adv', 1, 20, None, None, None),
        ]
        for case in formulas:
            for _ in range(20):
                if isinstance(case.formula, str) and isinstance(case.minimum, int) and isinstance(case.maximum, int):
                    d = DiceDistribution(case.formula)
                    self.assertGreaterEqual(d.roll(), case.minimum)
                    self.assertLessEqual(d.roll(), case.maximum)

    def test_roll_full(self) -> None:
        formulas = [
            DiceResult('1d1', 1, 1, None, None, None),
            DiceResult('1d4', 1, 4, None, None, None),
            DiceResult('1d6', 1, 6, None, None, None),
            DiceResult('1d10', 1, 10, None, None, None),
            DiceResult('1d20', 1, 20, None, None, None),
            DiceResult('adv', 1, 20, None, None, None),
        ]
        for case in formulas:
            for _ in range(20):
                if isinstance(case.formula, str) and isinstance(case.minimum, int) and isinstance(case.maximum, int):
                    d = DiceDistribution(case.formula)
                    self.assertGreaterEqual(d.roll_full()[0], case.minimum)
                    self.assertLessEqual(d.roll_full()[0], case.maximum)
