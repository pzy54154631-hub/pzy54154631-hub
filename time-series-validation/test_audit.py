from datetime import date
from pathlib import Path
import unittest

from audit import audit, forward_labels, read_panel


class FoldBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calendar, cls.prices = read_panel(Path(__file__).with_name("sessions.csv"))

    def test_missing_sessions_move_the_endpoint(self):
        labels = forward_labels(self.prices, 2)
        candidates, crossing, eligible = audit(self.calendar, labels, date(2030, 4, 8), 2)
        self.assertEqual((len(candidates), len(crossing), len(eligible)), (7, 2, 5))
        self.assertEqual(
            [(row.series, row.start.day, row.endpoint.day) for row in crossing],
            [("BRAVO", 2, 9), ("BRAVO", 3, 10)],
        )
        self.assertTrue(all(row.endpoint <= date(2030, 4, 8) for row in eligible))
        self.assertAlmostEqual(crossing[0].forward_return, 54 / 50 - 1)

    def test_complete_series_agrees_with_calendar_rule(self):
        labels = forward_labels({"ALPHA": self.prices["ALPHA"]}, 2)
        candidates, crossing, eligible = audit(self.calendar, labels, date(2030, 4, 8), 2)
        self.assertEqual(candidates, eligible)
        self.assertEqual(crossing, [])
        self.assertIn(date(2030, 4, 8), [row.endpoint for row in eligible])

    def test_short_history_does_not_index_from_the_end(self):
        labels = forward_labels(self.prices, 2)
        self.assertEqual(audit(self.calendar, labels, self.calendar[0], 2), ([], [], []))

    def test_no_endpoint_means_no_label(self):
        self.assertEqual(forward_labels(self.prices, len(self.calendar)), [])
        with self.assertRaises(ValueError):
            forward_labels(self.prices, 0)


if __name__ == "__main__":
    unittest.main()
