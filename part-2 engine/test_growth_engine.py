import os
import unittest

from growth_engine import mom_growth, is_flagged, validate_feed


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")


class TestGrowthEngine(unittest.TestCase):

    # Test 1
    def test_ethnic_wear_april_to_may(self):
        previous = 104520.77
        current = 185107.61

        growth = mom_growth(previous, current)

        self.assertEqual(growth, 77.1)
        self.assertEqual(is_flagged(growth), "flagged")

    # Test 2
    def test_beauty_june_vs_may(self):
        previous = 35542.11
        current = 37559.07

        growth = mom_growth(previous, current)

        self.assertEqual(growth, 5.67)
        self.assertEqual(is_flagged(growth), "not_flagged")

    # Test 3
    def test_exact_threshold_boundary(self):
        previous = 100000
        current = 108000

        growth = mom_growth(previous, current)

        self.assertEqual(growth, 8.0)
        self.assertEqual(
            is_flagged(growth),
            "escalate_exact_boundary"
        )

    # Test 4
    def test_corrupted_feed(self):
        csv_path = os.path.join(
            FIXTURES_DIR,
            "corrupted_feed.csv"
        )

        valid, errors = validate_feed(csv_path)

        expected_errors = [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)"
        ]

        self.assertFalse(valid)
        self.assertEqual(errors, expected_errors)

    # Test 5
    def test_valid_part1_feed(self):
        csv_path = os.path.join(
            FIXTURES_DIR,
            "monthly_category_revenue.csv"
        )

        valid, errors = validate_feed(csv_path)

        self.assertTrue(valid)
        self.assertEqual(errors, [])

    # Full May vs April MoM table
    def test_may_vs_april_table(self):
        expected = {
            "Ethnic Wear": (104520.77, 185107.61, 77.1),
            "Western Wear": (113866.15, 86998.18, -23.6),
            "Kids Wear": (59847.27, 45793.78, -23.48),
            "Home & Kitchen": (100446.23, 91152.57, -9.25),
            "Beauty & Personal Care": (40737.01, 35542.11, -12.75),
        }

        for category, (previous, current, expected_growth) in expected.items():
            growth = mom_growth(previous, current)

            self.assertEqual(growth, expected_growth)
            self.assertEqual(is_flagged(growth), "flagged")

    # Full June vs May MoM table
    def test_june_vs_may_table(self):
        expected = {
            "Ethnic Wear": (185107.61, 76371.53, -58.74),
            "Western Wear": (86998.18, 97415.64, 11.97),
            "Kids Wear": (45793.78, 56737.78, 23.9),
            "Home & Kitchen": (91152.57, 129971.22, 42.59),
            "Beauty & Personal Care": (35542.11, 37559.07, 5.67),
        }

        for category, (previous, current, expected_growth) in expected.items():
            growth = mom_growth(previous, current)

            self.assertEqual(growth, expected_growth)

            if category == "Beauty & Personal Care":
                self.assertEqual(
                    is_flagged(growth),
                    "not_flagged"
                )
            else:
                self.assertEqual(
                    is_flagged(growth),
                    "flagged"
                )


if __name__ == "__main__":
    unittest.main()