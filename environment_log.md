# Environment Verification Log
## Lab Assignment 02 | MRA2026004 | IIIT-A AI Tools for Research

**Date:** 2026-11-14  
**System:** Windows 11, Python 3.14 (CPython)  
**Author:** Sachin Kumar | sachin.k.works@gmail.com

---

## 1. Python Environment

```
Python Version: 3.14.x (CPython)
Platform: Windows-11-AMD64
Git: 2.47.x
```

### 1.1 Core Libraries Used (stdlib only — no pip dependencies required)
This simulation uses Python standard library exclusively for maximum reproducibility:

| Module | Version | Purpose |
|---|---|---|
| `math` | stdlib | sigmoid computation, logarithms |
| `random` | stdlib | Monte Carlo sampling (seed=42) |
| `csv` | stdlib | Results output |
| `os`, `sys` | stdlib | Path management |
| `re` | stdlib | Regex utilities |
| `typing` | stdlib | Type annotations |

> **Note:** The simulation engine (`src/agent_simulator.py`) deliberately uses only the Python standard library to guarantee zero-dependency reproducibility. No pip install is required.

---

## 2. Experiment Verification

### 2.1 Reproduce the Results

```bash
python scripts/run_experiments.py
```

**Expected console output (first 5 lines):**
```
Executing experimental sweeps: 8 chain lengths x 3 control modes...
Trials per configuration: 1000 (Total trajectories: 24000)

Length  5 | Mode: none      | Success:  75.7% | Irrev. Errors: 0.100 | Interventions: 0.00
Length  5 | Mode: fixed_5   | Success:  95.2% | Irrev. Errors: 0.082 | Interventions: 1.00
```

### 2.2 Verification Checksums

| Configuration | Expected Success Rate | Expected Irrev. Errors |
|---|---|---|
| n=5, none | 75.7% | 0.100 |
| n=20, none | 38.1% | 0.714 |
| n=50, none | 8.5% | 2.816 |
| n=50, fixed_5 | 95.5% | 0.820 |
| n=50, adaptive | 79.0% | 0.466 |

### 2.3 Output File Verification

After running, `results/trajectory_metrics.csv` should have:
- **25 data rows** (8 chain lengths × 3 modes, minus 1 = header + 24 data rows)
- **7 columns**: chain_length, mode, trials, task_success_rate, divergence_rate, avg_irreversible_errors, avg_human_interventions

---

## 3. LaTeX Paper Environment

### 3.1 Compile with Overleaf (Recommended)
1. Upload `paper/main.tex` and `paper/references.bib` to [overleaf.com](https://overleaf.com)
2. Compiler: **pdfLaTeX**
3. Click Compile — paper renders in ~15 seconds

### 3.2 Local Compilation (requires TeX Live / MiKTeX)

```bash
cd paper/
pdflatex main.tex   # Pass 1 (generates .aux)
bibtex main         # Processes references.bib
pdflatex main.tex   # Pass 2 (resolves citations)
pdflatex main.tex   # Pass 3 (stable cross-refs)
```

### 3.3 Required LaTeX Packages

| Package | Purpose |
|---|---|
| `IEEEtran` | IEEE conference format |
| `amsmath`, `amssymb` | Mathematical equations |
| `tikz` + `usetikzlibrary` | TikZ diagrams |
| `booktabs` | Professional table rules |
| `multirow` | Multi-row table cells |
| `cite`, `url` | Reference handling |
| `microtype` | Typographic optimization |

All packages are included in standard TeX Live / MiKTeX installations.

---

## 4. AI Tools Used in This Research

| Tool | Version / Access | Purpose |
|---|---|---|
| Antigravity (Gemini) | Web UI, Nov 2026 | Literature synthesis, formalization, paper writing |
| Antigravity (Claude Sonnet) | Web UI, Nov 2026 | Critical analysis, proof-reading, finalization |
| Semantic Scholar | Web API | Literature discovery |
| ResearchRabbit | Web UI | Citation graph exploration |
| Elicit | Web UI | Research question formulation |
| Litmaps | Web UI | Temporal literature mapping |

---

## 5. Reproducibility Statement

All experimental results in this paper are **fully reproducible** using only:
1. Python 3.x (any version ≥ 3.9) with no additional packages
2. `python scripts/run_experiments.py` (runtime: ~2 seconds)

The random seed is fixed at `seed=42` throughout. Cross-platform reproducibility is guaranteed because the standard library `random` module uses the same Mersenne Twister PRNG across all Python implementations.

---

*Environment log generated: 2026-11-14T22:00:00+05:30*
