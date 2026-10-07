"""Unit tests for AntiSlopFilter and Propositional Information Density."""

import unittest
from apex_sovereign_launchpad.core.anti_slop_filter import AntiSlopFilter


class TestAntiSlopFilter(unittest.TestCase):
    def setUp(self):
        self.filter = AntiSlopFilter(min_pid=0.30, max_slop_tokens=0)

    def test_high_signal_technical_copy_passes(self):
        technical_text = """
We benchmarked the DPLL SAT solver across 1,000 CNF clauses.
The mean latency is 9.67µs with p95 latency of 12.50µs and 103,389 solves/sec.
The AST contains 15 nodes and verifies `x > 0` implies `result >= 0` with 0 external dependencies.
Available at https://github.com/AAH20/apex-industrial-solver
"""
        metrics = self.filter.audit_text(technical_text)
        self.assertTrue(metrics.is_valid_technical_copy)
        self.assertGreaterEqual(metrics.propositional_information_density, 0.30)
        self.assertEqual(metrics.slop_token_count, 0)

    def test_marketing_buzzwords_rejected(self):
        slop_text = """
This revolutionary powerhouse tool will unleash your developer productivity!
It is a seamless game-changer designed to disrupt the industry and supercharge workflows.
"""
        metrics = self.filter.audit_text(slop_text)
        self.assertFalse(metrics.is_valid_technical_copy)
        self.assertTrue(metrics.slop_token_count >= 2)
        self.assertTrue(any("banned marketing buzzwords" in r for r in metrics.rejected_reasons))

    def test_empty_string_rejected(self):
        metrics = self.filter.audit_text("   ")
        self.assertFalse(metrics.is_valid_technical_copy)


if __name__ == "__main__":
    unittest.main()
