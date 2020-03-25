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
            state = self.player_move(state)

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
            
    def sel_cell(self) -> tuple:
        while True:
            row = int(input('Row (1-8): ')) - 1
            col = ord(input('Col (A-H): ').lower()) - 97

            if self.valid_position((row, col)):
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

    def is_dropzone_full(self, state: State) -> bool:
        row = 1 if (state.player == 2) else 7
        return not (0 in state.board[row][1:6] or 0 in state.board[row - 1][1:6])

    def in_last_row(self, state, pos: tuple) -> bool:
        return (state.player == 1 and pos[0] == 0) or (state.player == 2 and pos[0] == 7)

    def check_capture(self, state: State) -> bool:
        dir = self.get_direction(state)
        for row in range(len(state.board)):
            for col in range(len(state.board[row])):
                if not self.is_ally(state, (row, col)):
                    continue

                if (self.can_capture(state, dir, (row, col), Direction.WEST) or 
                    self.can_capture(state, dir, (row, col), Direction.NORTHWEST) or 
                    self.can_capture(state, dir, (row, col), Direction.NORTH) or 
                    self.can_capture(state, dir, (row, col), Direction.NORTHEAST) or 
                    self.can_capture(state, dir, (row, col), Direction.EAST)):
                    return True
        return False
    
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

        if self.in_last_row(state, n_pos):
            self.enter_place_mode(n_state)
        else:
            self.place_piece(n_state, n_pos, state.player)
            self.change_player(n_state)

        return n_state


    # JUMP MOVE OPERATORS
    def can_jump(self, state: State, dir: int, pos: tuple, vec: tuple) -> bool:
        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_ally(state, t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def jump(self, state: State, pos: tuple, vec: tuple) -> State:
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

        if self.in_last_row(state, n_pos):
            self.enter_place_mode(n_state)
        else:
            self.place_piece(n_state, n_pos, state.player)
            if  not (self.can_jump(n_state, dir, n_pos, Direction.NORTHWEST) or 
                self.can_jump(n_state, dir, n_pos, Direction.NORTH) or 
                self.can_jump(n_state, dir, n_pos, Direction.NORTHEAST)):
                self.change_player(n_state)
            else:
                n_state.action = Jump(n_pos)

        return n_state

    # CAPTURE OPERATORS
    def can_capture(self, state: State, dir: int, pos: tuple, vec: tuple) -> bool:
        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_enemy(state, t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def capture(self, state: State, pos: tuple, vec: tuple) -> State:
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

        if self.in_last_row(state, n_pos):
            self.enter_place_mode(n_state)
        else:
            self.place_piece(n_state, n_pos, state.player)
            if  not (self.can_capture(n_state, dir, n_pos, Direction.WEST) or 
                self.can_capture(n_state, dir, n_pos, Direction.NORTHWEST) or 
                self.can_capture(n_state, dir, n_pos, Direction.NORTH) or 
                self.can_capture(n_state, dir, n_pos, Direction.NORTHEAST) or 
                self.can_capture(n_state, dir, n_pos, Direction.EAST)):
                self.change_player(n_state)
            else:
                n_state.action = Capture(n_pos)
        
        return n_state

    def place(self, state: State, pos: tuple) -> State:
        row = 2 if state.player == 2 else 8
        if  pos[1] not in range(1, 8) or pos[0] not in range(row - 2, row) or not self.is_empty(state, pos):
            return None

        n_state = copy(state)
        self.place_piece(n_state, pos, n_state.player)
        n_state.action.pieces -= 1
        
        if n_state.action.pieces == 0:
            self.change_player(n_state)
        
        return n_state

    def enter_place_mode(self, state: State) -> None:
        row = 1 if (state.player == 2) else 7
        available = state.board[row][1:6].count(0) + state.board[row - 1][1:6].count(0)
        
        if available > 1:
            state.action = Place(2)
        elif available > 0:
            state.action = Place(1)
        else:
            self.change_player(state)

    def player_move(self, state: State) -> State:
        n_state = None
        while n_state == None:

            if state.action.type == "start":
                pos = self.sel_cell()
                vec = self.sel_direction()
                if self.check_capture(state):
                    n_state = self.capture(state, pos, vec)
                else:
                    n_state = self.move(state, pos, vec) or self.jump(state, pos, vec)

            elif state.action.type == "jump":
                pos = state.action.pos
                vec = self.sel_direction()
                n_state = self.jump(state, pos, vec)

            elif state.action.type == "capture":
                pos = state.action.pos
                vec = self.sel_direction()
                n_state = self.capture(state, pos, vec)

            elif state.action.type == "place":
                pos = self.sel_cell()
                n_state = self.place(state, pos)

        return n_state

    def move_north(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, 0))
    def move_north_east(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, -1))
    def move_north_west(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, 1))


    def jump_north(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, 0))
    def jump_north_east(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, -1))
    def jump_north_west(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, 1))


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
