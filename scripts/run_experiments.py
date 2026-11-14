"""
Main Experiment Runner for Chained Agent Failure Modes
Executes comparative evaluation across trajectory lengths (5 to 50)
Outputs CSV logs and evaluation summaries.
"""

import os
import sys
import csv

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.agent_simulator import evaluate_batch


def run_all_experiments():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "trajectory_metrics.csv")

    lengths = [5, 10, 15, 20, 25, 30, 40, 50]
    modes = ["none", "fixed_5", "adaptive"]
    trials_per_setting = 1000

    fieldnames = [
        "chain_length",
        "mode",
        "trials",
        "task_success_rate",
        "divergence_rate",
        "avg_irreversible_errors",
        "avg_human_interventions"
    ]

    all_results = []
    print(f"Executing experimental sweeps: {len(lengths)} chain lengths x {len(modes)} control modes...")
    print(f"Trials per configuration: {trials_per_setting} (Total trajectories: {len(lengths)*len(modes)*trials_per_setting})\n")

    for n in lengths:
        for mode in modes:
            res = evaluate_batch(
                num_trials=trials_per_setting,
                chain_length=n,
                checkpoint_mode=mode,
                seed=42 + n
            )
            all_results.append(res)
            print(f"Length {n:2d} | Mode: {mode:9s} | Success: {res['task_success_rate']*100:5.1f}% | Irrev. Errors: {res['avg_irreversible_errors']:.3f} | Interventions: {res['avg_human_interventions']:.2f}")

    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_results:
            writer.writerow(r)

    print(f"\n[SUCCESS] Experimental metrics successfully recorded to {csv_path}")


if __name__ == "__main__":
    run_all_experiments()
