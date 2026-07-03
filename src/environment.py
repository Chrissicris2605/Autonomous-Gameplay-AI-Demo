"""Grid-based environment for the autonomous gameplay AI demo."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class Action(str, Enum):
    """Possible movement actions for the agent."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass(frozen=True)
class Position:
    """A position inside the grid."""

    row: int
    col: int


@dataclass
class StepResult:
    """Result returned after applying an action to the environment."""

    position: Position
    reward: int
    done: bool
    message: str


class GridEnvironment:
    """Simple grid world with obstacles, rewards, and a target goal."""

    def __init__(
        self,
        width: int = 8,
        height: int = 6,
        start: Position | None = None,
        goal: Position | None = None,
        obstacles: Iterable[Position] | None = None,
        rewards: dict[Position, int] | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.start = start or Position(0, 0)
        self.goal = goal or Position(height - 1, width - 1)
        self.obstacles = set(obstacles or self._default_obstacles())
        self.rewards = dict(rewards or self._default_rewards())
        self.agent_position = self.start
        self.collected_rewards: set[Position] = set()

    def reset(self) -> Position:
        """Reset the environment to its initial state."""
        self.agent_position = self.start
        self.collected_rewards.clear()
        return self.agent_position

    def available_actions(self) -> list[Action]:
        """Return all actions that do not leave the grid or hit obstacles."""
        valid_actions: list[Action] = []
        for action in Action:
            next_position = self.next_position(self.agent_position, action)
            if self.is_valid_position(next_position):
                valid_actions.append(action)
        return valid_actions

    def step(self, action: Action) -> StepResult:
        """Apply an action and return the resulting state, reward, and status."""
        next_position = self.next_position(self.agent_position, action)

        if not self.is_inside_grid(next_position):
            return StepResult(self.agent_position, -8, False, "Hit grid boundary")

        if next_position in self.obstacles:
            return StepResult(self.agent_position, -10, False, "Hit obstacle")

        self.agent_position = next_position
        reward = -1
        message = "Moved"

        if next_position in self.rewards and next_position not in self.collected_rewards:
            reward += self.rewards[next_position]
            self.collected_rewards.add(next_position)
            message = "Collected reward"

        if next_position == self.goal:
            reward += 50
            return StepResult(next_position, reward, True, "Reached goal")

        return StepResult(next_position, reward, False, message)

    def next_position(self, position: Position, action: Action) -> Position:
        """Return the position that would result from applying an action."""
        if action == Action.UP:
            return Position(position.row - 1, position.col)
        if action == Action.DOWN:
            return Position(position.row + 1, position.col)
        if action == Action.LEFT:
            return Position(position.row, position.col - 1)
        if action == Action.RIGHT:
            return Position(position.row, position.col + 1)
        raise ValueError(f"Unknown action: {action}")

    def is_inside_grid(self, position: Position) -> bool:
        """Return whether a position is inside the grid boundaries."""
        return 0 <= position.row < self.height and 0 <= position.col < self.width

    def is_valid_position(self, position: Position) -> bool:
        """Return whether a position is inside the grid and not blocked."""
        return self.is_inside_grid(position) and position not in self.obstacles

    def manhattan_distance_to_goal(self, position: Position) -> int:
        """Return the Manhattan distance from a position to the goal."""
        return abs(position.row - self.goal.row) + abs(position.col - self.goal.col)

    def _default_obstacles(self) -> set[Position]:
        return {
            Position(1, 2),
            Position(2, 2),
            Position(3, 2),
            Position(3, 4),
            Position(4, 4),
            Position(1, 5),
        }

    def _default_rewards(self) -> dict[Position, int]:
        return {
            Position(0, 4): 8,
            Position(2, 6): 10,
            Position(4, 1): 6,
        }
