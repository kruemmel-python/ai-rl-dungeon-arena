################################################################################
# main.py
# Hauptskript, das die Umgebung erstellt und den Trainingsloop startet.
# Beinhaltet das Laden und Speichern der Modelle.

import os
import sys
import numpy as np
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input, LayerNormalization
from tensorflow.keras.optimizers import Adam
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", module="tensorflow")
import random
import time
import math
from config import WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE, MOVE_SPEED, MAX_PLAYERS, MAX_ENEMIES, PLAYER_CLASSES, NUM_EPISODES, MODEL_PATH, BOSS_MODEL_PATH
from environment import DungeonEnvironment

# Hauptfunktion
if __name__ == "__main__":
    env = DungeonEnvironment()
    player_agent_count = len(env.player_agents)
    boss_agent = env.boss_agent
    try:
        for agent in env.player_agents:
            agent.load(MODEL_PATH + ".weights.h5")
        boss_agent.load(BOSS_MODEL_PATH + ".weights.h5")
        print("Models loaded.")
    except:
        print("No existing model found, starting from scratch")

    for episode in range(NUM_EPISODES):
        state = env.reset()
        done = False
        total_reward = 0
        start_time = time.time()
        while not done:
            env.update()
            total_reward = 0
            for agent in env.player_agents:
                total_reward += agent.last_reward
            if env.done:
                break
        end_time = time.time()
        episode_time = end_time - start_time
        print(f"Episode: {episode + 1}/{NUM_EPISODES}, Total Reward: {total_reward:.2f}, Time: {episode_time:.2f} sec")
        if (episode + 1) % 25 == 0:
            for agent in env.player_agents:
                agent.save(MODEL_PATH + ".weights.h5")
            boss_agent.save(BOSS_MODEL_PATH + ".weights.h5")
            print("Models saved.")
    for agent in env.player_agents:
        agent.save(MODEL_PATH + ".weights.h5")
    boss_agent.save(BOSS_MODEL_PATH + ".weights.h5")
    print("Training complete, models saved.")
