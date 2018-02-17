"""
Back-end code implementation for game_interface.
CSC148 Winter, Assignment 1.
January 30, 2018.
"""

from typing import List, Any


class Game:
    """
    Impliment a game that can report instructions, possible moves, and if the
    game is over.
    """
    current_state: "CurrentState"

    def __init__(self, p1_bool: bool) -> None:
        """
        Initialize a game self with the current_player p1_bool and
        current_state.

        >>> tic_tac_toe = Game(True)
        >>> tic_tac_toe.current_state
        CurrentState(True)
        """
        self.current_state = CurrentState(p1_bool)

    def __eq__(self, other) -> bool:
        """
        Return True if and only if game self and other have the same set of
        instructions

        Doctest is dependent upon the instance of game self.
        """
        return issubclass(type(self), Game) and issubclass(type(other), Game) \
            and self.get_instructions() == other.get_instructions()

    def __str__(self) -> str:
        """
        Return a string representation of the name of game self.

        Doctest is dependent upon the instance of game self.
        """
        raise NotImplementedError('Subclass Required')

    def get_instructions(self) -> str:
        """
        Return a string representaiton of the instructions of game self.

        Doctest depends upon instance of game self.
        """
        raise NotImplementedError('Subclass Required')

    def is_over(self, current_state: 'CurrentState') -> bool:
        """
        Return True if the game self is over. This is eqivalent to returning
        True if there are no more possible moves.

        Doctest dependent upon instance of game self.
        """
        return current_state.get_possible_moves() == []

    def is_winner(self, player: str) -> bool:
        """
        Return True if the player player is the same as the other existing
        player for game self.

        Doctest is dependent upon the current state of the game.
        """
        if self.is_over(self.current_state):
            return player != self.current_state.current_player
        return False

    def str_to_move(self, move: Any) -> None:
        """
        Return an accurate representation of the move move depending on the
        game self being played.

        Doctest dependent upon instance of game self.
        """
        raise NotImplementedError('Subclass Required')


class CurrentState:
    """
    Impliment a current state for a game that can report the current player,
    possible moves, if a move is valid, and perform a move for a player.
    """
    inital_turn: bool

    def __init__(self, inital_turn: bool) -> None:
        """
        Initalize the current state self of a game with the inital player turn
        as inital_turn.

        >>> tic_tac_toe = CurrentState(True)
        >>> tic_tac_toe.current_player
        'p1'
        >>> tic_tac_toe.p1_turn
        True
        """
        self.p1_turn = inital_turn

        if self.p1_turn:
            self.current_player = 'p1'
        else:
            self.current_player = 'p2'

    def __eq__(self, other) -> bool:
        """
        Return True if and only if the curent state self has the same current
        player as other.

        Doctest is dependent upon the current state self of the game.
        """
        raise NotImplementedError('Subclass Required')

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        Doctest is dependent upon the current state of the game.
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Impliment a representation of CurrentState by returning a constructor
        of the CurrentState class.

        >>> tic_tac_toe = CurrentState(True)
        >>> tic_tac_toe
        CurrentState(True)
        """
        return "CurrentState({})".format(self.p1_turn)

    def get_current_player_name(self) -> str:
        """
        Return the player's name whose turn it currently is in the current
        state self.

        >>> tic_tac_toe = CurrentState(True)
        >>> tic_tac_toe.get_current_player_name()
        'p1'
        """
        return self.current_player

    def is_valid_move(self, move: Any) -> bool:
        """
        Return True if the move move is a valid play for game.

        Doctest dependent upon instance of game self.
        """
        return move in self.get_possible_moves()

    def make_move(self, move: Any) -> None:
        """
        Update the current state self my making the move move for the game.

        Doctest is dependent upon the current state of the game.
        """
        raise NotImplementedError

    def get_possible_moves(self) -> List:
        """
        Return a list of possible moves in the current state self of game.

        Doctest is dependent upon the current state of the game.
        """
        raise NotImplementedError


class SubtractSquare(Game):
    """
    Impliment the game Subtract Square.
    """
    p1_bool: bool
    start_num: int
    current_state: "StateSubtractSquare"

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
    current_state_number: int
    turn = bool

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

        new_state_num = int(self.current_state_number) - int(move)
        new_state.current_state_number = new_state_num

        return new_state

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

    def __eq__(self, other) -> bool:
        """
        Return True if and only if the current state's player and current
        number is the same

        >>> state_sub = StateSubtractSquare(5, True)
        >>> state_other = StateSubtractSquare(10, False)
        >>> state_sub == state_other
        False
        """
        return type(self) and type(other) and self.current_player == \
            other.current_player and self.current_state_number == \
            other.current_state_number


class ChopSticks(Game):
    """
    Impliment the game of Chopsticks
    """
    hand_tup: tuple
    current_state: "StateChopSticks"

    CHOP_INST = "\nEach of two players begins with one finger pointed up on " \
                "each of their hands. Player A touches one hand to one of " \
                "Player B's hands, increasing the number of fingers pointing" \
                " up on Player B's hand by the number on Player A's hand. " \
                "The number pointing up on Player A's hand remains the same." \
                " If Player B now has five fingers up, that hand becomes " \
                "dead or unplayable. If the number of fingers should exceed" \
                " five, subtract five from the sum. Now Player B touches one" \
                " hand to one of Player A's hands, and the distribution of " \
                "fingers proceeds as above, including the possibility of a" \
                " dead hand. Play repeats these steps until some player has" \
                " two dead hands, thus losing.\n"

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
    first_turn: bool
    current_hands: tuple

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
        >>> c_state.get_possible_moves()
        ['ll', 'lr', 'rl', 'rr']

        >>> other_state = StateChopSticks((0,1,1,1), True)
        >>> other_state.get_possible_moves()
        ['rl', 'rr']
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

    def __eq__(self, other) -> bool:
        """
        Return True if and only if the current states player's have identical
        hands.

        >>> state1 = StateChopSticks((1, 2, 3 ,4), True)
        >>> state2 = StateChopSticks((1, 2, 3 ,4), True)
        >>> state3 = StateChopSticks((1, 3, 3 ,4), True)

        >>> state1 == state2
        True
        >>> state1 == state3
        False
        """
        return type(self) and type(other) and self.current_player == \
            other.current_player and self.current_hands == other.current_hands


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
