"""
Back-end code implementation for game_interface.
CSC148 Winter, Assignment 1.
January 30, 2018.
"""

from typing import List, Any
from interface_set_up import Game, CurrentState


class SubtractSquare(Game):
    """
    Impliment the game Subtract Square.
    """
    SQUR_INSTRUC = "\nA positive whole number is chosen as the starting value" \
                   " to begin the game. Depending on the current value, the" \
                   " player whose turn it is chooses some square of a " \
                   "positive whole number which is less than the current " \
                   "value. These values are to be subtracted for a new " \
                   "current state value, from which the next player will" \
                   " perform the moves again. Play continues to alternate " \
                   "between the two players until no moves are possible. " \
                   "Whoever is about to play at that point loses!\n"

    def __init__(self, p1_bool: bool) -> None:
        """
        Initalize the game Subtract Square with the first players turn as
        p1_bool, a starting positive whole number and a current state.

        Extends Game init method.
        Doctest dependent upon the player's chosen input value.
        """
        Game.__init__(self, p1_bool)
        self.start_num = int(input('\nProvide a '
                                   'positive whole number: '))
        self._invariant()
        self.current_state = StateSubtractSquare(self.start_num, p1_bool)

    def _invariant(self) -> None:
        """
        Check if number provided is a positive whole number
        """
        assert int(self.start_num) > -1, 'Please enter a positive whole number'

    def __str__(self):
        """
        Return a string representation and message of the name of the game,
        Subtract Square self.
        Overrides Game.__str__()

        Doctest dependent upon the player's chosen input value.
        """
        return "The current game that is being played is Subtract Square"

    def get_instructions(self):
        """
        Return the instructions of Subtract Square.
        Overrides Game.get_instructions()

        Doctest dependent upon the player's chosen input value.
        """
        return SubtractSquare.SQUR_INSTRUC

    def str_to_move(self, move: Any) -> Any:
        """
        Return an integer representation of the move move if and only if it is
        a numerical value.
        Overrides CurrentState.str_to_move()

        Doctest dependent upon the player's chosen input value.
        """
        if str(move).isnumeric():
            return int(move)
        return None


class StateSubtractSquare(CurrentState):
    """
    Impliment the current state of game Subtract Square.
    """

    def __init__(self, start_num: int, first_turn: bool) -> None:
        """
        Initalize the current state of Subtract Square which allows the chosen
        move to be made, possible moves to be aquired, and turns to be swapped.

        >>> new_state_subsq = StateSubtractSquare(5, True)
        >>> new_state_subsq.current_state_number
        5
        >>> new_state_subsq.turn
        True
        """
        CurrentState.__init__(self, first_turn)
        self.current_state_number = start_num
        self.turn = first_turn

    def make_move(self, move: Any) -> Any:
        """
        Update current state by allowing a player choose some square of a
        positive whole number as a move move to subtract from the current state
        number.
        Overrides CurrentState.make_move()

        >>> s_state = StateSubtractSquare(5, True)
        >>> s_state.make_move(4)
        CurrentState(False)
        """
        new_state = StateSubtractSquare(self.current_state_number,
                                        not self.turn)

        if move in self.get_possible_moves():
            new_state_num = int(self.current_state_number) - int(move)
            new_state.current_state_number = new_state_num

            if self.get_current_player_name() == 'p1':
                new_state.current_player = 'p2'
            else:
                new_state.current_player = 'p1'
            return new_state
        else:
            raise ValueError('The move you have chosen is not valid')

    def get_possible_moves(self) -> List[int]:
        """
        Return a list of all the possible squares of positive whole numbers
        less than the current state number.
        Overrides CurrentState.get_possible_moves()

        >>> s_state = StateSubtractSquare(5, True)
        >>> s_state.get_possible_moves()
        [1, 4]
        """
        return [s for s in range(1, int(self.current_state_number + 1)) if
                s ** (1/2) % 1 == 0]

    def __str__(self):
        """
        Return a string representation of the current state of Subtract Square
        self, including the current player and the current game value.
        Overrides CurrentState.__str__()

        >>> s_state = StateSubtractSquare(5, True)
        >>> print(s_state)
        The current player is p1, and the current value is 5
        """
        return "The current player is {}, and the current value is {}".\
            format(self.current_player,
                   self.current_state_number)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
