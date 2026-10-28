import unittest
from datetime import date
from run_analysis import calculate, daily_series, ratio, window_sum


class AnalysisTests(unittest.TestCase):
    def test_unknown_is_not_zero(self):
        self.assertIsNone(ratio(None, 10))
        self.assertIsNone(ratio(1, 0))
        self.assertIsNone(ratio(float("nan"), 10))
        self.assertEqual(ratio(0, 10), 0)

    def test_duplicate_date_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            daily_series([{"date": "2026-10-01", "value_usd": 1}] * 2)

    def test_missing_day_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            window_sum({date(2026, 10, 1): 10}, date(2026, 10, 2), 2)

    def test_empty_and_null_series_are_rejected(self):
        for points in [[], [{"date": "2026-10-01", "value_usd": None}]]:
            with self.assertRaises(ValueError):
                daily_series(points)

    def test_saved_snapshot_and_cutoff(self):
        summary, rows, peers, scenarios, _, _ = calculate()
        self.assertEqual(summary["economic_cutoff"], "2026-10-27")
        self.assertEqual(summary["revenue_30d_usd"], 63870228)
        self.assertEqual(summary["revenue_365d_usd"], 686234852)
        self.assertAlmostEqual(sum(p["cohort_volume_share_pct"] for p in peers), 100)
        self.assertTrue(any(p["revenue_30d_usd"] is None for p in peers))
        self.assertIsNone(summary["actual_buybacks_30d_usd"])

    def test_dilution_sensitivity(self):
        summary, _, _, scenarios, _, _ = calculate()
        self.assertGreater(summary["fdv_to_run_rate"], summary["market_cap_to_run_rate"])
        for row in scenarios:
            self.assertGreater(row["price_current_circulating_usd"], row["price_current_total_supply_usd"])
            self.assertGreater(row["price_current_total_supply_usd"], row["price_initial_max_supply_usd"])


if __name__ == "__main__":
    unittest.main()
