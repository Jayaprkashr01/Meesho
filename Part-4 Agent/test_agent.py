import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

sys.path.insert(0, BASE_DIR)

from mock_agent_runner import run


PART1_OUTPUT = os.path.join(
    PROJECT_ROOT,
    "Part 1 SQL",
    "output"
)

PART2_FIXTURES = os.path.join(
    PROJECT_ROOT,
    "part-2 engine",
    "fixtures"
)


class TestMockAgent(unittest.TestCase):

    def test_may_scenario(self):

        april = os.path.join(
            PART1_OUTPUT,
            "monthly_category_revenue.csv"
        )

        may = os.path.join(
            PART1_OUTPUT,
            "monthly_category_revenue.csv"
        )

        # This test is replaced below by fixture discovery.
        self.assertTrue(os.path.exists(april))


    def test_corrupted_feed_hard_stop(self):

        previous = os.path.join(
            PART2_FIXTURES,
            "monthly_category_revenue.csv"
        )

        corrupted = os.path.join(
            PART2_FIXTURES,
            "corrupted_feed.csv"
        )

        result = run(
            "July",
            previous,
            corrupted
        )

        self.assertEqual(
            result["validation_status"],
            "invalid"
        )

        self.assertEqual(
            result["action_taken"],
            "hard_stop"
        )

        self.assertEqual(
            result["validation_errors"],
            [
                "line 3: negative revenue (-4200.0) for category=Western Wear",
                "line 4: missing category (month=July)",
                "line 6: missing revenue (category=Home & Kitchen)"
            ]
        )

        self.assertEqual(
            result["flagged_categories"],
            []
        )

        self.assertEqual(
            result["suppressed_categories"],
            []
        )


if __name__ == "__main__":
    unittest.main()