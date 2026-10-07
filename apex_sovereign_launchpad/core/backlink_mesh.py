"""Automated Cross-Repository Backlink Mesh Generator.

Generates synchronized institutional headers, sibling cross-pollination links,
and commercial hub conversion funnels across all 370+ repositories under
Apex Growth Systems LLC.
Zero external dependencies: 100% pure Python standard library.
"""

from __future__ import annotations

import time
from typing import Dict, List, Tuple
from apex_sovereign_launchpad.core.inventory_parser import COMMERCIAL_HUBS
from apex_sovereign_launchpad.core.models import (
    BacklinkMeshResult,
    MacroPillar,
    RepositoryItem,
)


class BacklinkMeshGenerator:
    """Generates deterministic reciprocal backlink anchors across the portfolio."""

    def __init__(self):
        pass

    def generate_repo_backlink_block(
        self,
        repo: RepositoryItem,
        sibling_repos: List[RepositoryItem],
    ) -> str:
        """Generates holding company trust header and commercial referral footer for a repo."""
        hub = COMMERCIAL_HUBS.get(repo.target_commercial_hub or "a2zsoc")
        hub_name = hub.name if hub else "a2zsoc"
        hub_url = hub.url if hub else "https://a2zsoc.com"
        hub_val = hub.value_proposition if hub else "Enterprise Governance"

        # Sibling links within same pillar (top 3)
        siblings = [s for s in sibling_repos if s.name != repo.name][:3]
        sibling_links = " • ".join([f"[{s.name}]({s.url})" for s in siblings]) if siblings else "[Portfolio Index](https://github.com/AAH20)"

        header = f"""<!-- APEX_HOLDING_SOVEREIGN_HEADER_START -->
> **🏛️ Apex Growth Systems LLC — Sovereign Deep-Tech Portfolio**  
> **Macro Pillar**: `{repo.macro_pillar.value}` | **Incubation Vehicle**: `Apex Growth Systems LLC`  
> **Enterprise Commercial Hub**: [{hub_name}]({hub_url})  
<!-- APEX_HOLDING_SOVEREIGN_HEADER_END -->
"""

        footer = f"""<!-- APEX_HOLDING_SOVEREIGN_FOOTER_START -->
---

### 🌐 Part of the Sovereign Constellation

This project is incubated within **Apex Growth Systems LLC** alongside 370+ sovereign deep-tech kernels:

* **Pillar Siblings**: {sibling_links}
* **Commercial Upstream**: Need enterprise SLAs, compliance isolation, or custom deployment? Learn about [{hub_name}]({hub_url}) — *{hub_val}*.
* **Founder & IP Governance**: Maintained under the founder-control architecture of **Ahmed Hassan** (Founder & Sole Managing Member, Apex Growth Systems LLC).

*Licensed under MIT with Enterprise Dual-Licensing Available.*
<!-- APEX_HOLDING_SOVEREIGN_FOOTER_END -->
"""
        return f"{header}\n\n{footer}"

    def build_full_mesh(self, repos: List[RepositoryItem]) -> Tuple[Dict[str, str], BacklinkMeshResult]:
        """Builds backlink injections for all original repositories."""
        t_start = time.perf_counter_ns()

        original_repos = [r for r in repos if r.inventory_class == "original"]
        # Group by pillar
        pillar_map: Dict[MacroPillar, List[RepositoryItem]] = {}
        for r in original_repos:
            if r.macro_pillar not in pillar_map:
                pillar_map[r.macro_pillar] = []
            pillar_map[r.macro_pillar].append(r)

        mesh_blocks: Dict[str, str] = {}
        total_edges = 0
        hub_referrals = 0

        for r in original_repos:
            siblings = pillar_map.get(r.macro_pillar, [])
            block = self.generate_repo_backlink_block(r, siblings)
            mesh_blocks[r.name] = block
            total_edges += min(3, max(0, len(siblings) - 1))
            hub_referrals += 1

        elapsed_us = (time.perf_counter_ns() - t_start) / 1000.0

        res = BacklinkMeshResult(
            total_repositories_processed=len(repos),
            original_repositories_meshed=len(original_repos),
            cross_referral_edges_generated=total_edges,
            commercial_hub_referrals_injected=hub_referrals,
            elapsed_microseconds=round(elapsed_us, 2),
        )

        return mesh_blocks, res
