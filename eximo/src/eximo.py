from colorama import Fore, Back, Style 
from copy import copy

from state import *
from aux import *


class Eximo:
    start_state = State([
        [0, 2, 2, 2, 2, 2, 2, 0],
        [0, 2, 2, 2, 2, 2, 2, 0], 
        [0, 2, 2, 0, 0, 2, 2, 0], 
        [0, 0, 1, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 1, 1, 1, 1, 1, 0], 
        [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, 1)
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
            pieces = self.check_last_row(state)
            while pieces > 0:
                state = self.sel_dropzone(state)
                pieces -= 1
            state = self.change_player(state)
                
    def change_player(self, state: State) -> State:
        if state.moves > 0:
            return state
        state.moves = 1
        state.player = state.player % 2 + 1
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
        # TODO: check if the player needs to capture enemy pieces

        while True:
            pos = self.sel_piece(state)
            dir = self.sel_direction()
            
            if self.can_move(state, pos, dir):
                return self.move(state, pos, dir)
            elif self.can_jump(state, pos, dir):
                return self.jump_combo(state, pos, dir)
            elif self.can_capture(state, pos, dir):
                return self.capture_combo(state, pos, dir)
    
    def sel_piece(self, state: State) -> tuple:
        while True:
            row = int(input('Row (1-8): '))
            col = ord(input('Col (A-H): ').lower()) - 97

            if self.valid_position((row, col)) and self.is_players(state, (row, col)):
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
        row_c = 2 if (state.player == 1) else 7
        while True:
            row = int(input('Row (1-8): '))
            col = ord(input('Col (A-H): ').lower()) - 97
            pos = (row, col)

            if (pos >= (row_c, 1) and pos <= (row_c, 6)) or (pos >= (row_c - 1, 1) and pos <= (row_c - 1, 6)) and self.is_empty(state, pos):
                return self.place_piece(state, pos, state.player)

    
    def jump_combo(self, state: State, pos: tuple, vec: tuple) -> State:
        n_state = self.jump(state, pos, vec)
        n_state.print()
            
        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir * 2))

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

    # checks if the player has any piece in the last row, removes 
    # those pieces and returns the number of pieces removed
    def check_last_row(self, state: State) -> int:
        ret = 0
        row = 0 if (state.player == 1) else 7
        for col in range(len(state.board[row])):
            if state.player == state.board[row][col]:
                self.remove_piece(state, (row, col))
                ret += 1
        state.moves += ret
        return ret  

    def check_capture(self, state: State) -> bool:
        for row in range(len(state.board)):
            for col in range(len(state.board[row])):
                if not self.is_players(state, (row, col)):
                    continue

                if self.can_capture(state, (row, col), Direction.WEST) or self.can_capture(state, (row, col), Direction.NORTHWEST) or self.can_capture(state, (row, col), Direction.NORTH) or self.can_capture(state, (row, col), Direction.NORTHEAST) or self.can_capture(state, (row, col), Direction.EAST):
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
    def is_players(self, state: State, pos: tuple) -> bool:
        return self.get_piece(state, pos) == state.player
    
    def is_opponents(self, state: State, pos: tuple) -> bool:
        return not self.is_empty(state, pos) and not self.is_players(state, pos)

    # returns the movement direction multiplier 
    def get_direction(self, state: State) -> int:
        if state.player == 2:
            return 1
        return -1
    
    def valid_position(self, pos: tuple) -> bool:
        return pos[0] >= 0 and pos[0] <= 7 and pos[1] >= 0 and pos[1] <= 7


    # ORDINARY MOVE OPERATORS
    def can_move(self, state: State, pos: tuple, vec: tuple) -> bool:
        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir))
        print(n_pos)
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def move(self, state: State, pos: tuple, vec: tuple) -> State:
        if not self.is_players(state, pos):
            return state
        
        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir))

        if not self.valid_position(n_pos):
            return state
        if not self.is_empty(state, n_pos):
            return state
        
        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.place_piece(n_state, n_pos, state.player)
        n_state.moves -= 1

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
        if not self.valid_position(t_pos) or not self.is_players(state, t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def jump(self, state: State, pos: tuple, vec: tuple) -> State:
        if not self.is_players(state, pos):
            return state

        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_players(state, t_pos):
            return state
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return state

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.place_piece(n_state, n_pos, state.player)
        
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
        if not self.valid_position(t_pos) or not self.is_opponents(state, t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return False
        
        return True

    def capture(self, state: State, pos: tuple, vec: tuple) -> State:
        # if not self.is_players(state, pos):
        #     return state

        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_opponents(state, t_pos):
            return state
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return state

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.remove_piece(n_state, t_pos)
        self.place_piece(n_state, n_pos, state.player)
        
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

