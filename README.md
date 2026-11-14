# Failure Modes in Chained Tool-Calling Agents Operating Without Human Checkpoints

> **IEEE Research Paper | Lab Assignment 02**  
> AI Tools for Research — Indian Institute of Information Technology Allahabad  
> Author: Sachin Kumar | Roll No.: MRA2026004 | M.Tech IT (Robotics & AI)

---

## Abstract

Large language model (LLM) agents increasingly integrate reasoning, multi-step planning, working memory, and external APIs to execute autonomous workflows. In chained tool-calling architectures, the output of one model–tool interaction becomes the direct operational state for subsequent decisions. When human checkpoints are removed, minor reasoning mistakes, schema hallucinations, or corrupted observations propagate, amplify, and solidify into ground truth across subsequent steps — inducing catastrophic trajectory divergence.

This paper establishes a formal six-class taxonomy of failure modes, formalizes chained execution as a Partially Observed Sequential Decision Process (POSDP), and proposes an adaptive risk-sensitive checkpointing architecture. Validated across **24,000 Monte Carlo trajectory simulations**, we demonstrate that unsupervised autonomy collapses to **8.5% task success** at 50-step chains, while adaptive checkpointing stabilizes success at **79%** with **6× fewer irreversible mutations**.

---

## Repository Structure

```
AITR_Lab02_MRA2026004_AgentFailureModes/
│
├── paper/
│   ├── main.tex              ← Complete IEEE-format LaTeX source (549 lines)
│   └── references.bib        ← BibTeX — 22 peer-reviewed references (2023–2026)
│
├── src/
│   └── agent_simulator.py    ← POSDP trajectory simulation engine + risk scoring
│
├── scripts/
│   └── run_experiments.py    ← Experiment runner (8 chain lengths × 3 control modes)
│
├── configs/
│   └── experiment_config.yaml ← Hyperparameter configuration
│
├── results/
│   └── trajectory_metrics.csv ← Raw simulation output (24,000 trials, 25 rows × 7 cols)
│
├── notebooks/
│   └── analysis.ipynb        ← Exploratory data analysis and figure generation
│
├── data/
│   └── README.md             ← Data provenance and format documentation
│
├── prompts/
│   └── prompt_workbook.md    ← All 13+ AI prompts used in this research workflow
│
├── environment.txt           ← Python dependency manifest (pip freeze equivalent)
├── environment_log.md        ← Environment setup verification log
├── README.md                 ← This file
└── .gitignore
```

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sachin-iiita/AITR_Lab02_MRA2026004_AgentFailureModes.git
cd AITR_Lab02_MRA2026004_AgentFailureModes
```

### 2. Run the Simulation Experiment

```bash
python scripts/run_experiments.py
```

**Expected output** in `results/trajectory_metrics.csv` — 24,000 simulated trajectories across:
- **8 chain lengths**: n ∈ {5, 10, 15, 20, 25, 30, 40, 50}
- **3 control modes**: Unsupervised | Fixed-5 Checkpointing | Adaptive Risk-Sensitive

### 3. Compile the IEEE Paper

Upload `paper/main.tex` and `paper/references.bib` to [Overleaf.com](https://overleaf.com), or locally:

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex   # 3rd pass for stable cross-references
```

---

## Key Results

| Chain Length | Unsupervised | Fixed-5 | **Adaptive (Proposed)** |
|:---:|:---:|:---:|:---:|
| n = 5  | 75.7% | 95.2% | **83.5%** |
| n = 10 | 63.2% | 95.1% | **82.8%** |
| n = 20 | 38.1% | 95.0% | **81.3%** |
| n = 30 | 19.6% | 94.6% | **77.6%** |
| n = 50 | **8.5%** | 95.5% | **79.0%** |

Adaptive checkpointing reduces irreversible errors by **83.5%** at n=50 compared to unsupervised execution, using **10% fewer human interventions** than rigid Fixed-5 schemes.

---

## Six-Class Failure Taxonomy

| Class | Failure Domain | Key Failure Modes |
|---|---|---|
| 1 | Planning & Decomposition | Goal misinterpretation, plan drift, premature commitment |
| 2 | Tool Selection & Arguments | Argument hallucination, schema mismatch, over-privilege |
| 3 | State, Memory & Context | Desynchronization, context dilution, memory contamination |
| 4 | Execution & Environment | Partial execution, transient timeouts, stale results |
| 5 | Verification & Recovery | Verification ceiling, false verification, error masking |
| 6 | Security & Governance | Indirect prompt injection, confused deputy, policy bypass |

---

## Formal Framework

The chained agent is modeled as a **POSDP** ⟨𝒮, 𝒜, 𝒪, 𝒯, Ω, π_θ, g⟩:

```
s_t  →[π_θ(h_t, g)]→  a_t  →[𝒯]→  s_{t+1}  →[Ω]→  o_{t+1}  → h_{t+1}
```

**Adaptive risk score** (Eq. 6 in paper):
```
R_t = σ(α·U(a_t|h_t) + β·I(a_t) + γ·P(a_t) + δ·C(a_t, s_t))
```

Where U = uncertainty, I = irreversibility, P = privilege level, C = downstream consequence.

---

## References (22 Works, 2023–2026)

Key citations include: Toolformer (NeurIPS'23), ReAct (ICLR'23), ToolLLM (ICLR'24), AgentBench (ICLR'24), WebArena (ICLR'24), AgentDojo (NeurIPS'24), τ-bench (ICLR'25), SafeToolBench (EMNLP'25), AgentHarm (ICLR'25), Agent Security Bench (ICLR'25), Verifiably Safe Tool Use (ICSE'26).

---

## License

This work is submitted as an academic assignment. Code is released for educational and research purposes.

---

*Generated and verified using AI Tools for Research methodology, IIIT-A, November 2026.*
