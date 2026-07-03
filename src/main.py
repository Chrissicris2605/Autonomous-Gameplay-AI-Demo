"""Entry point for the autonomous gameplay AI demo."""

from __future__ import annotations

import argparse
import random

from agent import HeuristicAgent, RandomAgent
from environment import GridEnvironment
from simulation import evaluate_policy, run_episode
from visualization import print_legend, render_grid


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Autonomous Gameplay AI Demo")
    parser.add_argument("--episodes", type=int, default=20, help="Number of evaluation episodes per policy")
    parser.add_argument("--max-steps", type=int, default=40, help="Maximum steps per episode")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducible baseline behavior")
    return parser.parse_args()


def print_summary_table(summaries) -> None:
    print("\nPolicy comparison")
    print("-" * 72)
    print(f"{'Policy':<18} {'Episodes':>8} {'Success':>9} {'Success %':>10} {'Avg Reward':>12} {'Avg Steps':>10}")
    print("-" * 72)
    for summary in summaries:
        print(
            f"{summary.agent_name:<18} "
            f"{summary.episodes:>8} "
            f"{summary.successes:>9} "
            f"{summary.success_rate * 100:>9.1f}% "
            f"{summary.average_reward:>12.2f} "
            f"{summary.average_steps:>10.2f}"
        )
    print("-" * 72)


def main() -> None:
    args = parse_args()
    random.seed(args.seed)

    agents = [RandomAgent(), HeuristicAgent()]
    summaries = []

    print("Autonomous Gameplay AI Demo")
    print("Applied AI / Decision Systems / Grid-Based Simulation")

    for agent in agents:
        summary, _ = evaluate_policy(agent, episodes=args.episodes, max_steps=args.max_steps)
        summaries.append(summary)

    print_summary_table(summaries)

    print("\nFinal demonstration episode using the heuristic agent")
    print("-" * 72)
    demo_environment = GridEnvironment()
    demo_result = run_episode(HeuristicAgent(), demo_environment, max_steps=args.max_steps)

    for message in demo_result.messages:
        print(message)

    print("\nFinal grid")
    print_legend()
    print(render_grid(demo_environment, demo_result.path))

    print("\nEpisode result")
    print(f"Agent: {demo_result.agent_name}")
    print(f"Success: {demo_result.success}")
    print(f"Total reward: {demo_result.total_reward}")
    print(f"Steps: {demo_result.steps}")


if __name__ == "__main__":
    main()
