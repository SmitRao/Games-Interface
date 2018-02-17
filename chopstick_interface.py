"""
Back-end code implementation for game_interface.
CSC148 Winter, Assignment 1.
January 30, 2018.
"""

from typing import List, Any
from interface_set_up import Game, CurrentState


class ChopSticks(Game):
    """
    Impliment the game of Chopsticks
    """
    CHOP_INST = "\nEach of two players begins with one finger pointed up on " \
                "each of their hands. Player A touches one hand to one of " \
                "Player B's hands, increasing the number of fingers pointing" \
                " up on Player B's hand by the number on Player A's hand. " \
                "The number pointing up on Player A's hand remains the same." \
                " If Player B now has five fingers up, that hand becomes " \
                "\dead or unplayable. If the number of fingers should exceed" \
                " five, subtract five from the sum. Now Player B touches one" \
                " hand to one of Player A's hands, and the distribution of " \
                "fingers proceeds as above, including the possibility of a" \
                " \dead hand. Play repeats these steps until some player has" \
                " two \dead hands, thus losing.\n"

    def __init__(self, p1_bool: bool) -> None:
        """
        Initalize the game ChopSticks with one finger up on each hand of p1 and
        p2 as well as its current state.
        Extends Game init method.

        >>> chops = ChopSticks(True)
        >>> chops.hand_tup
        (1, 1, 1, 1)
        >>> chops.current_state
        CurrentState(True)
        """
        Game.__init__(self, p1_bool)
        self.hand_tup = (1, 1, 1, 1)
        self.current_state = StateChopSticks(self.hand_tup, p1_bool)

    def __str__(self):
        """
        Return a string representation and message of the name of the game,
        Chopsticks self.
        Overrides Game.__str__()

        >>> c = ChopSticks(True)
        >>> print(c)
        The current game that is being played is Chopsticks
        """
        return "The current game that is being played is Chopsticks"

    def get_instructions(self):
        """
        Return the instructions of Subtract Square.
        Overrides Game.get_instructions()

        >>> chop_stick = ChopSticks(True)
        >>> instruct = chop_stick.get_instructions()
        >>> instruct == ChopSticks.CHOP_INST
        True
        """
        return ChopSticks.CHOP_INST

    def str_to_move(self, move: Any) -> Any:
        """
        Return a string representation of the move move if and only if it is
        a valid move.
        Overrides CurrentState.str_to_move()

        >>> s = ChopSticks(True)
        >>> s.str_to_move('ll')
        'll'
        """
        if move in ['ll', 'lr', 'rl', 'rr']:
            return move
        return None


class StateChopSticks(CurrentState):
    """
    Impliment the current state of game Subtract Square.
    """

    def __init__(self, hand_tup: tuple, first_turn: bool) -> None:
        """
        Initalize the current state of Chopsticks which allows the chosen
        move to be made, possible moves to be aquired, and turns to be swapped.

        >>> new_chop_state = StateChopSticks((1,2,3,4), True)
        >>> new_chop_state.first_turn
        True

        >>> new_chop_state.current_hands
        (1, 2, 3, 4)
        """
        CurrentState.__init__(self, first_turn)
        self.first_turn = first_turn
        self.current_hands = hand_tup

    def make_move(self, move: Any) -> Any:
        """
        Update current state by allowing a player chooses some move to apply on
        an opponents hand, given that no move is applied with or to a dead hand.
        Overrides CurrentState.make_move()

        >>> c_state = StateChopSticks((1,1,1,1), True)
        >>> c_state.make_move('ll')
        CurrentState(False)
        """
        list1 = list(self.current_hands)

        if self.current_player == 'p1':
            if move == 'rl':
                list1[2] = (list1[2] + list1[1]) % 5
            if move == 'rr':
                list1[3] = (list1[3] + list1[1]) % 5
            if move == 'll':
                list1[2] = (list1[0] + list1[2]) % 5
            if move == 'lr':
                list1[3] = (list1[3] + list1[0]) % 5
            p_val = False

        else:
            if move == 'rl':
                list1[0] = (list1[0] + list1[3]) % 5
            if move == 'rr':
                list1[1] = (list1[1] + list1[3]) % 5
            if move == 'll':
                list1[0] = (list1[0] + list1[2]) % 5
            if move == 'lr':
                list1[1] = (list1[2] + list1[1]) % 5
            p_val = True

        new_hand_tup = tuple(list1)
        new_state = StateChopSticks(new_hand_tup, p_val)

        return new_state

    def get_possible_moves(self) -> List[str]:
        """
        Return a list of all the possible moves that a player can apply to their
        opponent, no move can be applied with and to a dead hand.
        overrides CurentState.get_possible_moves()

        >>> c_state = StateChopSticks((1,1,1,1), True)
        >>> c_state.make_move('ll')
        CurrentState(False)
        >>> c_state.get_possible_moves()
        ['ll', 'lr', 'rl', 'rr']
        """
        possible_moves_list = []
        not_possible_set = set()

        if self.current_player == 'p1':
            curnt_playr_hands = [self.current_hands[0], self.current_hands[1]]
            other_playr_hands = [self.current_hands[2], self.current_hands[3]]
        else:
            curnt_playr_hands = [self.current_hands[2], self.current_hands[3]]
            other_playr_hands = [self.current_hands[0], self.current_hands[1]]

        if curnt_playr_hands[0] == 0:
            not_possible_set.add('ll')
            not_possible_set.add('lr')
        if other_playr_hands[0] == 0:
            not_possible_set.add('ll')
            not_possible_set.add('rl')
        if curnt_playr_hands[1] == 0:
            not_possible_set.add('rl')
            not_possible_set.add('rr')
        if other_playr_hands[1] == 0:
            not_possible_set.add('rr')
            not_possible_set.add('lr')

        for value in ['ll', 'lr', 'rl', 'rr']:
            if value not in not_possible_set:
                possible_moves_list.append(value)
        return possible_moves_list

    def __str__(self):
        """
        Return a string representation of the current state of Subtract Square
        self, including the current player and the current game value.
        Overrides Game.__str__()

        >>> c_state = StateChopSticks((1,1,1,1), True)
        >>> print(c_state)
        Player 1: 1-1; Player 2: 1-1
        """
        return "Player 1: {}-{}; Player 2: {}-{}". \
            format(self.current_hands[0], self.current_hands[1],
                   self.current_hands[2], self.current_hands[3])


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
