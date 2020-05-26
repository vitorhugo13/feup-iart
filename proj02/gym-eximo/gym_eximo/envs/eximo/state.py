from colorama import Fore, Back, Style 
from copy import copy

from .utils import add, mult, Direction


class State:

    # action = (INNNER_STATE, (POS | NUM_PIECES)?)
    # 1 - start of a play           ex: [1]
    # 2 - middle of a jump move     ex: [2, (3, 4)]
    # 3 - middle of a capture move  ex: [3, (4, 1)]
    # 4 - middle of a place move    ex: [4, 2]

    # state constructor
    def __init__(self, board, player, s1, s2, action):
        self.board = board
        self.player = player
        self.action = action
        self.score = {}
        self.score[1] = s1
        self.score[2] = s2

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        
        return self.board == other.board and self.player == other.player and self.action == other.action

    @staticmethod
    def valid_position(pos: tuple) -> bool:
        return pos[0] in range(0, 8) and pos[1] in range(0, 8)

    def in_last_row(self, pos: tuple) -> bool:
        return (self.player == 1 and pos[0] == 0) or (self.player == 2 and pos[0] == 7)

    # copy the current state and returns its copy
    def copy(self):
        board = [row.copy() for row in self.board]
        player = self.player + 0
        action = copy(self.action)
        return State(board, player, self.score[1], self.score[2], action)

    # ORDINARY MOVE OPERATORS
    def move(self, pos: tuple, vec: tuple):
        
        dir = self.move_direction()
        n_pos = add(pos, mult(vec, dir))

        if not State.valid_position(n_pos):
            return None
        if not self.is_empty(n_pos):
            return None
        
        n_state = self.copy()
        n_state.remove_piece(pos)

        if self.in_last_row(n_pos):
            n_state.enter_place_mode()
        else:
            n_state.place_piece(n_pos, self.player)
            n_state.next_turn()

        return n_state

    # JUMP MOVE OPERATORS
    def can_jump(self, dir: int, pos: tuple, vec: tuple) -> bool:
        t_pos = add(pos, mult(vec, dir))
        if not State.valid_position(t_pos) or not self.is_ally(t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not State.valid_position(n_pos) or not self.is_empty(n_pos):
            return False
        
        return True

    def jump(self, pos: tuple, vec: tuple):

        dir = self.move_direction()

        t_pos = add(pos, mult(vec, dir))
        if not State.valid_position(t_pos) or not self.is_ally(t_pos):
            return None
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not State.valid_position(n_pos) or not self.is_empty(n_pos):
            return None

        n_state = self.copy()
        n_state.remove_piece(pos)

        if self.in_last_row(n_pos):
            n_state.enter_place_mode()
        else:
            n_state.place_piece(n_pos, self.player)
            if  not (n_state.can_jump(dir, n_pos, Direction.NORTHWEST) or 
                n_state.can_jump(dir, n_pos, Direction.NORTH) or 
                n_state.can_jump(dir, n_pos, Direction.NORTHEAST)):
                n_state.next_turn()
            else:
                n_state.action = [2, n_pos]

        return n_state

    # CAPTURE OPERATORS
    def can_capture(self, dir: int, pos: tuple, vec: tuple) -> bool:
        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_enemy(t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(n_pos):
            return False
        
        return True

    def capture(self, pos: tuple, vec: tuple):
        dir = self.move_direction()

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_enemy(t_pos):
            return None
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(n_pos):
            return None

        n_state = self.copy()
        n_state.remove_piece(pos)
        n_state.remove_piece(t_pos)

        if self.in_last_row(n_pos):
            n_state.enter_place_mode()
        else:
            n_state.place_piece(n_pos, self.player)
            if not (n_state.can_capture(dir, n_pos, Direction.WEST) or 
                n_state.can_capture(dir, n_pos, Direction.NORTHWEST) or 
                n_state.can_capture(dir, n_pos, Direction.NORTH) or 
                n_state.can_capture(dir, n_pos, Direction.NORTHEAST) or 
                n_state.can_capture(dir, n_pos, Direction.EAST)):
                n_state.next_turn()
            else:
                n_state.action = [3, n_pos]
        
        return n_state
    
    def place(self, pos: tuple):
        #  TODO: verify if the player can place a piece
        # return the same state if placing is not possible
        n_state = self.copy()
        n_state.place_piece(pos, n_state.player)
        n_state.action[1] -= 1
        
        if n_state.action[1] == 0:
            n_state.next_turn()
        
        return n_state

    def print(self):
        print()
        print('     A    B    C    D    E    F    G    H')
        print('    ---------------------------------------')
        for row in range(len(self.board)):
            print(' ' + str(row + 1) + ' | ', end="")
            for piece in self.board[row]:
                if piece == 1:
                    print (Back.RED + '  ', end="")
                    print(Style.RESET_ALL, end="")
                elif piece == 2:
                    print (Back.BLUE + '  ', end="")
                    print(Style.RESET_ALL, end="")
                else:
                    print ('  ', end="")
                print (' | ', end="")
            print('\n' + '   | --   --   --   --   --   --   --   --')
        print('Player 1: ' + str(self.score[1]) + ' | Player 2: ' + str(self.score[2]))
        
        if self.action[0] == 1:
            message = "make a move"
        elif self.action[0] == 2:
            message = "keep jumping with piece (" + str(self.action[1][0]) + ", " + str(self.action[1][1]) + ")"
        elif self.action[0] == 3:
            message = "keep capturing with piece (" + str(self.action[1][0]) + ", " + str(self.action[1][1]) + ")"
        elif self.action[0] == 4:
            message = "place a piece in the dropzone"

        print(Fore.GREEN + 'Player ' + str(self.player) + ' ' + message + '!')
        print(Style.RESET_ALL, end="")

    def next_turn(self):
        self.player = self.player % 2 + 1
        self.action = [1]

    def get_piece(self, pos: tuple) -> int:
        return self.board[pos[0]][pos[1]]

    def is_empty(self, pos: tuple) -> bool:
        return self.get_piece(pos) == 0

    def place_piece(self, pos:tuple, piece: int) -> None:
        self.board[pos[0]][pos[1]] = piece
        self.score[piece] += 1

    def remove_piece(self, pos: tuple) -> None:
        player = self.get_piece(pos)
        self.board[pos[0]][pos[1]] = 0
        self.score[player] -= 1

    def is_ally(self, pos: tuple) -> bool:
        return self.get_piece(pos) == self.player

    def is_enemy(self, pos: tuple) -> bool:
        return self.get_piece(pos) == self.player % 2 + 1

    # return the move direction multiplier for the current player
    def move_direction(self) -> int:
        return 1 if self.player == 2 else -1

    # checks if there is a required move
    def check_capture(self) -> bool:
        dir = self.move_direction()
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if not self.is_ally((row, col)):
                    continue

                if (self.can_capture(dir, (row, col), Direction.WEST) or 
                    self.can_capture(dir, (row, col), Direction.NORTHWEST) or 
                    self.can_capture(dir, (row, col), Direction.NORTH) or 
                    self.can_capture(dir, (row, col), Direction.NORTHEAST) or 
                    self.can_capture(dir, (row, col), Direction.EAST)):
                    return True
        return False

    def enter_place_mode(self) -> None:
        row = 1 if (self.player == 2) else 7
        available = self.board[row][1:7].count(0) + self.board[row - 1][1:7].count(0)
        
        if available > 1:
            self.action = [4, 2]
        elif available > 0:
            self.action = [4, 1]
        else:
            self.next_turn()

    def has_moves(self) -> bool:
        # start mode - the player is free to do whatever move he can, 
        # however, if he has the chance to capture he must do so
        if self.action[0] == 1:

            for row in range(0,8): 
                for col in range(0,8):
                    pos = (row, col)

                    if not self.is_ally(pos):
                        continue
                    
                    for vec in [Direction.WEST, Direction.EAST]:
                        n_state = self.capture(pos, vec)
                        if n_state != None:
                            return True

                    for vec in [Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST]:
                        n_state = self.capture(pos, vec)
                        if n_state != None:
                            return True
                        
                        n_state = self.move(pos, vec) or self.jump(pos, vec)
                        if n_state != None: 
                            return True        
        # jump mode
        elif self.action[0] == 2:
            for vec in [Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST]:
                n_state = self.jump(self.action[1], vec)
                if n_state != None:
                    return True

        # capture mode
        elif self.action[0] == 3:
            for vec in [Direction.WEST, Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST, Direction.EAST]:
                n_state = self.capture(self.action[1], vec)
                if n_state != None:
                    return True

        # place mode
        elif self.action[0] == 4:
            row_c = 0 if (self.player == 2) else 6

            # try to place one piece on the dropzone
            for row in range(0, 2):
                for col in range(1, 7):
                    if not self.is_empty((row_c + row, col)):
                        continue
                    return True

        return False

start_state = State([
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 0], 
    [0, 2, 2, 0, 0, 2, 2, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 1, 0, 0, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, [1])

# start_state = State([
#     [0, 2, 2, 2, 2, 2, 2, 0],
#     [0, 2, 2, 0, 2, 2, 2, 0], 
#     [0, 2, 2, 0, 0, 2, 1, 0], 
#     [0, 2, 0, 0, 0, 0, 0, 0], 
#     [0, 1, 0, 0, 0, 0, 0, 0], 
#     [0, 1, 1, 0, 0, 0, 1, 0], 
#     [0, 0, 1, 1, 1, 1, 1, 1], 
#     [0, 1, 1, 1, 1, 1, 0, 0]], 1, 16, 15, [3, (2, 6)])