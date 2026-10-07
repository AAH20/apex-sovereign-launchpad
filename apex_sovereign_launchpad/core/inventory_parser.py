"""Portfolio Repository Inventory Parser.

Parses repository_inventory.json across all 554 repositories (370 originals),
classifying them into the 6 Macro Pillars and mapping them to the 4 Commercial Hubs.
Zero external dependencies: 100% pure Python standard library.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from apex_sovereign_launchpad.core.models import (
    CommercialHub,
    MacroPillar,
    RepositoryItem,
)


# The 4 Commercial Operating Hubs defined in Global_HoldingCompany_Architectures
COMMERCIAL_HUBS: Dict[str, CommercialHub] = {
    "a2zsoc": CommercialHub(
        hub_id="a2zsoc",
        name="a2zsoc Corp (Enterprise GRC & Agentic vCISO Swarm)",
        target_buyer="Global Enterprise CISOs, Regulated Cloud Datacenters, GovCloud",
        value_proposition="1,100+ Controls, Zero-Human Evidence Harvester, Continuous vCISO",
        url="https://a2zsoc.com",
        blended_cac=3200.0,
        annual_arpu=45000.0,
        net_ltv=250000.0,
        illustrative_cac_ltv_scenario="1:37 to 1:140",
    ),
    "investor_os": CommercialHub(
        hub_id="investor_os",
        name="InvestorOS LLC (Algorithmic M&A Diligence & Valuation)",
        target_buyer="Private Equity GPs, M&A Sponsors, Venture Growth Funds",
        value_proposition="48-Hour Technical Diligence, Codebase Haircut Math, EBITDA Valuation",
        url="https://github.com/AAH20/ma-vdr-diligence-os",
        blended_cac=4500.0,
        annual_arpu=120000.0,
        net_ltv=600000.0,
        illustrative_cac_ltv_scenario="1:120 to 1:430",
    ),
    "sovereign_rails": CommercialHub(
        hub_id="sovereign_rails",
        name="Sovereign Rails Corp (ISO 20022 & Multi-Rail Settlement)",
        target_buyer="Tier-1 Payment Processors, Neo-banks, Cross-Border Remitters",
        value_proposition="PCI DSS 4.0 Isolation, Sub-Cent Multi-Rail Arbitrage, PvP Clearing",
        url="https://github.com/AAH20/agentic-fintech-kernel",
        blended_cac=8500.0,
        annual_arpu=180000.0,
        net_ltv=900000.0,
        illustrative_cac_ltv_scenario="1:23 to 1:92",
    ),
    "computer_use": CommercialHub(
        hub_id="computer_use",
        name="ComputerUse Corp (Kernel-Level Remote Desktop & Agent OS)",
        target_buyer="AI Agent Scale-ups, Enterprise RPA Architects, Anthropic Ecosystem",
        value_proposition="Sub-500ms Ephemeral Sandbox, Atomic Rollbacks, Zero-CDP Fleet",
        url="https://github.com/AAH20/ghost-desktop",
        blended_cac=1800.0,
        annual_arpu=36000.0,
        net_ltv=144000.0,
        illustrative_cac_ltv_scenario="1:27 to 1:95",
    ),
}


class InventoryParser:
    """Parses and organizes holding company repository datasets."""

    def __init__(self, inventory_path: Optional[str] = None):
        self.inventory_path = inventory_path or self._find_default_path()

    def _find_default_path(self) -> str:
        """Finds repository_inventory.json in common local workspace paths."""
        candidates = [
            "/Users/ahmedhassan/Downloads/Global_HoldingCompany_Architectures/repository_inventory.json",
            "../Global_HoldingCompany_Architectures/repository_inventory.json",
            "repository_inventory.json",
        ]
        for p in candidates:
            if os.path.exists(p):
                return p
        return ""

    def load_inventory(self) -> List[RepositoryItem]:
        """Loads and resolves repositories into structured models."""
        if not self.inventory_path or not os.path.exists(self.inventory_path):
            return self._generate_fallback_portfolio()

        try:
            with open(self.inventory_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (PermissionError, OSError):
            return self._generate_fallback_portfolio()

        raw_repos = data.get("repositories", [])
        items: List[RepositoryItem] = []

        for r in raw_repos:
            full_name = r.get("full_name", "")
            name = full_name.split("/")[-1] if "/" in full_name else full_name
            inv_class = r.get("inventory_class", "original")
            vis = r.get("visibility", "public")
            desc = r.get("description") or ""
            stars = int(r.get("stars", 0))
            forks = int(r.get("forks_count", 0))
            issues = int(r.get("open_issues_count", 0))
            lang = r.get("language")
            cluster = r.get("cockpit_cluster")
            url = r.get("url") or f"https://github.com/{full_name}"
            is_feat = bool(r.get("featured_in_private_cockpit", False))

            pillar = self._classify_macro_pillar(name, desc, cluster)
            hub = self._assign_commercial_hub(pillar, name, desc)

            items.append(RepositoryItem(
                full_name=full_name,
                name=name,
                inventory_class=inv_class,
                visibility=vis,
                description=desc,
                stars=stars,
                forks=forks,
                open_issues=issues,
                language=lang,
                cockpit_cluster=cluster,
                macro_pillar=pillar,
                target_commercial_hub=hub,
                featured_in_cockpit=is_feat,
                url=url,
            ))

        return items

    def _classify_macro_pillar(self, name: str, desc: str, cluster: Optional[str]) -> MacroPillar:
        """Maps repository metadata to one of the 6 Macro Pillars."""
        n = name.lower()
        d = desc.lower()

        # 1. NP-Hard & Microsecond Systems
        if any(k in n for k in ["np-hard", "microsecond", "solver", "hft", "simplex", "geospatial", "datacenter", "leo-satellite", "constellation", "3dgs", "salvo"]):
            return MacroPillar.NP_HARD_MICROSECOND

        # 2. Sovereign FinTech & Multi-Rail
        if cluster == "fintech" or any(k in n for k in ["fintech", "rails", "iso20022", "pvp", "cfpb", "fdx", "nacha", "durbin", "stablecoin", "settlement", "baas"]):
            return MacroPillar.SOVEREIGN_FINTECH_RAILS

        # 3. Cloud GRC, SOC & Enterprise
        if cluster == "grc" or any(k in n for k in ["grc", "soc", "a2z", "diligence", "vdr", "audit", "ciso", "balance-sheet", "compliance"]):
            return MacroPillar.CLOUD_GRC_SOC

        # 4. Dual-Use Defense & Space
        if any(k in n for k in ["defense", "isr", "orbital", "airgap", "kill-chain", "kinetic", "tactical", "sovereignty", "drone"]):
            return MacroPillar.DUAL_USE_DEFENSE_SPACE

        # 5. Computer Use & Desktops
        if cluster == "computer-use" or any(k in n for k in ["ghost", "phantom", "desktop", "webrtc", "computer-use", "gui"]):
            return MacroPillar.DECISION_SCIENCE_COMMERCE

        # 6. Default to Frontier AI, Swarms & MCP
        return MacroPillar.FRONTIER_AI_SWARMS_MCP

    def _assign_commercial_hub(self, pillar: MacroPillar, name: str, desc: str) -> str:
        """Assigns the primary commercial conversion hub for each repo."""
        if pillar == MacroPillar.CLOUD_GRC_SOC:
            if "diligence" in name or "vdr" in name or "balance" in name:
                return "investor_os"
            return "a2zsoc"
        elif pillar == MacroPillar.SOVEREIGN_FINTECH_RAILS:
            return "sovereign_rails"
        elif pillar == MacroPillar.DECISION_SCIENCE_COMMERCE:
            return "computer_use"
        elif pillar == MacroPillar.NP_HARD_MICROSECOND:
            return "investor_os"
        else:
            return "a2zsoc"

    def _generate_fallback_portfolio(self) -> List[RepositoryItem]:
        """Synthetic portfolio fallback if JSON is not present."""
        sample_names = [
            ("apex-industrial-solver", MacroPillar.NP_HARD_MICROSECOND, "investor_os"),
            ("apex-token-slasher", MacroPillar.FRONTIER_AI_SWARMS_MCP, "computer_use"),
            ("apex-zero-loop", MacroPillar.FRONTIER_AI_SWARMS_MCP, "a2zsoc"),
            ("apex-audience-engine", MacroPillar.FRONTIER_AI_SWARMS_MCP, "a2zsoc"),
            ("a2zsoc-core", MacroPillar.CLOUD_GRC_SOC, "a2zsoc"),
            ("agentic-fintech-kernel", MacroPillar.SOVEREIGN_FINTECH_RAILS, "sovereign_rails"),
            ("ghost-desktop", MacroPillar.DECISION_SCIENCE_COMMERCE, "computer_use"),
            ("airgap-audit-breaker", MacroPillar.DUAL_USE_DEFENSE_SPACE, "a2zsoc"),
        ]
        return [
            RepositoryItem(
                full_name=f"AAH20/{name}",
                name=name,
                inventory_class="original",
                visibility="public",
                description=f"Core holding company module: {name}",
                stars=10,
                forks=2,
                open_issues=0,
                macro_pillar=pillar,
                target_commercial_hub=hub,
                featured_in_cockpit=True,
                url=f"https://github.com/AAH20/{name}",
            )
            for name, pillar, hub in sample_names
        ]
