"""Interactive Holding Company Portfolio Cockpit Generator.

Renders self-contained, high-performance HTML/JS directories and Markdown dossiers
for all 370+ repositories and 4 Commercial Hubs under Apex Growth Systems LLC.
Zero external dependencies: 100% pure Python standard library.
"""

from __future__ import annotations

import json
from typing import Dict, List
from apex_sovereign_launchpad.core.inventory_parser import COMMERCIAL_HUBS
from apex_sovereign_launchpad.core.models import (
    MacroPillar,
    RepositoryItem,
)


class CockpitGenerator:
    """Generates visual and markdown directory cockpits for the holding company."""

    def generate_html(self, repos: List[RepositoryItem]) -> str:
        """Generates self-contained Single Page Application (SPA) dashboard."""
        original_repos = [r for r in repos if r.inventory_class == "original"]
        total_stars = sum(r.stars for r in original_repos)

        # Build repository JSON payload for client-side search/filter
        repo_data = [
            {
                "name": r.name,
                "pillar": r.macro_pillar.value,
                "desc": r.description,
                "stars": r.stars,
                "url": r.url,
                "hub": r.target_commercial_hub,
            }
            for r in original_repos
        ]
        json_payload = json.dumps(repo_data)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Apex Growth Systems LLC — Sovereign Portfolio Cockpit</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #111827;
      --card-border: #1f2937;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --accent: #3b82f6;
      --accent-glow: rgba(59, 130, 246, 0.2);
      --green: #10b981;
      --purple: #8b5cf6;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }}
    body {{ background: var(--bg); color: var(--text); padding: 2rem; line-height: 1.5; }}
    header {{ max-width: 1200px; margin: 0 auto 2rem auto; border-bottom: 1px solid var(--card-border); padding-bottom: 1.5rem; }}
    .badge {{ display: inline-block; background: var(--accent-glow); color: var(--accent); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 0.75rem; border: 1px solid var(--accent); }}
    h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.025em; }}
    p.sub {{ color: var(--text-muted); font-size: 1rem; }}
    
    .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; max-width: 1200px; margin: 0 auto 2rem auto; }}
    .kpi-card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 0.5rem; padding: 1.25rem; }}
    .kpi-card .val {{ font-size: 1.75rem; font-weight: 700; color: var(--text); margin-top: 0.25rem; }}
    .kpi-card .lbl {{ font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }}

    .hubs-section {{ max-width: 1200px; margin: 0 auto 2.5rem auto; }}
    .hubs-section h2 {{ font-size: 1.25rem; margin-bottom: 1rem; color: var(--text); display: flex; align-items: center; gap: 0.5rem; }}
    .hubs-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 1rem; }}
    .hub-card {{ background: linear-gradient(180deg, #161f33 0%, #111827 100%); border: 1px solid #2563eb; border-radius: 0.5rem; padding: 1.25rem; }}
    .hub-card h3 {{ font-size: 1.1rem; color: var(--accent); margin-bottom: 0.25rem; }}
    .hub-card p {{ font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem; }}
    .hub-card .eco {{ font-size: 0.75rem; background: rgba(16, 185, 129, 0.1); color: var(--green); padding: 0.35rem 0.5rem; border-radius: 0.25rem; display: inline-block; }}

    .controls {{ max-width: 1200px; margin: 0 auto 1.5rem auto; display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; }}
    #search {{ flex: 1; min-width: 260px; background: var(--card-bg); border: 1px solid var(--card-border); color: var(--text); padding: 0.6rem 1rem; border-radius: 0.375rem; font-size: 0.9rem; }}
    .pill-btn {{ background: var(--card-bg); border: 1px solid var(--card-border); color: var(--text-muted); padding: 0.5rem 0.85rem; border-radius: 0.375rem; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; }}
    .pill-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}

    .repo-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 1rem; max-width: 1200px; margin: 0 auto; }}
    .repo-card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 0.5rem; padding: 1.25rem; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.15s ease, border-color 0.15s ease; }}
    .repo-card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}
    .repo-card .title {{ font-size: 1rem; font-weight: 600; color: var(--text); text-decoration: none; word-break: break-all; }}
    .repo-card .title:hover {{ color: var(--accent); }}
    .repo-card .p-tag {{ font-size: 0.7rem; color: var(--purple); font-weight: 600; text-transform: uppercase; margin-top: 0.25rem; }}
    .repo-card .desc {{ font-size: 0.85rem; color: var(--text-muted); margin: 0.75rem 0; flex-grow: 1; }}
    .repo-card .meta {{ display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: var(--text-muted); border-top: 1px solid var(--card-border); padding-top: 0.75rem; }}
  </style>
