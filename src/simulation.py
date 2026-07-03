"""Simulation runner and metrics for the autonomous gameplay AI demo."""

from __future__ import annotations

from dataclasses import dataclass, field

from agent import BaseAgent
from environment import GridEnvironment, Position


@dataclass
class EpisodeResult:
    """Summary of one simulation episode."""

    agent_name: str
    success: bool
    total_reward: int
    steps: int
    path: list[Position] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)


@dataclass
class PolicySummary:
    """Aggregated metrics for multiple episodes."""

    agent_name: str
    episodes: int
    successes: int
    average_reward: float
    average_steps: float

    @property
    def success_rate(self) -> float:
        return self.successes / self.episodes if self.episodes else 0.0


def run_episode(agent: BaseAgent, environment: GridEnvironment, max_steps: int = 40) -> EpisodeResult:
    """Run a single episode and return the result."""
    environment.reset()
    total_reward = 0
    path = [environment.agent_position]
    messages: list[str] = []

    for step_index in range(1, max_steps + 1):
        action = agent.choose_action(environment)
        result = environment.step(action)
        total_reward += result.reward
        path.append(result.position)
        messages.append(f"Step {step_index:02d}: {action.value:<5} | reward={result.reward:>3} | {result.message}")

        if result.done:
            return EpisodeResult(
                agent_name=agent.name,
                success=True,
                total_reward=total_reward,
                steps=step_index,
                path=path,
                messages=messages,
            )

    return EpisodeResult(
        agent_name=agent.name,
        success=False,
        total_reward=total_reward,
        steps=max_steps,
        path=path,
        messages=messages,
    )


def evaluate_policy(agent: BaseAgent, episodes: int, max_steps: int) -> tuple[PolicySummary, EpisodeResult]:
    """Run multiple episodes and return aggregate metrics plus the final episode."""
    results: list[EpisodeResult] = []
    for _ in range(episodes):
        environment = GridEnvironment()
        results.append(run_episode(agent, environment, max_steps=max_steps))

    successes = sum(1 for result in results if result.success)
    average_reward = sum(result.total_reward for result in results) / episodes
    average_steps = sum(result.steps for result in results) / episodes

    return (
        PolicySummary(
            agent_name=agent.name,
            episodes=episodes,
            successes=successes,
            average_reward=average_reward,
            average_steps=average_steps,
        ),
        results[-1],
    )
