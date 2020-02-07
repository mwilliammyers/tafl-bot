import numpy as np
import time


class Arena:
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, display=lambda x: x):
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
        self.display = display

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
                self.display(board)

            canonical_board = self.game.canonical_form(board, curr_player)

            action = players[curr_player + 1](canonical_board)

            valids = self.game.valid_moves(canonical_board, 1)

            if valids[action] == 0:
                print(action)
                assert valids[action] > 0

            board, curr_player = self.game.next_state(board, curr_player, action)

        if verbose:
            print(f"Game over: Turn {it} Result {self.game.game_ended(board, 1)}")
            self.display(board)

        return self.game.game_ended(board, 1)

    def play_games(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts num/2 games.

        Returns:
            one_wins: games won by player1
            two_wins: games won by player2
            draws:  games won by nobody
        """

        from pytorch_classification.utils import Bar, AverageMeter

        eps_time = AverageMeter()
        bar = Bar("Arena.play_games", max=num)
        end = time.time()
        eps = 0
        maxeps = int(num)

        num = int(num / 2)
        one_wins = 0
        two_wins = 0
        draws = 0
        for _ in range(num):
            game_result = self.play_game(verbose=verbose)
            if game_result == 1:
                one_wins += 1
            elif game_result == -1:
                two_wins += 1
            else:
                draws += 1

            # bookkeeping + plot progress
            eps += 1
            eps_time.update(time.time() - end)
            end = time.time()
            bar.suffix = "({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}".format(
                eps=eps,
                maxeps=maxeps,
                et=eps_time.avg,
                total=bar.elapsed_td,
                eta=bar.eta_td,
            )

            bar.next()

        self.player1, self.player2 = self.player2, self.player1

        for _ in range(num):
            game_result = self.play_game(verbose=verbose)
            if game_result == -1:
                one_wins += 1
            elif game_result == 1:
                two_wins += 1
            else:
                draws += 1

            # bookkeeping + plot progress
            eps += 1
            eps_time.update(time.time() - end)
            end = time.time()
            bar.suffix = "({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}".format(
                eps=eps,
                maxeps=maxeps,
                et=eps_time.avg,
                total=bar.elapsed_td,
                eta=bar.eta_td,
            )

            bar.next()

        bar.finish()

        return one_wins, two_wins, draws