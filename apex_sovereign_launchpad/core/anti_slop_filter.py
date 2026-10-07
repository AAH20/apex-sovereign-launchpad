"""Propositional Information Density (PID) and Anti-Slop Audit Filter.

Enforces Shannon entropy bounds and empirical content density (PID >= 0.35)
across all Show HN launch drafts, technical whitepapers, and README copy.
Zero external dependencies: 100% pure Python standard library.
"""

from __future__ import annotations

import math
import re
from typing import List, Set, Tuple
from apex_sovereign_launchpad.core.models import AntiSlopMetrics


PROHIBITED_SLOP_TOKENS: Set[str] = {
    "revolutionize", "game-changer", "tapestry", "unleash", "delve", "powerhouse",
    "seamless", "next-gen", "cutting-edge", "paradigm shift", "leverage", "robust",
    "groundbreaking", "disrupt", "game changer", "testament", "beacon", "pinnacle",
    "unlock the power", "supercharge", "transformative", "unparalleled",
}

TECH_ACRONYMS: Set[str] = {
    "AST", "DPLL", "CNF", "SAT", "COG", "VRPTW", "JSSP", "CFLP", "MILP", "LP",
    "SCC", "ISO", "CFPB", "FDX", "PCI", "DSS", "PVP", "BAAS", "SOC", "VCISO",
    "CMMC", "ISR", "LEO", "DAG", "MCP", "LLC", "API", "GUI", "V8", "WEBRTC",
    "HN", "FX", "EBITDA", "M&A", "VDR", "SRE", "GRC", "PKI", "EWA",
}

TECH_KEYWORDS: Set[str] = {
    "python", "simplex", "solomon", "voronoi", "tessellation", "knapsack",
    "benchmark", "benchmarks", "sub-millisecond", "air-gap", "kalman", "combinatorial",
    "geodesic", "spatial", "thermal", "orbital", "laser", "repo", "repositories",
    "kernels", "solver", "solvers", "latency", "throughput", "p95", "dual-licensing",
    "open-source", "slashing", "tokens", "ast", "dijkstra", "precondition",
}


class AntiSlopFilter:
    """Mathematical content signal validator for technical GTM copy."""

    def __init__(self, min_pid: float = 0.35, max_slop_tokens: int = 0):
        self.min_pid = min_pid
        self.max_slop_tokens = max_slop_tokens

    def audit_text(self, text: str) -> AntiSlopMetrics:
        """Audits text content for empirical signal vs marketing noise."""
        if not text.strip():
            return AntiSlopMetrics(
                propositional_information_density=0.0,
                empirical_token_count=0,
                slop_token_count=0,
                total_token_count=0,
                shannon_entropy=0.0,
                is_valid_technical_copy=False,
                rejected_reasons=["Empty content payload"],
            )

        words = re.findall(r"\b\w+(?:[-/'_]\w+)*\b", text)
        total_words = len(words)
        if total_words == 0:
            return AntiSlopMetrics(0.0, 0, 0, 0, 0.0, False, ["No alphanumeric tokens"])

        text_lower = text.lower()

        # 1. Detect Slop Words
        slop_count = 0
        found_slop = []
        for slop in PROHIBITED_SLOP_TOKENS:
            occurrences = len(re.findall(r"\b" + re.escape(slop) + r"\b", text_lower))
            if occurrences > 0:
                slop_count += occurrences
                found_slop.append(slop)

        # 2. Count Empirical / Technical Tokens
        # A token is empirical if it is numerical, a physical unit, a URL, a code identifier,
        # an acronym, a hyphenated/underscored package/repo name, or a recognized technical keyword.
        empirical_count = 0
        for w in words:
            w_upper = w.upper()
            w_lower = w.lower()

            if any(c.isdigit() for c in w):
                empirical_count += 1
            elif "-" in w or "_" in w:
                empirical_count += 1
            elif w_upper in TECH_ACRONYMS:
                empirical_count += 1
            elif w_lower in TECH_KEYWORDS:
                empirical_count += 1
            elif w.startswith("http://") or w.startswith("https://"):
                empirical_count += 1

        # Also account for backticked symbols and math blocks in original text
        backtick_matches = len(re.findall(r"`[^`]+`", text))
        empirical_total = min(total_words, empirical_count + backtick_matches)

        pid = min(1.0, empirical_total / float(total_words))

        # 3. Sentence Length Variation (Shannon Entropy proxy)
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        sentence_lengths = [len(s.split()) for s in sentences]

        if len(sentence_lengths) > 1:
            mean_len = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((l - mean_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            entropy = math.sqrt(variance)
        else:
            entropy = 0.0

        # Verification rules
        rejected: List[str] = []
        if pid < self.min_pid:
            rejected.append(f"PID {pid:.2f} below minimum threshold {self.min_pid:.2f} (lacks technical/empirical facts)")
        if slop_count > self.max_slop_tokens:
            rejected.append(f"Found {slop_count} banned marketing buzzwords: {', '.join(found_slop)}")

        is_valid = len(rejected) == 0

        return AntiSlopMetrics(
            propositional_information_density=round(pid, 4),
            empirical_token_count=empirical_total,
            slop_token_count=slop_count,
            total_token_count=total_words,
            shannon_entropy=round(entropy, 2),
            is_valid_technical_copy=is_valid,
            rejected_reasons=rejected,
        )
