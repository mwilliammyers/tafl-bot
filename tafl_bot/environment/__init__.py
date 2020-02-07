from typing import Union

import numpy as np

from environment.board import Board
from environment.board.variants import *
from utils import int2base


class Env:
    def __init__(self, board: Union[str, Board] = None):
        self.board = board
        self.init_board()

    def init_board(self):
        """
        Returns:
            board: a representation of the board (ideally this is the form that will be
                   the input to your neural network)
        """
        if self.board is None:
            self.board = Board(Brandubh())
        elif isinstance(self.board, str):
            self.board = Board(globals()[self.board]())

        assert isinstance(self.board, Board)

        self.n = self.board.size

        return self.board

    def board_size(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (self.n, self.n)

    def action_size(self):
        """
        Returns:
            action_size: number of all possible actions
        """
        return self.n ** 4

    def next_state(self, board, player, action):
        """
        Args:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            next_board: board after applying action
            next_player: player who plays in the next turn (should be -player)
        """
        b = board.copy()
        move = int2base(action, self.n, 4)
        b.execute_move(move, player)
        return (b, -player)

    def valid_moves(self, board, player):
        """
        Args:
            board: current board
            player: current player

        Returns:
            valid_moves: a binary vector of length self.getActionSize(), 1 for moves that
                         are valid from the current board and player, 0 for invalid moves
        """

        # Note: Ignoring the passed in player variable since we are not inverting colors
        # for canonical_form and Arena calls with constant 1.
        valids = [0] * self.action_size()

        b = board.copy()

        legal_moves = b.legal_moves(board.player_to_move())

        if not legal_moves:
            valids[-1] = 1
            return np.array(valids)

        for x1, y1, x2, y2 in legal_moves:
            valids[x1 + y1 * self.n + x2 * self.n ** 2 + y2 * self.n ** 3] = 1

        return np.array(valids)

    def game_ended(self, board, player):
        """
        Args:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        return board.done * player

    def canonical_form(self, board, player):
        """
        Args:
            board: current board
            player: current player (1 or -1)

        Returns:
            board: a canonical form of board. The canonical form should be independent of
                   player. For e.g. in chess, the canonical form can be chosen to be from
                   the pov of white. When the player is white, we can return board as is.
                   When the player is black, we can invert the colors and return the board.
        """
        b = board.copy()
        # rules and objectives are different for the different players, so inverting
        # board results in an invalid state.
        return b

    def symmetries(self, board, pi):
        """
        Args:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symm_forms: a list of [(board,pi)] where each tuple is a symmetrical form of
                        the board and the corresponding pi vector. This is used when
                        training the neural network from examples.
        """
        return [(board, pi)]
        # mirror, rotational
        # assert(len(pi) == self.n**4)
        # pi_board = np.reshape(pi[:-1], (self.n, self.n))
        # l = []

        # for i in range(1, 5):
        #    for j in [True, False]:
        #        newB = np.rot90(board, i)
        #        newPi = np.rot90(pi_board, i)
        #        if j:
        #            newB = np.fliplr(newB)
        #            newPi = np.fliplr(newPi)
        #        l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        # return l

    def score(self, board, player):
        if board.done:
            return 1000 * board.done * player
        return board.count_diff(player)

    def __str__(self):
        render_chars = {
            -1: "b",
            0: " ",
            1: "W",
            2: "K",
            10: "#",
            12: "E",
            20: "_",
            22: "x",
        }

        image = self.board.image()

        s = f"   {' '.join(str(i) for i in range(len(image)))}"
        for i in range(len(image) - 1, -1, -1):
            s += f"\n{i:2}"
            for col in image[i]:
                s += f" {render_chars[col]}"

        return s

    def render(self):
        print("---------------------", self, "---------------------", sep="\n")

