# AI RL Dungeon Arena

AI RL Dungeon Arena is a project designed to explore reinforcement learning (RL) and artificial intelligence (AI) concepts in a dungeon-based simulation. The project enables training of agents (players and bosses) using deep reinforcement learning in a controlled game environment.

## Features

- **Multi-Agent System**: Players and bosses are controlled by separate AI agents, interacting with each other in a dynamic environment.
- **Class-Based Player Actions**: Each player class (e.g., Tank, Healer, DPS) has unique abilities, actions, and rewards.
- **Boss Behavior**: The boss AI features complex attack patterns, phases, and strategic decision-making.
- **Prioritized Replay Buffer**: Implements efficient experience replay for training deep Q-networks.
- **Customizable Environment**: Configure grid size, player counts, learning rates, and more.
- **Saved Model States**: Agents' training progress is saved for future use.

## Repository

[GitHub Repository](https://github.com/kruemmel-python/ai-rl-dungeon-arena.git)

## Files Overview

### Configuration (`config.py`)
Defines global constants and parameters, such as:
- Grid dimensions
- Agent hyperparameters (e.g., learning rate, epsilon decay)
- Rewards and penalties
- Class-specific abilities

### Entities (`entities.py`)
Contains the definitions for core game entities:
- `Player`: Represents a player with class-specific abilities.
- `Boss`: Implements boss behavior, including phase transitions.
- `Add`: Represents additional enemies summoned by the boss.

### Environment (`environment.py`)
Implements the game environment:
- Resets and initializes game state.
- Defines player and boss states.
- Handles interactions, movements, and actions.

### Agents (`agents.py`)
Defines Deep Q-Network (DQN) agents:
- `DDQNAgent`: Player agents using Double DQN for action-value estimation.
- `BossAgent`: AI for controlling the boss with similar DQN methods.

### Replay Buffer (`replay_buffer.py`)
Implements prioritized replay:
- `SumTree`: Efficient data structure for sampling transitions.
- `PrioritizedReplayBuffer`: Ensures important transitions are replayed more often.

### Actions
Split into modular files, each defining specific actions for player classes:
- `tank_actions.py`
- `healer_actions.py`
- `melee_dps_1_actions.py`
- `melee_dps_2_actions.py`
- `melee_dps_3_actions.py`
- `ranged_dps_1_actions.py`
- `ranged_dps_2_actions.py`
- `ranged_dps_3_actions.py`

### Main Script (`main.py`)
Runs the training loop:
- Initializes the environment and agents.
- Loads or saves models.
- Logs rewards and performance metrics.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kruemmel-python/ai-rl-dungeon-arena.git
   cd ai-rl-dungeon-arena
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure settings in `config.py`.
2. Start training by running:
   ```bash
   python main.py
   ```
3. Monitor progress through the console output or `combat_log.txt`.

## Architecture

The AI system leverages Double DQN with a prioritized replay buffer. Players and the boss operate in a shared grid-based environment with distinct rewards and penalties encouraging goal-oriented behavior.

### Key Components

- **Environment**: Handles game state, action execution, and rewards.
- **Agents**: Learn optimal strategies using DQN.
- **Replay Buffer**: Stores transitions for efficient training.
- **Logging**: Records actions and rewards for analysis.

## Customization

The project is highly modular, allowing customization:
- Add new player classes or abilities.
- Adjust rewards, penalties, or environment parameters.
- Implement alternative RL algorithms.

## Future Work

- Integrate Pygame for visualization.
- Enhance boss AI with more complex strategies.
- Expand replay buffer features for distributed training.

## Author

**Ralf Krümmel**

For inquiries, please visit the [GitHub repository](https://github.com/kruemmel-python/ai-rl-dungeon-arena.git).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

