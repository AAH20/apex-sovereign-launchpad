"""Sovereign Spin-Out Hurdle Rate Evaluation Engine.

Codifies the 4 quantitative hurdle gates from Apex Growth Systems LLC:
- Gate 1: CAC:LTV >= 1:4 (Payback < 6-9 months)
- Gate 2: Recurring Retainer ARR > $250k
- Gate 3: Sovereign Liability / Regulatory Ring-Fencing
- Gate 4: Surgical Transaction Trigger (Dedicated ESOP / Acqui-hire)
Zero external dependencies: 100% pure Python standard library.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from apex_sovereign_launchpad.core.models import CommercialHub, HurdleEvaluation


class HurdleEvaluator:
    """Evaluates whether an incubated technical cluster earns subsidiary status."""

    def __init__(self, min_cac_ltv: float = 4.0, min_arr: float = 250000.0):
        self.min_cac_ltv = min_cac_ltv
        self.min_arr = min_arr

    def evaluate_candidate(
        self,
        candidate_name: str,
        cac: float,
        arpu: float,
        annual_churn: float = 0.05,
        gross_margin: float = 0.85,
        current_arr: float = 0.0,
        regulatory_isolation_needed: bool = False,
        strategic_transaction_trigger: bool = False,
    ) -> HurdleEvaluation:
        """Evaluates candidate against the 4 Sovereign Spin-Out Hurdle Gates."""
        # 1. Calculate LTV
        churn = max(0.01, annual_churn)
        ltv = (arpu * gross_margin) / churn
        cac_effective = max(1.0, cac)
        cac_ltv_ratio = ltv / cac_effective

        # Gate 1
        g1_passed = cac_ltv_ratio >= self.min_cac_ltv

        # Gate 2
        g2_passed = current_arr >= self.min_arr

        # Gate 3
        g3_passed = regulatory_isolation_needed

        # Gate 4
        g4_passed = strategic_transaction_trigger

        all_cleared = g1_passed and g2_passed and g3_passed and g4_passed

        # Formulate recommendation
        if all_cleared:
            rec = "SPIN_OUT_GRADUATE"
            just = f"Cleared all 4 Gates: CAC:LTV is 1:{cac_ltv_ratio:.1f}, ARR is ${current_arr:,.0f}, and regulatory/strategic triggers are satisfied. Authorized for subsidiary spin-out."
        elif g1_passed and (current_arr >= 50000.0 or g3_passed):
            rec = "COMMERCIAL_SPRINT"
            just = f"High CAC:LTV (1:{cac_ltv_ratio:.1f}) but ARR (${current_arr:,.0f}) is below $250k threshold. Deploy fixed-price commercial testing sprints within Apex Growth Systems LLC."
        else:
            rec = "MAINTAIN_INCUBATION"
            just = f"Keep incubated inside master IP vault at zero legal overhead. Premature incorporation avoided (Zero Delaware taxes, zero holding dilution)."

        return HurdleEvaluation(
            target_name=candidate_name,
            gate1_cac_ltv_ratio=round(cac_ltv_ratio, 2),
            gate1_passed=g1_passed,
            gate2_arr_baseline=current_arr,
            gate2_passed=g2_passed,
            gate3_ringfence_isolation=regulatory_isolation_needed,
            gate3_passed=g3_passed,
            gate4_strategic_trigger=strategic_transaction_trigger,
            gate4_passed=g4_passed,
            all_gates_cleared=all_cleared,
            recommendation=rec,
            justification=just,
        )

    def evaluate_hub(self, hub: CommercialHub, current_arr: float = 0.0, is_strategic: bool = False) -> HurdleEvaluation:
        """Evaluates a standard commercial hub using its established economic parameters."""
        req_isolation = hub.hub_id in ("sovereign_rails", "a2zsoc")
        return self.evaluate_candidate(
            candidate_name=hub.name,
            cac=hub.blended_cac,
            arpu=hub.annual_arpu,
            current_arr=current_arr,
            regulatory_isolation_needed=req_isolation,
            strategic_transaction_trigger=is_strategic,
        )
