from colorama import Fore, Back, Style 
from copy import copy
from aux import add, mult, Direction

class State:

    def __init__(self, board, player, s1, s2, action):
        self.board = board
        self.player = player
        self.action = action
        self.score = {}
        self.score[1] = s1
        self.score[2] = s2

    def game_over(self) -> bool:
        if self.score[1] <= 0:
            print("player 2 won")
            return True
        elif self.score[2] <= 0:
            print("player 1 won")
            return True
        return False

    @staticmethod
    def valid_position(pos: tuple) -> bool:
        return pos[0] in range(0, 8) and pos[1] in range(0, 8)

    def in_last_row(self, pos: tuple) -> bool:
        return (self.player == 1 and pos[0] == 0) or (self.player == 2 and pos[0] == 7)

    def copy(self):
        board = [row.copy() for row in self.board]
        player = self.player + 0
        action = self.action
        return State(board, player, self.score[1], self.score[2], action)

    def get_children(self) -> list:

        ret_states = []

        if self.action.type == "start":
            # TODO: check if any piece can capture
            # TODO: if no piece can capture then try jumps and moves for each piece on the board

            regular_arr = []

            for row in range(0,8): 
                for col in range(0,8):
                    pos = (row, col)

                    for vec in [Direction.WEST, Direction.EAST]:
                        n_state = self.capture(pos, vec)
                        if n_state != None: ret_states.append(n_state)

                    for vec in [Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST]:
                        n_state = self.capture(pos, vec)
                        if n_state != None: ret_states.append(n_state)

                        if ret_states: continue
                        
                        n_state = self.move(pos, vec) or self.jump(pos, vec)
                        if n_state != None: 
                            regular_arr.append(n_state)

            if not ret_states:
                # TODO: check if it is possible to assign
                ret_states.extend(regular_arr)

        elif self.action.type == "place":
            # TODO: generate all possible placing possibilities
            row_c = 0 if (self.player == 2) else 6

            for row in range(0, 2):
                for col in range(1, 7):
                    n_state = self.place((row_c + row, col))
                    if n_state != None: ret_states.append(n_state)

        elif self.action.type == "capture":
            # TODO: check all the moves that the capturing piece can do
            for vec in [Direction.WEST, Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST, Direction.EAST]:
                n_state = self.capture(self.action.pos, vec)
                if n_state != None: ret_states.append(n_state)
            
        elif self.action.type == "jump":
            # TODO: check all the jumps that the jumping piece can do
            for vec in [Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST]:
                n_state = self.jump(self.action.pos, vec)
                if n_state != None: ret_states.append(n_state)

        # check if a r_state is a start action, if not get_children of that state until a start state          
        tmp_states = []
        for state in ret_states:
            if state.action.type == "start":
                continue
            
            tmp_states.extend(state.get_children())
            ret_states.remove(state)
            
        ret_states.extend(tmp_states)
        return ret_states

    # ORDINARY MOVE OPERATORS
    def move(self, pos: tuple, vec: tuple):
        if not self.is_ally(pos):
            return None
        
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
        if not self.is_ally(pos):
            return None

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
                n_state.action = Jump(n_pos)

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
        if not self.is_ally(pos):
            return None
        
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
                n_state.action = Capture(n_pos)
        
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
        
        print(Fore.GREEN + 'Player ' + str(self.player) + ' ' + self.action.type + '!')
        print(Style.RESET_ALL, end="")

    def next_turn(self):
        self.player = self.player % 2 + 1
        self.action = Start()

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
        # return not state.is_empty(pos) and not self.is_ally(state, pos)

    def move_direction(self) -> int:
        return 1 if self.player == 2 else -1

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

    def place(self, pos: tuple):
        row = 2 if self.player == 2 else 8
        if  pos[1] not in range(1, 8) or pos[0] not in range(row - 2, row) or not self.is_empty(pos):
            return None

        n_state = self.copy()
        n_state.place_piece(pos, n_state.player)
        n_state.action.pieces -= 1
        
        if n_state.action.pieces == 0:
            n_state.next_turn()
        
        return n_state

    def enter_place_mode(self) -> None:
        row = 1 if (self.player == 2) else 7
        available = self.board[row][1:6].count(0) + self.board[row - 1][1:6].count(0)
        
        if available > 1:
            self.action = Place(2)
        elif available > 0:
            self.action = Place(1)
        else:
            self.next_turn()

class Start:
    type = "start"
    def __init__(self):
        self.type = "start"

class Jump:
    type = "jump"
    pos = (0,0)
    def __init__(self, pos: tuple):
        self.pos = pos
        
class Capture:
    type = "capture"
    pos = (0,0)
    def __init__(self, pos: tuple):
        self.pos = pos

class Place:
    type = "place"
    pieces = 0
    def __init__(self, pieces):
        self.pieces = pieces

start_state = State([
        [0, 2, 2, 2, 2, 2, 2, 0],
        [0, 2, 2, 2, 2, 2, 2, 0], 
        [0, 2, 2, 0, 0, 2, 2, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 1, 1, 1, 1, 1, 0], 
        [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Start())
