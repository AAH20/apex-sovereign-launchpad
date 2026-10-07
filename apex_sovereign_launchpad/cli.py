"""Unified Command Line Interface for Apex Sovereign Launchpad.

Governs portfolio GTM orchestration, backlink mesh engineering,
spin-out hurdle audits, and thematic launch generation for Apex Growth Systems LLC.
Pure Python standard library: zero external dependencies.
"""

from __future__ import annotations

import argparse
import sys
from apex_sovereign_launchpad.core.anti_slop_filter import AntiSlopFilter
from apex_sovereign_launchpad.core.backlink_mesh import BacklinkMeshGenerator
from apex_sovereign_launchpad.core.cockpit_generator import CockpitGenerator
from apex_sovereign_launchpad.core.hurdle_evaluator import HurdleEvaluator
from apex_sovereign_launchpad.core.inventory_parser import COMMERCIAL_HUBS, InventoryParser
from apex_sovereign_launchpad.core.models import MacroPillar
from apex_sovereign_launchpad.core.super_launcher import SuperLauncher


def main():
    parser = argparse.ArgumentParser(
        prog="apex-launchpad",
        description="Apex Sovereign Launchpad: GTM, Backlink Mesh & Hurdle Control Plane for Apex Growth Systems LLC",
    )
    subparsers = parser.add_subparsers(dest="command", help="Portfolio GTM sub-commands")

    # inventory
    subparsers.add_parser("inventory", help="Inspect holding company repository inventory across the 6 Macro Pillars")

    # mesh
    p_mesh = subparsers.add_parser("mesh", help="Generate cross-repo backlink mesh and referral anchors")
    p_mesh.add_argument("--preview", type=str, default="", help="Repo name to preview backlink snippet for")

    # launch-wave
    p_wave = subparsers.add_parser("launch-wave", help="Synthesize a Thematic Super-Launch campaign (Waves 1 to 6)")
    p_wave.add_argument("--wave", type=int, choices=[1, 2, 3, 4, 5, 6], default=1, help="Wave number (1-6)")

    # hurdle-audit
    subparsers.add_parser("hurdle-audit", help="Audit the 4 Commercial Hubs against the Sovereign Spin-Out Hurdle Gates")

    # export-cockpit
    p_cockpit = subparsers.add_parser("export-cockpit", help="Export self-contained HTML portfolio cockpit")
    p_cockpit.add_argument("--out", type=str, default="portfolio_cockpit.html", help="Output file path")

    # verify-slop
    p_slop = subparsers.add_parser("verify-slop", help="Audit copy for Propositional Information Density (PID >= 0.35)")
    p_slop.add_argument("--text", type=str, required=True, help="Text string or markdown snippet to audit")

    # benchmark
    subparsers.add_parser("benchmark", help="Execute microsecond benchmark telemetry suite")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    parser_engine = InventoryParser()
    repos = parser_engine.load_inventory()

    if args.command == "inventory":
        original_repos = [r for r in repos if r.inventory_class == "original"]
        print("\n================================================================================")
        print("          APEX GROWTH SYSTEMS LLC — REPOSITORY PORTFOLIO INVENTORY             ")
        print("================================================================================\n")
        print(f"Total Repositories Ingested:    {len(repos)}")
        print(f"Original Repositories:          {len(original_repos)}")
        print(f"Forks:                          {len(repos) - len(original_repos)}")
        print(f"Total Portfolio Star Count:     {sum(r.stars for r in original_repos):,}\n")

        print("Macro Pillar Distribution (Original Repositories):")
        pillar_counts = {}
        for r in original_repos:
            pillar_counts[r.macro_pillar.value] = pillar_counts.get(r.macro_pillar.value, 0) + 1

        for p_name, count in sorted(pillar_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {p_name:<46}: {count:>3} repos")
        print()

    elif args.command == "mesh":
        mesh_gen = BacklinkMeshGenerator()
        blocks, res = mesh_gen.build_full_mesh(repos)
        print("\n[Apex-Launchpad] Automated Backlink Mesh Generated:")
        print(f"Original Repositories Meshed:        {res.original_repositories_meshed}")
        print(f"Cross-Referral Sibling Edges:        {res.cross_referral_edges_generated}")
        print(f"Commercial Hub Referrals Injected:   {res.commercial_hub_referrals_injected}")
        print(f"Execution Latency:                   {res.elapsed_microseconds:.2f} µs\n")

        preview_target = args.preview or "apex-industrial-solver"
        if preview_target in blocks:
            print(f"--- Sample Backlink Preview for `{preview_target}` ---")
            print(blocks[preview_target])
            print("------------------------------------------------------\n")

    elif args.command == "launch-wave":
        pillar_mapping = {
            1: MacroPillar.NP_HARD_MICROSECOND,
            2: MacroPillar.SOVEREIGN_FINTECH_RAILS,
            3: MacroPillar.CLOUD_GRC_SOC,
            4: MacroPillar.DECISION_SCIENCE_COMMERCE,
            5: MacroPillar.DUAL_USE_DEFENSE_SPACE,
            6: MacroPillar.FRONTIER_AI_SWARMS_MCP,
        }
        target_pillar = pillar_mapping[args.wave]
        target_repos = [r for r in repos if r.macro_pillar == target_pillar]

        launcher = SuperLauncher()
        manifest = launcher.generate_manifest(args.wave, target_pillar, target_repos)

        print(f"\n================================================================================")
        print(f"        THEMATIC SUPER-LAUNCH MANIFEST: WAVE {args.wave}                        ")
        print(f"================================================================================\n")
        print(f"Macro Pillar:              {manifest.macro_pillar.value}")
        print(f"Target Commercial Hub:     {manifest.target_hub_id}")
        print(f"Featured Repositories:     {', '.join(manifest.featured_repositories)}")
        print(f"Propositional Density:     PID = {manifest.anti_slop_metrics.propositional_information_density * 100:.1f}%")
        print(f"Anti-Slop Status:          {'PASS (High-Signal Technical)' if manifest.anti_slop_metrics.is_valid_technical_copy else 'FAIL'}")
        print(f"\n--- Show HN Title ---\n{manifest.show_hn_title}\n")
        print(f"--- Executive Abstract ---\n{manifest.executive_abstract}\n")
        print("--- X/Twitter Launch Thread ---")
        for b in manifest.x_thread_bullets:
            print(f"{b}\n")

    elif args.command == "hurdle-audit":
        evaluator = HurdleEvaluator()
        print("\n================================================================================")
        print("      APEX GROWTH SYSTEMS LLC — SOVEREIGN SPIN-OUT HURDLE AUDIT                 ")
        print("================================================================================\n")
        for hub_id, hub in COMMERCIAL_HUBS.items():
            current_arr = 75000.0 if hub_id == "a2zsoc" else 0.0
            ev = evaluator.evaluate_hub(hub, current_arr=current_arr)
            print(f"🏛️  {hub.name}")
            print(f"    • Gate 1 (CAC:LTV >= 1:4):      {'PASSED' if ev.gate1_passed else 'FAILED'} (Scenario: 1:{ev.gate1_cac_ltv_ratio:.1f})")
            print(f"    • Gate 2 (ARR > $250k):         {'PASSED' if ev.gate2_passed else 'PENDING'} (${ev.gate2_arr_baseline:,.0f} / $250,000)")
            print(f"    • Gate 3 (Liability Ringfence): {'REQUIRED & SECURED' if ev.gate3_passed else 'NOT REQUIRED'}")
            print(f"    • Gate 4 (Strategic Trigger):   {'ACTIVE' if ev.gate4_passed else 'NONE'}")
            print(f"    • Status Verdict:               [{ev.recommendation}]")
            print(f"    • Justification:                {ev.justification}\n")

    elif args.command == "export-cockpit":
        cockpit_gen = CockpitGenerator()
        html_content = cockpit_gen.generate_html(repos)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n[Apex-Launchpad] Exported interactive portfolio cockpit to: {args.out} ({len(html_content):,} bytes)\n")

    elif args.command == "verify-slop":
        flt = AntiSlopFilter()
        metrics = flt.audit_text(args.text)
        print(f"\nPropositional Information Density (PID): {metrics.propositional_information_density * 100:.1f}%")
        print(f"Shannon Entropy (Sentence Rhythm):       {metrics.shannon_entropy}")
        print(f"Slop Words Found:                        {metrics.slop_token_count}")
        print(f"Valid Technical Copy:                    {metrics.is_valid_technical_copy}")
        if metrics.rejected_reasons:
            print(f"Rejection Reasons:                       {', '.join(metrics.rejected_reasons)}")
        print()

    elif args.command == "benchmark":
        from benchmarks.benchmark_telemetry import run_benchmarks
        run_benchmarks()


if __name__ == "__main__":
    main()
