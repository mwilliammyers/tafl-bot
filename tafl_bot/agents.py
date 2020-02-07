import sys

import numpy as np


class Random:
    def __init__(self, game):
        self.game = game

    def act(self, board):
        a = np.random.randint(self.game.action_size())
        valids = self.game.valid_moves(board, board.player_to_move())
        while valids[a] != 1:
            a = np.random.randint(self.game.action_size())
        return a


class Human:
    def __init__(self, game):
        import readline  # for fancy command-line I/O

        self.game = game

    def act(self, board):
        from utils import int2base

        valid_actions = self.game.valid_moves(board, board.player_to_move())

        print([int2base(i, self.game.n, 4) for i, v in enumerate(valid_actions) if v])

        action = None
        while True:
            try:
                x1, y1, x2, y2 = [int(x) for x in input("> ").strip().split(" ")]

                action = x1
                action += y1 * self.game.n
                action += x2 * self.game.n ** 2
                action += y2 * self.game.n ** 3

                if valid_actions[action]:
                    break
                else:
                    print("Try again; that move is not valid")
            except KeyboardInterrupt:
                sys.exit(0)

        return action


class Greedy:
    def __init__(self, game):
        self.game = game

    def act(self, board):
        valids = self.game.valid_moves(board, board.player_to_move())
        candidates = []

        for a in range(self.game.action_size()):
            if valids[a] == 0:
                continue

            next_board, _ = self.game.next_state(board, board.player_to_move(), a)
            score = self.game.score(next_board, board.player_to_move())
            candidates += [(-score, a)]

        candidates.sort()

        return candidates[0][1]
