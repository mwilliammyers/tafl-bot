"""
Script to play any two agents against each other, or play manually with any agent.
"""


def play(game, player1, player2, verbose=False):
    """Executes one episode of a game.

    Returns:
        either
            winner: player who won the game (1 if player1, -1 if player2)
        or
            draw result returned from the game that is neither 1, -1, nor 0.
    """
    players = [player2, None, player1]
    curr_player = 1
    board = game.init_board()
    it = 0
    while game.game_ended(board, curr_player) == 0:
        it += 1

        if verbose:
            print("Turn ", str(it), "Player ", str(curr_player))
            game.render()

        canonical_board = game.canonical_form(board, curr_player)

        action = players[curr_player + 1](canonical_board)

        valids = game.valid_moves(canonical_board, 1)

        if valids[action] == 0:
            print(action)
            assert valids[action] > 0

        board, curr_player = game.next_state(board, curr_player, action)

    if verbose:
        print(f"Game over: Turn {it} Result {game.game_ended(board, 1)}")
        game.render()

    return game.game_ended(board, 1)


if __name__ == "__main__":
    from game import Game
    from players import *

    g = Game("Tablut")

    # all players
    # rp = RandomPlayer(g).play
    gp = GreedyPlayer(g).play
    hp = HumanPlayer(g).play

    play(g, hp, gp, verbose=True)
