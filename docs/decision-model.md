# Decision model

This document explains the simplified decision model used in the public demo.

## Environment

The environment is a small grid world. Each cell can represent:

- an empty space;
- the agent position;
- the start position;
- the goal;
- an obstacle;
- a collectible reward;
- a visited path cell.

The agent can move in four directions:

- up;
- down;
- left;
- right.

Invalid actions include moving outside the grid or into an obstacle.

## Reward design

The reward structure is intentionally simple:

- each valid move has a small cost;
- hitting an obstacle or boundary is penalized;
- collecting reward cells increases the score;
- reaching the goal provides a large positive reward.

This makes the agent balance short-term rewards with progress toward the final goal.

## Policies

### Random Agent

The random agent chooses any valid action at random. It is used as a baseline.

### Heuristic Agent

The heuristic agent scores valid actions using:

- improvement in Manhattan distance to the goal;
- optional reward bonus if the next cell contains a collectible reward.

This is not reinforcement learning. It is a transparent rule-based decision policy designed to demonstrate environment modeling, action scoring, and policy evaluation.

## Why this matters

Many applied AI systems begin with the same foundations:

1. define the environment;
2. define the state;
3. define possible actions;
4. define objectives and rewards;
5. compare behavior across policies;
6. iterate based on measured outcomes.

This demo keeps the implementation small so the decision-making logic remains easy to inspect and explain.
