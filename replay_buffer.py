################################################################################
import numpy as np
import random
from config import PRIORITIZED_REPLAY_EPS

# Prioritized Replay Buffer Klasse
class SumTree:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)
        self.n_entries = 0
        self.next_leaf_index = 0

    def _propagate(self, index, change):
        parent = (index - 1) // 2
        self.tree[parent] += change
        if parent != 0:
            self._propagate(parent, change)

    def _retrieve(self, index, s):
        left = 2 * index + 1
        right = left + 1

        if left >= len(self.tree):
            return index

        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s - self.tree[left])

    def add(self, priority, data):
        leaf_index = self.next_leaf_index
        self.data[leaf_index] = data
        self.update(leaf_index, priority)
        self.n_entries = min(self.n_entries + 1, self.capacity)
        self.next_leaf_index = (self.next_leaf_index + 1) % self.capacity

    def update(self, index, priority):
        tree_index = index + self.capacity - 1
        if tree_index >= len(self.tree):
            print(f"Index {tree_index} is out of bounds for tree of size {len(self.tree)}")
            return
        change = priority - self.tree[tree_index]
        self.tree[tree_index] = priority
        self._propagate(tree_index, change)

    def get_leaf(self, s):
        tree_index = self._retrieve(0, s)
        data_index = tree_index - self.capacity + 1
        return tree_index, data_index, self.tree[tree_index]

    @property
    def total_priority(self):
        return self.tree[0]

class PrioritizedReplayBuffer:
    def __init__(self, capacity, alpha=0.6, beta_start=0.4, beta_frames=10000):
        self.tree = SumTree(capacity)
        self.capacity = capacity
        self.alpha = alpha
        self.beta_start = beta_start
        self.beta = beta_start
        self.beta_frames = beta_frames
        self.frame = 0

    def add(self, state, action, reward, next_state, done, error):
        priority = self._get_priority(error)
        transition = (state, action, reward, next_state, done)
        self.tree.add(priority, transition)

    def _get_priority(self, error):
        return (np.abs(error) + PRIORITIZED_REPLAY_EPS) ** self.alpha

    def sample(self, batch_size):
        segment = self.tree.total_priority / batch_size
        idxs = []
        mini_batch = []
        is_weights = []

        for i in range(batch_size):
            a = segment * i
            b = segment * (i + 1)
            s = random.uniform(a, b)
            tree_index, data_index, priority = self.tree.get_leaf(s)

            prob = priority / self.tree.total_priority
            is_weight = (self.tree.n_entries * prob) ** (-self.beta)
            is_weights.append(is_weight)

            idxs.append(tree_index)
            mini_batch.append(self.tree.data[data_index])

        self.beta = min(1.0, self.beta + (1 - self.beta_start) / self.beta_frames)

        is_weights_normalized = np.array(is_weights) / np.max(is_weights)

        self.frame += 1

        return mini_batch, idxs, is_weights_normalized

    def batch_update(self, tree_idxs, errors):
        priorities = self._get_priority(errors)
        for tree_idx, priority in zip(tree_idxs, priorities):
            self.tree.update(tree_idx, priority)
