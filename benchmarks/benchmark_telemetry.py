"""Microsecond Benchmark Telemetry Suite for Apex Sovereign Launchpad.

Measures throughput and execution latency across inventory ingestion,
backlink mesh generation, hurdle gate evaluation, and cockpit rendering.
Pure Python 3.10+ standard library: zero external dependencies.
"""

from __future__ import annotations

import os
from pathlib import Path
import statistics
import sys
import time
from typing import Callable, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apex_sovereign_launchpad.core.anti_slop_filter import AntiSlopFilter
from apex_sovereign_launchpad.core.backlink_mesh import BacklinkMeshGenerator
from apex_sovereign_launchpad.core.cockpit_generator import CockpitGenerator
from apex_sovereign_launchpad.core.hurdle_evaluator import HurdleEvaluator
from apex_sovereign_launchpad.core.inventory_parser import COMMERCIAL_HUBS, InventoryParser
from apex_sovereign_launchpad.core.models import MacroPillar
from apex_sovereign_launchpad.core.super_launcher import SuperLauncher


def benchmark_call(fn: Callable, runs: int = 25) -> Tuple[float, float, float]:
    """Measures execution latency over multiple runs.
    
    Returns (mean_us, p95_us, ops_per_sec).
    """
    times_us: List[float] = []
    # Warmup
    fn()

    for _ in range(runs):
        t0 = time.perf_counter_ns()
        fn()
        t1 = time.perf_counter_ns()
        times_us.append((t1 - t0) / 1000.0)

    mean_us = statistics.mean(times_us)
    times_us.sort()
    p95_idx = int(0.95 * len(times_us))
    p95_us = times_us[min(p95_idx, len(times_us) - 1)]
    ops_per_sec = 1_000_000.0 / mean_us if mean_us > 0 else 0.0

    return mean_us, p95_us, ops_per_sec


def run_benchmarks():
    parser = InventoryParser()
    repos = parser.load_inventory()
    mesh_gen = BacklinkMeshGenerator()
    launcher = SuperLauncher()
    evaluator = HurdleEvaluator()
    slop_filter = AntiSlopFilter()
    cockpit_gen = CockpitGenerator()

    sample_repo = repos[0]
    sample_text = """
We benchmarked 53 operations research solvers in pure Python.
Latency ranges from 9.67µs (Two-Phase Simplex LP) to 3.05ms (3D Bin Packing).
Solves 103,389 LP problems per second with 0 external dependencies.
Available at https://github.com/AAH20/apex-industrial-solver
"""

    print("================================================================================")
    print("      APEX SOVEREIGN LAUNCHPAD — MICROSECOND BENCHMARK TELEMETRY                ")
    print("================================================================================\n")

    results = []

    # 1. Inventory Classification & Pillar Resolution (554 repos)
    mean_us, p95_us, ops = benchmark_call(lambda: parser.load_inventory(), runs=20)
    results.append(("Inventory Ingestion", f"{len(repos)} Repos Resolved", mean_us, p95_us, ops))

    # 2. Single Repo Backlink Synthesis
    mean_us, p95_us, ops = benchmark_call(
        lambda: mesh_gen.generate_repo_backlink_block(sample_repo, repos[:5]),
        runs=50,
    )
    results.append(("Single Repo Mesh Injection", "Header + Footer + Siblings", mean_us, p95_us, ops))

    # 3. Full Portfolio Backlink Mesh (370+ original repos)
    mean_us, p95_us, ops = benchmark_call(
        lambda: mesh_gen.build_full_mesh(repos),
        runs=20,
    )
    results.append(("Full Portfolio Mesh", f"{len(repos)} Repos (Full Graph)", mean_us, p95_us, ops))

    # 4. Anti-Slop Propositional Density Audit
    mean_us, p95_us, ops = benchmark_call(
        lambda: slop_filter.audit_text(sample_text),
        runs=50,
    )
    results.append(("Anti-Slop PID Audit", "Empirical Density + Entropy", mean_us, p95_us, ops))

    # 5. Thematic Super-Launch Campaign Synthesis
    pillar_repos = [r for r in repos if r.macro_pillar == MacroPillar.NP_HARD_MICROSECOND]
    mean_us, p95_us, ops = benchmark_call(
        lambda: launcher.generate_manifest(1, MacroPillar.NP_HARD_MICROSECOND, pillar_repos),
        runs=30,
    )
    results.append(("Thematic Super-Launcher", "Wave Manifest + X Thread", mean_us, p95_us, ops))

    # 6. Spin-Out Hurdle Rate Gate Evaluation
    hub = COMMERCIAL_HUBS["a2zsoc"]
    mean_us, p95_us, ops = benchmark_call(
        lambda: evaluator.evaluate_hub(hub, current_arr=150000.0, is_strategic=True),
        runs=50,
    )
    results.append(("4-Gate Hurdle Evaluator", "LTV:CAC + ARR + Ringfence", mean_us, p95_us, ops))

    # 7. HTML Cockpit SPA Generation
    mean_us, p95_us, ops = benchmark_call(
        lambda: cockpit_gen.generate_html(repos),
        runs=20,
    )
    results.append(("Cockpit SPA Generator", f"Single-Page HTML ({len(repos)} cards)", mean_us, p95_us, ops))

    # Print Table
    header = f"| {'GTM Engine Kernel':<26} | {'Target Benchmark Payload':<28} | {'Mean Latency (µs)':<18} | {'p95 Latency (µs)':<18} | {'Throughput (ops/s)':<18} |"
    sep = f"|{'-'*28}|{'-'*30}|{'-'*20}|{'-'*20}|{'-'*20}|"
    print(header)
    print(sep)
    for kernel, payload, mean_u, p95_u, ops_s in results:
        print(f"| {kernel:<26} | {payload:<28} | {mean_u:>16.2f} µs | {p95_u:>16.2f} µs | {ops_s:>16.1f} /s |")
    print(sep)


if __name__ == "__main__":
    run_benchmarks()
