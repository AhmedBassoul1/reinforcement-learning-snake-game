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

    def train_short_memory(self, state_old, final_move, reward, state_new, done):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = 0
    plot_mean_scores = 0
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state=state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_mermory()

            if score > record:
                record = score
                #agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

        



if __name__== "__main__":
    train()
 