"""Decision policies for the autonomous gameplay AI demo."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod

from environment import Action, GridEnvironment


class BaseAgent(ABC):
    """Base class for agents that choose actions in the grid environment."""

    name: str

    @abstractmethod
    def choose_action(self, environment: GridEnvironment) -> Action:
        """Choose the next action given the current environment state."""


class RandomAgent(BaseAgent):
    """Baseline agent that selects any valid action randomly."""

    name = "Random Agent"

    def choose_action(self, environment: GridEnvironment) -> Action:
        actions = environment.available_actions()
        return random.choice(actions)


class HeuristicAgent(BaseAgent):
    """Simple goal-oriented agent using distance-based action selection."""

    name = "Heuristic Agent"

    def choose_action(self, environment: GridEnvironment) -> Action:
        actions = environment.available_actions()
        current_distance = environment.manhattan_distance_to_goal(environment.agent_position)

        scored_actions: list[tuple[int, int, Action]] = []
        for action in actions:
            next_position = environment.next_position(environment.agent_position, action)
            next_distance = environment.manhattan_distance_to_goal(next_position)
            reward_bonus = environment.rewards.get(next_position, 0)
            distance_improvement = current_distance - next_distance
            score = distance_improvement * 10 + reward_bonus
            scored_actions.append((score, -next_distance, action))

        scored_actions.sort(reverse=True, key=lambda item: (item[0], item[1]))
        return scored_actions[0][2]
