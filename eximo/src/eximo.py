from colorama import Fore, Back, Style 
from copy import copy

from state import *
from aux import *


class Eximo:
    start_state = State([
        [0, 2, 2, 2, 2, 2, 2, 0],
        [0, 2, 2, 2, 2, 2, 2, 0], 
        [0, 2, 2, 0, 0, 2, 2, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 1, 1, 1, 1, 1, 0], 
        [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Start())
    player = {}

    def __init__(self, p1: str, p2: str):
        self.player[1] = p1
        self.player[2] = p2

    def play(self):
        state = self.start_state
        while not self.game_over(state):
            state.print()
            print(Fore.GREEN + 'Player ' + str(state.player) + "\'s turn")
            print(Style.RESET_ALL, end="")
            state = self.player_move(state)
            state.print()
            if self.last_row(state):
                state = self.remove_last_row(state)
                state.print()
                state = self.sel_dropzone(state)
                state = self.sel_dropzone(state)
            state = self.change_player(state)
                
    def change_player(self, state: State) -> State:
        state.player = state.player % 2 + 1
        state.action = Start()
        return state

    def game_over(self, state: State) -> bool:
        if state.score[1] == 0:
            print("player 2 won")
            return True
        elif state.score[2] == 0:
            print("player 1 won")
            return True
        return False
            
    def player_move(self, state: State) -> State:
        capture = self.check_capture(state)

        while True:
            pos = self.sel_piece(state)
            while capture and pos not in capture:
                pos = self.sel_piece(state)

            dir = self.sel_direction()
            
            if self.can_move(state, pos, dir):
                n_state = self.move(state, pos, dir)
                break
            elif self.can_jump(state, pos, dir):
                n_state = self.jump_combo(state, pos, dir)
                break
            elif self.can_capture(state, pos, dir):
                n_state = self.capture_combo(state, pos, dir)
                break
        
        n_state.moves -= 1
        return n_state
    
    def sel_piece(self, state: State) -> tuple:
        while True:
            row = int(input('Row (1-8): ')) - 1
            col = ord(input('Col (A-H): ').lower()) - 97

            if self.valid_position((row, col)) and self.is_ally(state, (row, col)):
                return (row, col)

    def sel_direction(self) -> tuple:
        while True:
            dir = input('Direction (W|NW|N|NE|E): ').upper()

            if dir == 'W':
                return Direction.WEST
            elif dir == 'NW':
                return Direction.NORTHWEST
            elif dir == 'N':
                return Direction.NORTH
            elif dir == 'NE':
                return Direction.NORTHEAST
            elif dir == 'E':
                return Direction.EAST

    def sel_dropzone(self, state: State) -> State:
        row_c = 2 if (state.player == 2) else 8
        if self.is_dropzone_full(state, row_c - 1):
            print('full ' + str(row_c))
            return state

        print(Fore.GREEN + 'Player ' + str(state.player) + " place a new piece!")
        print(Style.RESET_ALL, end="")

        while True:
            row = int(input('Row (1-8): ')) - 1
            col = ord(input('Col (A-H): ').lower()) - 97
            pos = (row, col)

            if col in range(1, 8) and row in range(row_c - 2, row_c) and self.is_empty(state, pos):
                self.place_piece(state, pos, state.player)
                state.print()
                return state

    def is_dropzone_full(self, state: State, row: int) -> bool:
        return not (0 in state.board[row][1:6] or 0 in state.board[row - 1][1:6])
    
    def jump_combo1(self, state: State, pos: tuple, vec: tuple) -> State:
        n_state = self.jump(state, pos, vec)
        n_state.print()
        
        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir * 2))

        if self.in_last_row(n_pos):
            return state

        print(Fore.GREEN + 'Player ' + str(state.player) + " keep jumping!")
        print(Style.RESET_ALL, end="")

        if not (self.can_jump(state, pos, Direction.NORTHWEST) or
                self.can_jump(state, pos, Direction.NORTH) or
                self.can_jump(state, pos, Direction.NORTHEAST)):
            n_state.moves -= 1
            return n_state
        
        dir = self.sel_direction()
        while not self.can_jump(n_state, n_pos, dir):
            dir = self.sel_direction()

        return self.jump_combo(n_state, n_pos, dir)

    def capture_combo(self, state: State, pos: tuple, vec: tuple) -> State:
        n_state = self.capture(state, pos, vec)
        n_state.print()

        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir * 2))

        if self.in_last_row(n_pos):
            return state

        print(Fore.GREEN + 'Player ' + str(state.player) + " keep capturing!")
        print(Style.RESET_ALL, end="")

        if not (self.can_capture(state, pos, Direction.WEST) or 
                self.can_capture(state, pos, Direction.NORTHWEST) or 
                self.can_capture(state, pos, Direction.NORTH) or 
                self.can_capture(state, pos, Direction.NORTHEAST) or
                self.can_capture(state, pos, Direction.EAST)):
            n_state.moves -= 1
            return n_state
        
        dir = self.sel_direction()
        while not self.can_capture(n_state, n_pos, dir):
            dir = self.sel_direction()

        return self.capture_combo(n_state, n_pos, dir)

    def in_last_row(self, pos: tuple) -> bool:
        return pos[0] == 0 or pos[0] == 7

    def last_row(self, state: State) -> bool:
        row = 0 if state.player == 1 else 7
        for col in range(len(state.board[row])):
            if self.is_ally(state, (row, col)):
                return True
        return False

    def remove_last_row(self, state: State) -> State:
        row = 0 if (state.player == 1) else 7
        n_state = copy(state)
        for col in range(len(state.board[row])):
            if self.is_ally(state, (row, col)):
                n_state.moves += 2
                self.remove_piece(n_state, (row, col))
                return n_state
        return state

    def check_capture(self, state: State) -> list:
        ret = []
        for row in range(len(state.board)):
            for col in range(len(state.board[row])):
                if not self.is_ally(state, (row, col)):
                    continue

                if (self.can_capture(state, (row, col), Direction.WEST) or 
                    self.can_capture(state, (row, col), Direction.NORTHWEST) or 
                    self.can_capture(state, (row, col), Direction.NORTH) or 
                    self.can_capture(state, (row, col), Direction.NORTHEAST) or 
                    self.can_capture(state, (row, col), Direction.EAST)):
                    ret.append((row, col))
        return ret
    
    def get_piece(self, state: State, pos: tuple) -> int:
        return state.board[pos[0]][pos[1]]

    def place_piece(self, state: State, pos: tuple, piece: int) -> None:
        state.board[pos[0]][pos[1]] = piece
    
    def remove_piece(self, state: State, pos: tuple) -> None:
        player = self.get_piece(state, pos)
        self.place_piece(state, pos, 0)
        state.score[player] -= 1

    def is_empty(self, state: State, pos: tuple) -> bool:
        return self.get_piece(state, pos) == 0
    
    # True if the piece on the position belongs to the player that is making the move
    def is_ally(self, state: State, pos: tuple) -> bool:
        return self.get_piece(state, pos) == state.player
    
    def is_enemy(self, state: State, pos: tuple) -> bool:
        return not self.is_empty(state, pos) and not self.is_ally(state, pos)

    # returns the movement direction multiplier 
    def get_direction(self, state: State) -> int:
        return 1 if state.player == 2 else -1
    
    def valid_position(self, pos: tuple) -> bool:
        return pos[0] in range(0, 8) and pos[1] in range(0, 8)

    # ORDINARY MOVE OPERATORS
    def can_move(self, state: State, pos: tuple, vec: tuple) -> bool:
        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def move(self, state: State, pos: tuple, vec: tuple) -> State:
        if state.action.type != "start":
            return None
        
        if not self.is_ally(state, pos):
            return None
        
        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir))

        if not self.valid_position(n_pos):
            return None
        if not self.is_empty(state, n_pos):
            return None
        
        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.place_piece(n_state, n_pos, state.player)

        # TODO: check if the player has reached the end row

        self.change_player(n_state)

        return n_state

    def move_north(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, 0))
    def move_north_east(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, -1))
    def move_north_west(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, 1))

    # JUMP MOVE OPERATORS
    def can_jump(self, state: State, pos: tuple, vec: tuple) -> bool:
        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_ally(state, t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def jump_start(self, state: State, pos: tuple, vec: tuple) -> State:
        if state.action.type != "start":
            return None
        
        if not self.is_ally(state, pos):
            return None

        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_ally(state, t_pos):
            return state
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return state

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)

        # TODO: check if the piece (n_pos) has reached the enemy's end row

        self.place_piece(n_state, n_pos, state.player)

        # TODO: check if the piece still has possible moves
        

        n_state.action = Jump(n_pos)
        
        return n_state

    def jump_combo(self, state: State, vec: tuple) -> State:
        if state.action.type != "jump":
            print(state.action.type)
            return None
        
        dir = self.get_direction(state)
        pos = state.action.pos

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_ally(state, t_pos):
            return None
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return None

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)

        # TODO: check if the piece (n_pos) has reached the enemy's end row

        self.place_piece(n_state, n_pos, state.player)

        # TODO: check if the piece still has possible moves

        n_state.action = Jump(n_pos)
        
        return n_state

    def jump_north(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, 0))
    def jump_north_east(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, -1))
    def jump_north_west(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, 1))

    # CAPTURE OPERATORS
    def can_capture(self, state: State, pos: tuple, vec: tuple) -> bool:
        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_enemy(state, t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def capture_start(self, state: State, pos: tuple, vec: tuple) -> State:
        if state.action.type != "start":
            return None

        if not self.is_ally(state, pos):
            return None
        
        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_enemy(state, t_pos):
            return None
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return None

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.remove_piece(n_state, t_pos)

        # TODO: check if the piece (n_pos) has reached the enemy's end row

        self.place_piece(n_state, n_pos, state.player)

        # TODO: check if the piece still has possible moves

        return n_state

    def capture_combo(self, state: State, vec: tuple) -> State:
        
        if state.action.type != "capture":
            return None

        dir = self.get_direction(state)
        pos = state.action.pos

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_enemy(state, t_pos):
            return state
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return state

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)

        # TODO: check if the piece (n_pos) has reached the enemy's end row

        self.remove_piece(n_state, t_pos)
        self.place_piece(n_state, n_pos, state.player)
        
        # TODO: check if the piece still has possible moves
        
        return n_state

    def capture_north(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (1, 0))
    def capture_east(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (0, -1))
    def capture_north_east(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (1, -1))
    def capture_west(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (0, 1))
    def capture_north_west(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (1, 1))

    def place(self, state: State, pos: tuple) -> State:
        if state.action.type != "place":
            return None

        row = 2 if state.player == 2 else 8
        if  pos[1] not in range(1, 8) or pos[0] not in range(row - 2, row) or not state.is_empty(state, pos):
            return None

        n_state = copy(state)
        self.place_piece(n_state, pos, n_state.player)
        n_state.action.pieces -= 1
        
        if n_state.action.pieces == 0:
            n_state.action = Start()
            self.change_player(n_state)
        
        return n_state
