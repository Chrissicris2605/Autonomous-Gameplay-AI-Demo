"""Terminal visualization helpers for the autonomous gameplay AI demo."""

from __future__ import annotations

from environment import GridEnvironment, Position


def render_grid(environment: GridEnvironment, path: list[Position] | None = None) -> str:
    """Render the grid as plain text for terminal output."""
    path_set = set(path or [])
    lines: list[str] = []

    for row in range(environment.height):
        cells: list[str] = []
        for col in range(environment.width):
            position = Position(row, col)
            if position == environment.agent_position:
                cells.append("A")
            elif position == environment.start:
                cells.append("S")
            elif position == environment.goal:
                cells.append("G")
            elif position in environment.obstacles:
                cells.append("#")
            elif position in environment.rewards and position not in environment.collected_rewards:
                cells.append("+")
            elif position in path_set:
                cells.append(".")
            else:
                cells.append(" ")
        lines.append("|" + "|".join(cells) + "|")
    return "\n".join(lines)


def print_legend() -> None:
    """Print the grid legend."""
    print("Legend: S=start | A=agent | G=goal | #=obstacle | +=reward | .=visited path")
