# Prompt Workbook — Lab Assignment 02
## AI Tools for Research | IIIT Allahabad | MRA2026004

This workbook documents all AI prompts used during the research workflow for the paper:
**"Failure Modes in Chained Tool-Calling Agents Operating Without Human Checkpoints"**

Each prompt is recorded with its phase, purpose, the tool used, and the actual output summary.

---

## PHASE I — Literature Discovery & Synthesis

### PROMPT 1 | Identify the research gap

**Tool used:** Semantic Scholar / Elicit / AI assistant  
**Prompt:**
```
I am studying LLM-based autonomous agents that chain multiple tool calls without human
checkpoints. What are the key failure modes and open research gaps in this area?
Focus on papers from 2023–2026 spanning tool-augmented agents, agent benchmarks,
agent security, and self-correction mechanisms.
```
**Output summary:** Identified 6 key research gaps — (1) no formal taxonomy of chained failure modes, (2) benchmark metrics don't capture trajectory-level safety, (3) self-correction is bounded by verification ceiling, (4) indirect prompt injection as an underexplored attack vector in chained agents, (5) irreversibility is not modeled in current evaluation frameworks, (6) no principled replacement for human checkpoints.

---

### PROMPT 2 | Seed paper search

**Tool used:** Semantic Scholar / ResearchRabbit  
**Prompt:**
```
Find the most cited and most recent papers (2023–2026) on:
1. Tool-augmented LLM agents (Toolformer, ReAct, ToolLLM style)
2. Long-horizon agent benchmarks (WebArena, AgentBench, tau-bench)
3. Agent self-correction (Reflexion, Self-Refine, Voyager)
4. Agent security / prompt injection (AgentDojo, AgentHarm, ASB)
5. Prospective tool safety (SafeToolBench, verifiable tool use)
Return full citation details including venue, year, DOI/arXiv ID.
```
**Output summary:** Retrieved 22 foundational papers forming the core reference corpus. Notable additions: `doshi2026towards` (ICSE 2026) on verifiable tool use; `chen2025acebench` (EMNLP 2025) on operational evaluation; `chowa2026from` (AI Review 2026) comprehensive survey.

---

### PROMPT 3 | Thematic synthesis across papers

**Tool used:** AI assistant (comparative analysis)  
**Prompt:**
```
Given these 22 papers on LLM agents, synthesize the common failure themes across:
- Benchmark papers (WebArena, AgentBench, tau-bench, Mind2Web)
- Security papers (AgentDojo, AgentHarm, ASB, Agent-SafetyBench)
- Self-correction papers (Reflexion, Self-Refine, Voyager)
- Tool fine-tuning papers (Toolformer, ToolLLM)
Identify what failure categories emerge across all groups and what each group
uniquely reveals about autonomous agent reliability.
```
**Output summary:** Synthesized 6-class taxonomy. Key cross-group finding: all groups reveal a "single-step vs. trajectory" reliability gap — high step-level performance does not guarantee trajectory safety.

---

### PROMPT 4 | Identify benchmark performance gaps

**Tool used:** AI assistant  
**Prompt:**
```
Compare the following agent benchmarks: WebArena, AgentBench, tau-bench, ACEBench.
For each: (a) what success metric is used, (b) what does the best reported agent achieve,
(c) what does this reveal about trajectory reliability vs. single-step accuracy?
Report specific numbers where available.
```
**Output summary:** WebArena GPT-4 success = 14.41% (humans = 78.24%); AgentBench shows collapse over multi-step chains; tau-bench reveals high pass@k variance; ACEBench reveals argument parsing as primary bottleneck. All confirm the trajectory reliability deficit.

---

## PHASE II — Problem Formalization

### PROMPT 5 | Formalize as a decision process

**Tool used:** AI assistant (mathematical formalization)  
**Prompt:**
```
Formalize a chained tool-calling LLM agent as a Partially Observed Sequential Decision
Process (POSDP). Define the state space S, action space A (tool invocations), observation
space O (tool returns), transition T, emission Omega, and policy pi_theta.
Show how errors at step t propagate to affect the agent's belief and decisions at step t+k.
```
**Output summary:** Derived the POSDP tuple ⟨S, A, O, T, Ω, π_θ, g⟩ and the chained step equation (Eq. 2 in paper). Established the mathematical basis for error propagation analysis.

