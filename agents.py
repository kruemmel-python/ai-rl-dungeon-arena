################################################################################
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input, LayerNormalization
from tensorflow.keras.optimizers import Adam
from config import LEARNING_RATE, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY_RATE, BATCH_SIZE, MEMORY_SIZE_MAX, TARGET_UPDATE_FREQ, PRIORITIZED_REPLAY_EPS
from replay_buffer import PrioritizedReplayBuffer

# Deep Q-Network Agenten Klasse
class DDQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = PrioritizedReplayBuffer(MEMORY_SIZE_MAX)
        self.gamma = GAMMA
        self.epsilon = EPSILON_START
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY_RATE
        self.learning_rate = LEARNING_RATE
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        self.train_step_counter = 0
        self.last_reward = 0

    def on_done(self):
        self.last_reward = 0

    def _build_model(self):
        input_layer = Input(shape=(self.state_size,))
        x = Dense(128, activation='relu')(input_layer)
        x = LayerNormalization()(x)
        x = Dense(128, activation='relu')(x)
        x = LayerNormalization()(x)
        output_layer = Dense(self.action_size, activation='linear')(x)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done, error):
        self.memory.add(state, action, reward, next_state, done, error)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            state = np.reshape(state, [1, self.state_size])
            q_values = self.model.predict(state, verbose=0)
            return np.argmax(q_values[0])

    def train_step(self, state, action, reward, next_state, done):
        self.train_step_counter += 1
        self.epsilon = max(self.epsilon_min, self.epsilon - self.epsilon_decay)
        if self.memory.tree.n_entries < BATCH_SIZE:
            return
        mini_batch, idxs, is_weights = self.memory.sample(BATCH_SIZE)
        states = np.array([transition[0] for transition in mini_batch])
        actions = np.array([transition[1] for transition in mini_batch])
        rewards = np.array([transition[2] for transition in mini_batch])
        next_states = np.array([transition[3] for transition in mini_batch])
        dones = np.array([transition[4] for transition in mini_batch])

        target_q_values = self.target_model.predict(next_states, verbose=0)
        target_q_values_for_max = self.model.predict(next_states, verbose=0)

        max_actions = np.argmax(target_q_values_for_max, axis=1)

        targets = rewards + self.gamma * (1 - dones) * target_q_values[np.arange(BATCH_SIZE), max_actions]
        q_values = self.model.predict(states, verbose=0)
        q_values[np.arange(BATCH_SIZE), actions] = targets

        absolute_errors = np.abs(targets - q_values[np.arange(BATCH_SIZE), actions])

        self.model.train_on_batch(states, q_values, sample_weight=is_weights)
        self.memory.batch_update(idxs, absolute_errors)

        if self.train_step_counter % TARGET_UPDATE_FREQ == 0:
            self.update_target_model()
            print("Target model updated")

    def load(self, name):
        self.model.load_weights(name)
        self.target_model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

# Agent Klasse für den Boss
class BossAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = PrioritizedReplayBuffer(MEMORY_SIZE_MAX)
        self.gamma = GAMMA
        self.epsilon = EPSILON_START
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY_RATE
        self.learning_rate = LEARNING_RATE
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        self.train_step_counter = 0
        self.last_reward = 0

    def on_done(self):
        self.last_reward = 0

    def _build_model(self):
        input_layer = Input(shape=(self.state_size,))
        x = Dense(128, activation='relu')(input_layer)
        x = LayerNormalization()(x)
        x = Dense(128, activation='relu')(x)
        x = LayerNormalization()(x)
        output_layer = Dense(self.action_size, activation='linear')(x)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done, error):
        self.memory.add(state, action, reward, next_state, done, error)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            state = np.reshape(state, [1, self.state_size])
            q_values = self.model.predict(state, verbose=0)
            return np.argmax(q_values[0])

    def train_step(self, state, action, reward, next_state, done):
        self.train_step_counter += 1
        self.epsilon = max(self.epsilon_min, self.epsilon - self.epsilon_decay)
        if self.memory.tree.n_entries < BATCH_SIZE:
            return
        mini_batch, idxs, is_weights = self.memory.sample(BATCH_SIZE)
        states = np.array([transition[0] for transition in mini_batch])
        actions = np.array([transition[1] for transition in mini_batch])
        rewards = np.array([transition[2] for transition in mini_batch])
        next_states = np.array([transition[3] for transition in mini_batch])
        dones = np.array([transition[4] for transition in mini_batch])

        target_q_values = self.target_model.predict(next_states, verbose=0)
        target_q_values_for_max = self.model.predict(next_states, verbose=0)

        max_actions = np.argmax(target_q_values_for_max, axis=1)

        targets = rewards + self.gamma * (1 - dones) * target_q_values[np.arange(BATCH_SIZE), max_actions]
        q_values = self.model.predict(states, verbose=0)
        q_values[np.arange(BATCH_SIZE), actions] = targets

        absolute_errors = np.abs(targets - q_values[np.arange(BATCH_SIZE), actions])

        self.model.train_on_batch(states, q_values, sample_weight=is_weights)
        self.memory.batch_update(idxs, absolute_errors)

        if self.train_step_counter % TARGET_UPDATE_FREQ == 0:
            self.update_target_model()
            print("Boss Target model updated")

    def load(self, name):
        self.model.load_weights(name)
        self.target_model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
