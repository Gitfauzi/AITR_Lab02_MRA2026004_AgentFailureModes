"""
Agent Failure Modes Simulation Engine
Simulates chained tool-calling agent trajectories under varying error propagation models:
1. Independent step failure model: P(all correct) = p^n
2. Autocorrelated / Cascading failure model: P(E_{1:n}) = P(E_1) * prod(P(E_t | E_{1:t-1}))
3. Adaptive Risk-Sensitive Checkpointing model: R_t = sigma(alpha*U_t + beta*I_t + gamma*P_t + delta*C_t)
"""

import math
import random
from typing import Dict, List, Tuple


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(min(x, 15.0), -15.0)))


class ChainedAgentTrajectorySimulator:
    def __init__(
        self,
        base_step_accuracy: float = 0.95,
        autocorrelation_penalty: float = 0.40,
        irreversible_tool_ratio: float = 0.20,
        risk_weights: Tuple[float, float, float, float] = (1.5, 2.5, 2.0, 2.0),
        escalation_threshold: float = 0.70,
        seed: int = 42
    ):
        self.p_base = base_step_accuracy
        self.penalty = autocorrelation_penalty
        self.irreversible_ratio = irreversible_tool_ratio
        self.alpha, self.beta, self.gamma, self.delta = risk_weights
        self.tau_escalate = escalation_threshold
        random.seed(seed)

    def compute_risk_score(
        self,
        uncertainty: float,
        irreversibility: float,
        privilege: float,
        consequence: float
    ) -> float:
        """
        Computes dynamic risk score:
        R_t = sigma(alpha * U_t + beta * I_t + gamma * P_t + delta * C_t - bias)
        """
        raw_score = (
            self.alpha * uncertainty +
            self.beta * irreversibility +
            self.gamma * privilege +
            self.delta * consequence
        ) - 4.0  # Center around operational threshold
        return sigmoid(raw_score)

    def run_trajectory(
        self,
        chain_length: int,
        checkpoint_mode: str = "none"  # "none", "fixed_5", "adaptive"
    ) -> Dict[str, any]:
        """
        Simulates a single multi-step tool-calling trajectory.
        Modes:
        - 'none': Fully autonomous (no human checkpoints)
        - 'fixed_5': Fixed human checkpoint every 5 steps
        - 'adaptive': Risk-sensitive dynamic checkpointing when R_t >= tau_escalate
        """
        state_valid = True
        trajectory_diverged = False
        earliest_divergence_step = -1
        irreversible_errors = 0
        human_interventions = 0
        step_logs = []

        for step in range(1, chain_length + 1):
            # Dynamic attributes of the tool call at step t
            is_irreversible = random.random() < self.irreversible_ratio
            irreversibility = 1.0 if is_irreversible else 0.1
            privilege = random.uniform(0.3, 0.9) if is_irreversible else random.uniform(0.1, 0.4)
            uncertainty = random.uniform(0.05, 0.35) if state_valid else random.uniform(0.40, 0.85)
            consequence = random.uniform(0.5, 0.95) if is_irreversible else random.uniform(0.05, 0.3)

            # Compute risk
            risk_t = self.compute_risk_score(uncertainty, irreversibility, privilege, consequence)

            # Determine checkpoint trigger
            checkpoint_triggered = False
            if checkpoint_mode == "fixed_5" and (step % 5 == 0):
                checkpoint_triggered = True
            elif checkpoint_mode == "adaptive" and (risk_t >= self.tau_escalate):
                checkpoint_triggered = True

            if checkpoint_triggered:
                human_interventions += 1
                # Human checkpoint acts as error-correction boundary: restores state validity
                if not state_valid:
                    state_valid = True  # Human caught and corrected the latent drift

            # Compute conditional step success probability
            if state_valid:
                p_step = self.p_base
            else:
                # Once diverged, error propagation reduces step accuracy drastically
                p_step = max(0.10, self.p_base - self.penalty)

            step_success = random.random() < p_step

            if not step_success:
                if state_valid:
                    # First divergence
                    state_valid = False
                    trajectory_diverged = True
                    if earliest_divergence_step == -1:
                        earliest_divergence_step = step

                if is_irreversible:
                    irreversible_errors += 1

            step_logs.append({
                "step": step,
                "risk_score": round(risk_t, 4),
                "is_irreversible": is_irreversible,
                "checkpoint": checkpoint_triggered,
                "step_success": step_success,
                "state_valid": state_valid
            })

        return {
            "chain_length": chain_length,
            "mode": checkpoint_mode,
            "success": state_valid,
            "trajectory_diverged": trajectory_diverged,
            "earliest_divergence": earliest_divergence_step,
            "irreversible_errors": irreversible_errors,
            "human_interventions": human_interventions,
            "steps": step_logs
        }


def evaluate_batch(
    num_trials: int = 500,
    chain_length: int = 20,
    checkpoint_mode: str = "none",
    seed: int = 42
) -> Dict[str, float]:
    """Evaluates a batch of trajectories and computes statistical reliability metrics."""
    sim = ChainedAgentTrajectorySimulator(seed=seed)
    success_count = 0
    total_irreversible_errors = 0
    total_interventions = 0
    divergence_count = 0

    for _ in range(num_trials):
        res = sim.run_trajectory(chain_length=chain_length, checkpoint_mode=checkpoint_mode)
        if res["success"]:
            success_count += 1
        if res["trajectory_diverged"]:
            divergence_count += 1
        total_irreversible_errors += res["irreversible_errors"]
        total_interventions += res["human_interventions"]

    return {
        "trials": num_trials,
        "chain_length": chain_length,
        "mode": checkpoint_mode,
        "task_success_rate": round(success_count / num_trials, 4),
        "divergence_rate": round(divergence_count / num_trials, 4),
        "avg_irreversible_errors": round(total_irreversible_errors / num_trials, 4),
        "avg_human_interventions": round(total_interventions / num_trials, 4)
    }