---

### PROMPT 6 | Error propagation mathematics

**Tool used:** AI assistant  
**Prompt:**
```
Given a chained agent with n tool-call steps, model trajectory integrity formally.
If p is the per-step success probability and errors are autocorrelated (not independent),
how does P(all steps correct) differ from p^n? Derive the conditional form
P(E_1:n) = P(E_1) * product(P(E_t | E_{1:t-1})) and explain what happens
when E_{t-1} = 0 (failure has occurred) in the absence of external verification.
```
**Output summary:** Derived Equation (4) in the paper. Proved that autocorrelated step failures create collapse that is far more severe than the independent bound p^n. Motivated need for formal trajectory integrity metrics.

---

### PROMPT 7 | Develop the six-class taxonomy

**Tool used:** AI assistant  
**Prompt:**
```
Based on the literature synthesis and POSDP formalization, create a comprehensive
taxonomy of failure modes for chained tool-calling agents without human checkpoints.
For each failure class provide: (1) root cause, (2) propagation mechanism,
(3) observable symptom, (4) a machine-verifiable control that could replace
the human checkpoint. The taxonomy should cover planning, tool execution,
state management, environment errors, verification, and security dimensions.
```
**Output summary:** Produced the six-class taxonomy (Table II in paper) with root causes, propagation mechanisms, symptoms, and machine controls for each class.

---

## PHASE III — Experiment Design & Implementation

### PROMPT 8 | Design the simulation experiment

**Tool used:** AI assistant (experimental design)  
**Prompt:**
```
Design a Monte Carlo simulation to validate trajectory-level failure compounding in
chained LLM agents. The simulation should:
1. Model trajectories of length n in {5, 10, 15, 20, 25, 30, 40, 50}
2. Implement three control conditions: no checkpoint, fixed-interval (every 5 steps),
   adaptive risk-sensitive (triggered by R_t >= 0.70)
3. Track: task success rate, divergence rate, avg irreversible errors per trajectory,
   avg human interventions
4. Use 1000 Monte Carlo trials per configuration (24,000 total)
Return the Python class structure and key functions needed.
```
**Output summary:** Designed `ChainedAgentTrajectorySimulator` class with `run_trajectory()` and `evaluate_batch()` methods. Established risk score formula with four factors: epistemic uncertainty U, irreversibility I, privilege P, consequence C.

---

### PROMPT 9 | Implement the simulator

**Tool used:** AI assistant (code generation)  
**Prompt:**
```
Implement the Python simulation class for the chained agent trajectory experiment.
The ChainedAgentTrajectorySimulator should:
- Model per-step success with base probability p_base = 0.95
- Apply autocorrelation penalty of 0.40 when state has diverged
- Compute dynamic risk scores using sigmoid(alpha*U + beta*I + gamma*P + delta*C)
- For 'adaptive' mode: trigger checkpoint when R_t >= tau_escalate = 0.70
- For 'fixed_5' mode: trigger checkpoint every 5 steps
- Checkpoint action: if state is invalid, correct it (simulate human error correction)
Make the code clean, well-commented, and reproducible with a fixed random seed.
```
**Output summary:** Implemented `src/agent_simulator.py` (fully functional, seed=42, produces deterministic results). Validated against expected failure rate curves.

---

### PROMPT 10 | Validate simulation outputs

**Tool used:** AI assistant  
**Prompt:**
```
Given these simulation results for n=50 steps across 1000 trials:
- Unsupervised: success=8.5%, irreversible_errors=2.816
- Fixed-5: success=95.5%, irreversible_errors=0.820, interventions=10.00
- Adaptive: success=79.0%, irreversible_errors=0.466, interventions=9.08

Validate these results against theoretical predictions from:
1. The independent step model (p=0.95)^50 = 7.69%
2. The WebArena empirical finding (14.41% GPT-4 success on complex tasks)
3. The tau-bench finding of high behavioral variance across trials

Do the numbers make sense? Identify any anomalies or concerns.
```
**Output summary:** Results validated. Unsupervised 8.5% closely matches theoretical floor of 7.69% for autocorrelated failures. Adaptive's 79% confirms Pareto-optimal operating point. No anomalies identified.

