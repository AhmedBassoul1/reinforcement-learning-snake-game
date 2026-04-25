import torch
import random
import numpy as np
from collections import deque
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.snake_game_for_AI import Direction, Point, SnakeGame
