# AI-RL Dungeon Arena

This repository contains the implementation of an AI-driven dungeon arena where players and a boss engage in combat. The project utilizes reinforcement learning to train agents to effectively navigate and fight within the arena.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The AI-RL Dungeon Arena project is designed to simulate a dungeon environment where multiple player agents and a boss agent engage in combat. The players and the boss have various abilities and actions they can perform. The goal is to train the agents using reinforcement learning to optimize their strategies for defeating the boss and surviving the encounter.

## Features

- **Reinforcement Learning**: Utilizes Deep Q-Networks (DQN) for training player and boss agents.
- **Diverse Player Classes**: Includes various player classes with unique abilities and actions.
- **Boss Mechanics**: The boss has multiple phases, abilities, and special actions.
- **Reward System**: A comprehensive reward system to guide the agents' learning process.
- **Prioritized Experience Replay**: Enhances the learning efficiency by prioritizing significant experiences.

## Installation

To set up the project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kruemmel-python/ai-rl-dungeon-arena.git
   cd ai-rl-dungeon-arena
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up TensorFlow**:
   Ensure you have TensorFlow installed and configured correctly. The project uses TensorFlow for building and training the neural networks.

## Usage

To run the project, follow these steps:

1. **Navigate to the Project Directory**:
   ```bash
   cd ai-rl-dungeon-arena
   ```

2. **Run the Main Script**:
   ```bash
   python main.py
   ```

3. **Training and Saving Models**:
   The main script will train the agents and save the models periodically. You can adjust the training parameters in the `config.py` file.

## Project Structure

The project is organized into several modules:

- **config.py**: Contains configuration parameters and constants.
- **entities.py**: Defines the player, boss, and add entities.
- **environment.py**: Implements the dungeon environment and game logic.
- **agents.py**: Contains the implementation of the DQN agents for players and the boss.
- **replay_buffer.py**: Implements the prioritized experience replay buffer.
- **boss_actions.py**: Contains the logic for boss actions.
- **main.py**: The main script to run the training loop and manage model saving/loading.
- **tank_actions.py, healer_actions.py, melee_dps_1_actions.py, ...**: Contain the logic for specific player class actions.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or inquiries, feel free to reach out to the project maintainer:

- **Ralf Krümmel**

---

This README provides a comprehensive overview of the AI-RL Dungeon Arena project, including its features, installation instructions, usage guidelines, project structure, contributing information, and licensing details.
