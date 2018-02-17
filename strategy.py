"""
Back-end code implementation for game_interface.
CSC148 Winter, Assignment 1.
January 30, 2018.
"""

from typing import Any
import random
from interface_set_up import Game


# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

# TODO: Implement a random strategy.


def random_strategy(game: Game) -> Any:
    """
    Return a move for a game through randomly choosing from possible moves for
    game
    """
    move = random.choice(game.current_state.get_possible_moves())
    return game.str_to_move(move)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
