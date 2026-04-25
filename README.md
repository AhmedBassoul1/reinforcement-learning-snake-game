# 🐍 Snake Game with Reinforcement Learning

A classic Snake game implementation paired with a Deep Q-Learning (DQN) agent that learns to play it from scratch using PyTorch. The agent observes its environment, takes actions, and improves its policy over time through trial and error.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Overview

This project contains two main components:

1. **A playable Snake game** built with Pygame — both for humans and as a controllable environment for an AI agent.
2. **A Deep Q-Learning agent** that learns to play Snake on its own through reinforcement learning, using a feed-forward neural network as the Q-function approximator.

The agent starts with no knowledge of the game. Through exploration (random moves) and exploitation (learned moves), it gradually improves its score across thousands of games.

---

## 🗂️ Project Structure

```
snake-game-RL/
├── agent/
│   ├── model/                  # Saved trained models (.pth files)
│   ├── arial.ttf               # Font used by Pygame
│   ├── helper.py               # Live training plot utility (matplotlib)
│   └── rl_agent.py             # The DQN agent + training loop
│
├── environment/
│   ├── arial.ttf               # Font used by Pygame
│   ├── snake_game_for_AI.py    # Game environment exposing a step() API for the agent
│   └── snake_game_for_humain.py # Standalone playable version for humans
│
├── model/
│   └── model.py                # Linear_QNet (PyTorch model) + QTrainer
│
├── snake/                      # Python virtual environment
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/snake-game-RL.git
cd snake-game-RL
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv snake
.\snake\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv snake
source snake/bin/activate
```

### 3. Install dependencies

```bash
pip install pygame torch numpy matplotlib ipython
```

> 💡 You may want to create a `requirements.txt` file with the following content:
> ```
> pygame
> torch
> numpy
> matplotlib
> ipython
> ```
> Then install with `pip install -r requirements.txt`.

---

## 🚀 Usage

### Train the AI agent

From the project root:

```bash
python agent/rl_agent.py
```

A Pygame window will open showing the snake playing, and a matplotlib window will display live training progress (score per game and mean score). Each time the agent beats its previous best score, the model is automatically saved to `model/model.pth`.

### Play the game yourself

```bash
python environment/snake_game_for_humain.py
```

> Note: depending on how you wired keyboard input in the human version, use the arrow keys to control the snake.

---

## 🧠 How the Agent Works

### State representation (11 values)

At every step, the environment is encoded as an 11-dimensional binary vector:

| Index | Feature |
|-------|---------|
| 0–2   | Danger straight / right / left of the head |
| 3–6   | Current direction (left, right, up, down) |
| 7–10  | Food location relative to head (left, right, up, down) |

### Action space (3 values)

The agent chooses one of three relative moves:

- `[1, 0, 0]` → continue straight
- `[0, 1, 0]` → turn right
- `[0, 0, 1]` → turn left

### Reward structure

| Event | Reward |
|-------|--------|
| Eats food | **+10** |
| Game over (collision or timeout) | **−10** |
| Otherwise | **0** |

### Neural network

A simple feed-forward network defined in `model/model.py`:

```
Input (11) → Linear → ReLU → Linear → Output (3)
                       ↑
                 Hidden size = 256
```

### Training algorithm

The agent uses **Deep Q-Learning** with experience replay:

- **Short memory:** trains on every single step right after it happens.
- **Long memory:** at the end of each game, samples a random batch of `BATCH_SIZE = 1000` past experiences from a replay buffer (`MAX_MEMORY = 100,000`) and trains on it.
- **Bellman equation:**
  
  ```
  Q_new = reward + γ · max(Q(next_state))
  ```
  
  with discount factor `γ = 0.9`.
- **Exploration vs exploitation:** ε-greedy strategy where ε decays as `80 - n_games`. Early games are mostly random; later games rely on the learned policy.

---

## 🔧 Hyperparameters

These can be tweaked in `agent/rl_agent.py` and `model/model.py`:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `MAX_MEMORY` | 100,000 | Replay buffer size |
| `BATCH_SIZE` | 1,000 | Mini-batch size for long memory |
| `LR` | 0.001 | Learning rate (Adam optimizer) |
| `gamma` | 0.9 | Discount factor for future rewards |
| `epsilon` | `80 - n_games` | Exploration rate (decays over time) |
| `hidden_size` | 256 | Hidden layer neurons |
| `BLOCK_SIZE` | 20 | Pixel size of one grid cell |
| `SPEED` | 50 | Game speed (FPS) during training |

---

## 📊 Expected Results

With the default settings, you should typically observe:

- **Games 1–80:** mostly random behavior, scores between 0 and a few points.
- **Games 80–200:** the agent starts heading toward food and avoiding walls.
- **Games 200+:** consistent improvement, scores often above 20.
- **Long term:** records of 40+ are achievable. Performance plateaus depending on state representation limits (the snake doesn't "see" its full body, so it can trap itself at large sizes).

---

## 🛠️ Possible Improvements

- Use a richer state representation (e.g., a full grid view via CNN).
- Implement a **target network** for more stable Q-learning.
- Add **Double DQN** or **Dueling DQN** to reduce overestimation bias.
- Add **Prioritized Experience Replay**.
- Reward shaping: small positive reward for getting closer to food, small negative for getting farther.
- Save and reload checkpoints to resume training.
- Add a script to watch a trained model play without further learning.

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'environment'` or `'model'`**  
Run the script from the project root directory, not from inside `agent/`. The `sys.path.append(...)` in `rl_agent.py` expects the project root as the working directory's parent.

**`pygame.error: Couldn't open arial.ttf`**  
Make sure `arial.ttf` is present in the same directory as the script being run, or change the font loading line to `pygame.font.SysFont('arial', 25)`.

**Pygame window freezes**  
This is usually because matplotlib is blocking. The `helper.py` file uses `plt.ion()` and `plt.pause(.1)` to keep things interactive — make sure those calls aren't removed.

---

## 📚 References

- [Mnih et al., "Playing Atari with Deep Reinforcement Learning" (2013)](https://arxiv.org/abs/1312.5602) — the original DQN paper.
- [PyTorch documentation](https://pytorch.org/docs/stable/index.html)
- [Pygame documentation](https://www.pygame.org/docs/)

---

## 📝 License

This project is released under the MIT License. Feel free to use, modify, and share it.

---

## 👤 Author

Built with ❤️ as a hands-on project to learn deep reinforcement learning fundamentals.