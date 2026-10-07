"""Core Domain Models for Apex Sovereign Launchpad.

Governs GTM orchestrations, repository clusters, spin-out hurdle evaluations,
anti-slop propositional metrics, and cross-repo distribution meshes.
Zero external dependencies: 100% pure Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class MacroPillar(str, Enum):
    """The 6 Macro Pillars of Apex Growth Systems LLC."""
    NP_HARD_MICROSECOND = "NP-Hard & Microsecond Systems"
    FRONTIER_AI_SWARMS_MCP = "Frontier AI, Swarms & MCP Ecosystem"
    SOVEREIGN_FINTECH_RAILS = "Sovereign FinTech, Banking & Treasury Rails"
    DUAL_USE_DEFENSE_SPACE = "Dual-Use Defense, Electronic Warfare & Space"
    CLOUD_GRC_SOC = "Cloud GRC, SOC & Enterprise Infrastructure"
    DECISION_SCIENCE_COMMERCE = "Decision Science, Commerce & Bio-Kinematics"


@dataclass
class CommercialHub:
    """The 4 Flagship Commercial Operating Hubs (Candidate Subsidiaries)."""
    hub_id: str
    name: str
    target_buyer: str
    value_proposition: str
    url: str
    blended_cac: float
    annual_arpu: float
    net_ltv: float
    illustrative_cac_ltv_scenario: str


@dataclass
class RepositoryItem:
    """Metadata item representing one of the 370+ repositories."""
    full_name: str
    name: str
    inventory_class: str       # "original" or "fork"
    visibility: str            # "public" or "private"
    description: str
    stars: int
    forks: int
    open_issues: int
    language: Optional[str] = None
    cockpit_cluster: Optional[str] = None
    macro_pillar: MacroPillar = MacroPillar.FRONTIER_AI_SWARMS_MCP
    target_commercial_hub: Optional[str] = None
    featured_in_cockpit: bool = False
    url: str = ""


@dataclass
class HurdleEvaluation:
    """The 4 Quantitative Spin-Out Hurdle Gates Evaluation."""
    target_name: str
    gate1_cac_ltv_ratio: float
    gate1_passed: bool
    gate2_arr_baseline: float
    gate2_passed: bool
    gate3_ringfence_isolation: bool
    gate3_passed: bool
    gate4_strategic_trigger: bool
    gate4_passed: bool
    all_gates_cleared: bool
    recommendation: str  # "MAINTAIN_INCUBATION", "COMMERCIAL_SPRINT", "SPIN_OUT_GRADUATE"
    justification: str


@dataclass
class AntiSlopMetrics:
    """Propositional Information Density (PID) and Entropy Audit."""
    propositional_information_density: float  # |F_empirical| / |W|
    empirical_token_count: int
    slop_token_count: int
    total_token_count: int
    shannon_entropy: float
    is_valid_technical_copy: bool
    rejected_reasons: List[str] = field(default_factory=list)


@dataclass
class LaunchWaveManifest:
    """Programmatic Thematic Super-Launch campaign manifest."""
    wave_number: int
    macro_pillar: MacroPillar
    show_hn_title: str
    executive_abstract: str
    x_thread_bullets: List[str]
    featured_repositories: List[str]
    target_hub_id: str
    anti_slop_metrics: AntiSlopMetrics
    elapsed_microseconds: float = 0.0


@dataclass
class BacklinkMeshResult:
    """Outcome of automated 370-node cross-repository backlink mesh injection."""
    total_repositories_processed: int
    original_repositories_meshed: int
    cross_referral_edges_generated: int
    commercial_hub_referrals_injected: int
    elapsed_microseconds: float = 0.0
