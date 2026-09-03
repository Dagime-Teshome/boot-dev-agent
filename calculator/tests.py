# calculator/tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_addition(self) -> None:
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self) -> None:
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self) -> None:
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self) -> None:
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_modulo(self) -> None:
        result = self.calculator.evaluate("10 % 3")
        self.assertEqual(result, 1)

    def test_modulo_with_precedence(self) -> None:
        result = self.calculator.evaluate("3 * 4 % 5")
        self.assertEqual(result, 2)

    def test_nested_expression(self) -> None:
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self) -> None:
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self) -> None:
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self) -> None:
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    # ---- New percentage tests ----

    def test_percentage_postfix(self) -> None:
        """20pct (postfix) divides the number by 100."""
        result = self.calculator.evaluate("20pct")
        self.assertEqual(result, 0.2)

    def test_percentage_of_value(self) -> None:
        """200 * 20pct should give 40."""
        result = self.calculator.evaluate("200 * 20pct")
        self.assertEqual(result, 40)

    def test_percentage_addition(self) -> None:
        """50 + 50pct should give 50.5."""
        result = self.calculator.evaluate("50 + 50pct")
        self.assertEqual(result, 50.5)

    def test_percentage_subtraction(self) -> None:
        """100 - 25pct should give 99.75 (since 25pct == 0.25)."""
        result = self.calculator.evaluate("100 - 25pct")
        self.assertEqual(result, 99.75)

    def test_percentage_chain(self) -> None:
        """Chaining percentages: 100 * 10pct * 20pct should give 2."""
        result = self.calculator.evaluate("100 * 10pct * 20pct")
        self.assertEqual(result, 2)

    def test_lone_percent_as_modulo_still_works(self) -> None:
        """The regular % operator still performs modulo."""
        result = self.calculator.evaluate("10 % 3")
        self.assertEqual(result, 1)

    def test_modulo_inside_expression_with_percentage(self) -> None:
        """Modulo and percentage should not interfere with each other."""
        result = self.calculator.evaluate("20pct + 10 % 3")
        self.assertEqual(result, 1.2)


if __name__ == "__main__":
    unittest.main()