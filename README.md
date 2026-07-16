# \# Python Texas Hold’em Engine

# 

# A command-line Texas Hold’em engine written in Python. The project models cards, players, community-card dealing, betting rounds, poker-hand detection, winner determination, and Monte Carlo simulations for estimating hand equity.

# 

# \## Project Status

# 

# This project is under active development. A complete game can run from pre-flop through the river and determine a winner, but betting behavior and advanced tie-breaking are still being improved.

# 

# \## Features

# 

# \- Object-oriented game, player, and card models

# \- Shuffled 52-card deck

# \- Two-card player hands

# \- Flop, turn, and river dealing

# \- Detection of:

# &#x20; - Pairs

# &#x20; - Three of a kind

# &#x20; - Four of a kind

# &#x20; - Straights

# &#x20; - Flushes

# &#x20; - Royal flushes

# \- Winner and tie determination

# \- Monte Carlo hand-equity simulation

# \- Basic computer-player behavior

# \- Command-line player interaction

# 

# \## Getting Started

# 

# \### Requirements

# 

# \- Python 3

# 

# The engine is designed to use Python’s standard library. Remove any unused third-party imports before running the project on a new machine.

# 

# \### Run the Game

# 

# Clone or download this repository, open a terminal in the project directory, and run:

# 

# ```bash

# python runner.py

# ```

# 

# The program will ask how many players should join the game. Follow the prompts to play through each betting round.

# 

# \## Project Structure

# 

# ```text

# Poker-Engine/

# ├── card.py          # Playing-card model

# ├── game.py          # Game state, dealing, hand evaluation, and simulation

# ├── montecarlo.py    # Monte Carlo result model

# ├── player.py        # Human and computer-player behavior

# ├── runner.py        # Command-line entry point and game loop

# └── README.md        # Project documentation

# ```

# 

# \## How the Monte Carlo Simulation Works

# 

# For a given player, the engine repeatedly simulates unknown opponent cards and remaining community cards. It evaluates the completed hands and estimates the player’s probability of winning or tying.

# 

# The current simulation runs 40,000 trials for each estimate.

# 

# \## Current Limitations

# 

# \- Betting and raising behavior is still being developed.

# \- Side pots and all-in situations are not yet supported.

# \- Computer-player strategies are experimental.

# \- Automated tests have not yet been added.

# \- Starting another hand in the same session requires further state-reset work.

# 

# \## Planned Improvements

# 


# \- Add varied AI profiles

# \- Complete raising and pot-management logic

# \- Add side-pot and all-in support

# \- Improve game-state resets between hands

# \- Add automated unit tests

# \- Improve command-line input validation

# \- Separate the Monte Carlo simulation from the main game engine

# 

# \## Purpose

# 

# This project was created to strengthen my understanding of:

# 

# \- Object-oriented Python

# \- Probability and simulation

# \- Game-state management

# \- Poker-hand evaluation

# \- Algorithm design

# \- AI decision-making

# 

# \## Author

# 

# Gavin — \[oldlight15](https://github.com/oldlight15)