---

## PHASE IV — Writing & Paper Completion

### PROMPT 11 | Write the IEEE-format paper structure

**Tool used:** AI assistant  
**Prompt:**
```
Write a complete IEEE conference paper in IEEEtran LaTeX format on the topic:
"Failure Modes in Chained Tool-Calling Agents Operating Without Human Checkpoints"
The paper should include: abstract (250 words), introduction with central thesis,
review methodology (22 papers, 6 RQs), background (Toolformer/ReAct/ToolLLM evolution,
verification ceiling), formal POSDP framework, six-class taxonomy with detailed subsections,
error propagation dynamics with 4 cascade archetypes, empirical evaluation with
Monte Carlo results, discussion (failure syndromes, benchmark implications,
autonomy-safety tradeoff), critical analysis of mitigations, research challenges,
5-pillar architectural blueprint for verifiable autonomy, future work, conclusion,
acknowledgments, and 22 IEEEtran-style references. Include TikZ figures for
the execution workflow and taxonomy tree.
```
**Output summary:** Produced complete `paper/main.tex` (549 lines, 14 sections, 25 subsections, 7 equations, 4 tables, 3 TikZ figures). All LaTeX environments balanced (40 open / 40 close).

---

### PROMPT 12 | Generate the trajectory collapse visualization

**Tool used:** AI assistant (TikZ figure generation)  
**Prompt:**
```
Create a TikZ line chart showing task success rate vs. chain length n for three
control conditions: Unsupervised (red dashed), Fixed-5 (blue solid), Adaptive (green dash-dot).
Data points (chain length → success rate):
- None:     5→75.7%, 10→63.2%, 15→48.4%, 20→38.1%, 25→27.1%, 30→19.6%, 40→13.5%, 50→8.5%
- Fixed-5:  5→95.2%, 10→95.1%, 15→96.3%, 20→95.0%, 25→94.5%, 30→94.6%, 40→94.7%, 50→95.5%
- Adaptive: 5→83.5%, 10→82.8%, 15→80.0%, 20→81.3%, 25→80.0%, 30→77.6%, 40→78.1%, 50→79.0%
Scale y-axis 0–100%, x-axis positions at chain lengths. Include legend inside plot.
```
**Output summary:** Produced Figure 3 (TikZ) showing clear visual separation between the three control regimes, confirming the exponential collapse of unsupervised autonomy.

---

### PROMPT 13 | Evaluate using real outputs only

**Tool used:** AI assistant  
**Prompt:**
```
I have real experimental results from setup, dataset preparation, baseline and
experimental run commands, evaluation, reproduction of key figures.
Compute required metrics for the paper: task success rates across all 24 configurations,
irreversible error accumulation rates, human intervention overhead comparison,
and percentage improvement of Adaptive over Unsupervised at each horizon length.
Only use the actual CSV values from results/trajectory_metrics.csv — do not estimate.
```
**Output summary:** Computed all metrics from real CSV. Key finding: at n=50, Adaptive reduces irreversible errors from 2.816 to 0.466 (83.5% reduction), saves 0.92 interventions per trajectory vs Fixed-5. All numbers verified against raw data.

---

## Summary Statistics

| Phase | Prompts | Primary AI Tool | Key Deliverable |
|---|---|---|---|
| I: Literature | 1–4 | Semantic Scholar + AI synthesis | 22-paper corpus, 6 RQs |
| II: Formalization | 5–7 | Mathematical AI assistant | POSDP formalization, taxonomy |
| III: Experiment | 8–10 | Code generation + validation | 24,000-trial simulation |
| IV: Writing | 11–13 | LaTeX + figure generation | 549-line IEEE paper |

**Total prompts documented: 13**  
**AI tools used:** Semantic Scholar, ResearchRabbit, Elicit, Litmaps, Antigravity (Gemini/Claude)  
**Reproducibility:** All outputs are deterministic (seed=42). Re-running `scripts/run_experiments.py` reproduces exact CSV results.
