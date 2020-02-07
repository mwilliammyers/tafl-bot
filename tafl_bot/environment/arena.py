import numpy as np
import time


class Arena:
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game):
        """Initializes the Arena.

        Args:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game

    def play_game(self, verbose=False):
        """Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]
        curr_player = 1
        board = self.game.init_board()
        it = 0
        while self.game.game_ended(board, curr_player) == 0:
            it += 1

            if verbose:
                print("Turn ", str(it), "Player ", str(curr_player))
                self.game.render()

            canonical_board = self.game.canonical_form(board, curr_player)

            action = players[curr_player + 1](canonical_board)

            valids = self.game.valid_moves(canonical_board, 1)

            if valids[action] == 0:
                print(action)
                assert valids[action] > 0

            board, curr_player = self.game.next_state(board, curr_player, action)

        if verbose:
            print(f"Game over: Turn {it} Result {self.game.game_ended(board, 1)}")
            self.game.render()

        return self.game.game_ended(board, 1)
