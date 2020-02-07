"""
Script to play any two agents against each other, or play manually with any agent.
"""
import numpy as np

from arena import Arena
from game import Game
from players import *


g = Game("Tablut")

# all players
# rp = RandomPlayer(g).play
gp = GreedyPlayer(g).play
hp = HumanPlayer(g).play

Arena(hp, gp, g).play_game(verbose=True)
