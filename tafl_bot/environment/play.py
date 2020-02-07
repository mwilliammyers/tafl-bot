import Arena
from TaflGame import TaflGame, display
from TaflPlayers import *

# from keras.NNet import NNetWrapper as NNet

import numpy as np

# from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = TaflGame("Tablut")

# all players
rp = RandomTaflPlayer(g).play
gp = GreedyTaflPlayer(g).play
hp = HumanTaflPlayer(g).play

# nnet players
# n1 = NNet(g)
# n1.load_checkpoint('./pretrained_models/tafl/keras/','6x100x25_best.pth.tar')
# args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
# mcts1 = MCTS(g, n1, args1)
# n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

arena = Arena.Arena(hp, gp, g, display=display)
# arena = Arena.Arena(gp, rp, g, display=display)
print(arena.playGame(verbose=True))
