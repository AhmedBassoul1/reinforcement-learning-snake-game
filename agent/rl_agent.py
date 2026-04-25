import torch
import random
import numpy as np
from collections import deque
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.snake_game_for_AI import Direction, Point, SnakeGame

MAX_MEMORY = 100_000
BATCH_SIZE = 1_000
LEARNING_RATE = 0.001

class Agent:

    def __init__(self):

        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)

        

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_mermory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass

def train():
    pass


if __name__== "__main__":
    train()
 