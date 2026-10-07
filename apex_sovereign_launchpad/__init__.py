"""Apex Sovereign Launchpad: Programmatic GTM, Backlink Mesh, and Spin-Out Hurdle Control Plane.

Governs 370+ sovereign deep-tech repositories under Apex Growth Systems LLC.
Pure Python 3.10+ standard library.
"""

from apex_sovereign_launchpad.core.anti_slop_filter import AntiSlopFilter
from apex_sovereign_launchpad.core.backlink_mesh import BacklinkMeshGenerator
from apex_sovereign_launchpad.core.cockpit_generator import CockpitGenerator
from apex_sovereign_launchpad.core.hurdle_evaluator import HurdleEvaluator
from apex_sovereign_launchpad.core.inventory_parser import COMMERCIAL_HUBS, InventoryParser
from apex_sovereign_launchpad.core.models import (
    AntiSlopMetrics,
    BacklinkMeshResult,
    CommercialHub,
    HurdleEvaluation,
    LaunchWaveManifest,
    MacroPillar,
    RepositoryItem,
)
from apex_sovereign_launchpad.core.super_launcher import SuperLauncher

__version__ = "0.1.0"

__all__ = [
    "AntiSlopFilter",
    "AntiSlopMetrics",
    "BacklinkMeshGenerator",
    "BacklinkMeshResult",
    "COMMERCIAL_HUBS",
    "CockpitGenerator",
    "HurdleEvaluation",
    "HurdleEvaluator",
    "InventoryParser",
    "LaunchWaveManifest",
    "MacroPillar",
    "RepositoryItem",
    "SuperLauncher",
    "__version__",
]
