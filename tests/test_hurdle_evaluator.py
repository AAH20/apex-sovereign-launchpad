"""Unit tests for HurdleEvaluator and 4 Spin-Out Hurdle Gates."""

import unittest
from apex_sovereign_launchpad.core.hurdle_evaluator import HurdleEvaluator
from apex_sovereign_launchpad.core.inventory_parser import COMMERCIAL_HUBS


class TestHurdleEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = HurdleEvaluator(min_cac_ltv=4.0, min_arr=250000.0)

    def test_full_spinout_graduation(self):
        # Meets all 4 gates
        ev = self.evaluator.evaluate_candidate(
            candidate_name="a2zsoc Corp",
            cac=3200.0,
            arpu=50000.0,
            annual_churn=0.04,
            current_arr=300000.0,
            regulatory_isolation_needed=True,
            strategic_transaction_trigger=True,
        )
        self.assertTrue(ev.all_gates_cleared)
        self.assertEqual(ev.recommendation, "SPIN_OUT_GRADUATE")
        self.assertTrue(ev.gate1_passed)
        self.assertTrue(ev.gate2_passed)
        self.assertTrue(ev.gate3_passed)
        self.assertTrue(ev.gate4_passed)

    def test_commercial_sprint_recommendation(self):
        # High CAC:LTV and regulatory need, but ARR is $80k (< $250k)
        ev = self.evaluator.evaluate_candidate(
            candidate_name="Sovereign Rails Unit",
            cac=5000.0,
            arpu=60000.0,
            annual_churn=0.05,
            current_arr=80000.0,
            regulatory_isolation_needed=True,
            strategic_transaction_trigger=False,
        )
        self.assertFalse(ev.all_gates_cleared)
        self.assertEqual(ev.recommendation, "COMMERCIAL_SPRINT")
        self.assertTrue(ev.gate1_passed)
        self.assertFalse(ev.gate2_passed)

    def test_maintain_incubation_low_unit_economics(self):
        # Low LTV relative to CAC (CAC:LTV < 4.0)
        ev = self.evaluator.evaluate_candidate(
            candidate_name="Early Experimental Kernel",
            cac=10000.0,
            arpu=500.0,
            annual_churn=0.10,
            current_arr=0.0,
            regulatory_isolation_needed=False,
            strategic_transaction_trigger=False,
        )
        self.assertFalse(ev.all_gates_cleared)
        self.assertEqual(ev.recommendation, "MAINTAIN_INCUBATION")
        self.assertFalse(ev.gate1_passed)


if __name__ == "__main__":
    unittest.main()
