from datetime import date
from pathlib import Path
import unittest

from audit import audit, fixed_session_targets, forward_labels, read_panel


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

    def test_fixed_session_missing_price_remains_null(self):
        rows = fixed_session_targets(self.calendar, self.prices, date(2030, 4, 8), 2)
        self.assertEqual(len(rows), 7)
        missing = [(row.series, row.start.day, row.endpoint.day)
                   for row in rows if row.forward_return is None]
        self.assertEqual(missing, [("BRAVO", 2, 4), ("BRAVO", 3, 5)])
        self.assertEqual(sum(row.forward_return is not None for row in rows), 5)

    def test_fixed_session_accepts_gaps_between_observed_endpoints(self):
        rows = fixed_session_targets(self.calendar, self.prices, date(2030, 4, 9), 4)
        row = next(row for row in rows if row.series == "BRAVO" and row.start.day == 3)
        self.assertEqual(row.endpoint, date(2030, 4, 9))
        self.assertAlmostEqual(row.forward_return, 54 / 51 - 1)
        self.assertTrue(all(row.endpoint <= date(2030, 4, 9) for row in rows))

    def test_fixed_session_cannot_use_a_post_cutoff_quote(self):
        cutoff = date(2030, 4, 8)
        truncated = {name: [(day, px) for day, px in obs if day <= cutoff]
                     for name, obs in self.prices.items()}
        self.assertEqual(fixed_session_targets(self.calendar, self.prices, cutoff, 2),
                         fixed_session_targets(self.calendar, truncated, cutoff, 2))
        self.assertEqual(fixed_session_targets(self.calendar, self.prices, cutoff, 20), [])


if __name__ == "__main__":
    unittest.main()