</head>
<body>

  <header>
    <div class="badge">Master Sovereign Portfolio</div>
    <h1>Apex Growth Systems LLC</h1>
    <p class="sub">370+ Sovereign Deep-Tech Kernels across 6 Macro Pillars • Zero Premature Dilution • Master IP Vault</p>
  </header>

  <div class="kpi-grid">
    <div class="kpi-card"><div class="lbl">Original Repositories</div><div class="val">{len(original_repos)}</div></div>
    <div class="kpi-card"><div class="lbl">Total Star Volume</div><div class="val">{total_stars:,}</div></div>
    <div class="kpi-card"><div class="lbl">Macro Pillars</div><div class="val">6</div></div>
    <div class="kpi-card"><div class="lbl">Commercial Hubs</div><div class="val">4</div></div>
  </div>

  <section class="hubs-section">
    <h2>🏛️ Commercial Operating Hubs (Candidate Subsidiaries)</h2>
    <div class="hubs-grid">
      <div class="hub-card">
        <h3>a2zsoc Corp</h3>
        <p>Enterprise GRC, Agentic vCISO & Continuous Evidence Harvester (1,100+ Controls).</p>
        <div class="eco">CAC:LTV = 1:37 to 1:140</div>
      </div>
      <div class="hub-card">
        <h3>InvestorOS LLC</h3>
        <p>Algorithmic Technical M&A Diligence & EBITDA Codebase Haircut Valuation.</p>
        <div class="eco">CAC:LTV = 1:120 to 1:430</div>
      </div>
      <div class="hub-card">
        <h3>Sovereign Rails Corp</h3>
        <p>ISO 20022 Engine, PCI DSS 4.0 Isolation & Real-Time PvP Multi-Rail Settlement.</p>
        <div class="eco">CAC:LTV = 1:23 to 1:92</div>
      </div>
      <div class="hub-card">
        <h3>ComputerUse Corp</h3>
        <p>Phantom-V8, Ghost-Desktop & WebRTC Canvas for Sub-500ms Ephemeral Sandboxes.</p>
        <div class="eco">CAC:LTV = 1:27 to 1:95</div>
      </div>
    </div>
  </section>

  <div class="controls">
    <input type="text" id="search" placeholder="Search 370+ repositories by name, keyword, or algorithm...">
    <button class="pill-btn active" onclick="filterPillar('ALL')">All Pillars</button>
    <button class="pill-btn" onclick="filterPillar('NP-Hard & Microsecond Systems')">NP-Hard</button>
    <button class="pill-btn" onclick="filterPillar('Frontier AI, Swarms & MCP Ecosystem')">Swarms/MCP</button>
    <button class="pill-btn" onclick="filterPillar('Sovereign FinTech, Banking & Treasury Rails')">FinTech</button>
    <button class="pill-btn" onclick="filterPillar('Cloud GRC, SOC & Enterprise Infrastructure')">GRC/SOC</button>
    <button class="pill-btn" onclick="filterPillar('Dual-Use Defense, Electronic Warfare & Space')">Defense/Space</button>
  </div>

  <div id="grid" class="repo-grid"></div>

  <script>
    const repos = {json_payload};
    let activePillar = 'ALL';
    let query = '';

    function render() {{
      const grid = document.getElementById('grid');
      grid.innerHTML = '';
      const filtered = repos.filter(r => {{
        const matchPillar = (activePillar === 'ALL') || (r.pillar === activePillar);
        const matchQuery = !query || r.name.toLowerCase().includes(query) || (r.desc && r.desc.toLowerCase().includes(query));
        return matchPillar && matchQuery;
      }});

      filtered.forEach(r => {{
        const card = document.createElement('div');
        card.className = 'repo-card';
        card.innerHTML = `
          <div>
            <a href="${{r.url}}" target="_blank" class="title">${{r.name}}</a>
            <div class="p-tag">${{r.pillar}}</div>
            <div class="desc">${{r.desc || 'Zero-dependency sovereign kernel.'}}</div>
          </div>
          <div class="meta">
            <span>⭐ ${{r.stars}} stars</span>
            <span>Hub: ${{r.hub}}</span>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function filterPillar(p) {{
      activePillar = p;
      document.querySelectorAll('.pill-btn').forEach(b => {{
        b.classList.toggle('active', b.textContent.includes(p) || (p === 'ALL' && b.textContent === 'All Pillars'));
      }});
      render();
    }}

    document.getElementById('search').addEventListener('input', (e) => {{
      query = e.target.value.toLowerCase().trim();
      render();
    }});

    render();
  </script>
</body>
</html>"""
        return html
