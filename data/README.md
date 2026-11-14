# Data Directory

## Overview

This directory contains input data for the research project. The primary simulation in this paper is **self-contained** — it generates its own synthetic trajectory data via the Monte Carlo engine in `src/agent_simulator.py`.

## Synthetic Simulation Data

The experiment (`scripts/run_experiments.py`) generates structured synthetic data modeling:

- **Agent trajectory execution** over chain lengths n ∈ {5, 10, 15, 20, 25, 30, 40, 50}
- **Per-step tool attributes** sampled from calibrated distributions:
  - `is_irreversible`: Bernoulli(p=0.20) — 20% of tools are destructive/irreversible
  - `privilege`: Uniform(0.3, 0.9) for irreversible tools; Uniform(0.1, 0.4) for safe tools
  - `uncertainty`: Uniform(0.05, 0.35) in valid state; Uniform(0.40, 0.85) post-divergence
  - `consequence`: Uniform(0.5, 0.95) for irreversible; Uniform(0.05, 0.3) for safe tools

## Output Schema

Generated output is stored in `results/trajectory_metrics.csv`:

| Column | Type | Description |
|---|---|---|
| `chain_length` | int | Number of tool-call steps in trajectory (n) |
| `mode` | str | Control mode: `none`, `fixed_5`, or `adaptive` |
| `trials` | int | Number of Monte Carlo trials (always 1000) |
| `task_success_rate` | float | Fraction of trials where state remained valid at end |
| `divergence_rate` | float | Fraction of trials where trajectory diverged at any point |
| `avg_irreversible_errors` | float | Mean irreversible tool errors per trajectory |
| `avg_human_interventions` | float | Mean human checkpoint triggers per trajectory |

## Reproducibility

All data is **fully reproducible** with `seed=42`. Run:
```bash
python scripts/run_experiments.py
```

No external datasets, model weights, or API keys are required.
