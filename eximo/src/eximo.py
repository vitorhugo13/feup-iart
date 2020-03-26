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

            if self.player[state.player] == 'P':
                state = self.player_move(state)
            else:
                print("------- MINIMAX START --------")
                state = self.minimax(state, 3, state.player)
                print("------- MINIMAX END --------")

    def game_over(self, state: State) -> bool:
        if state.score[1] <= 0:
            print("player 2 won")
            return True
        elif state.score[2] <= 0:
            print("player 1 won")
            return True
        return False
            
    def sel_cell(self) -> tuple:
        while True:
            row = int(input('Row (1-8): ')) - 1
            col = ord(input('Col (A-H): ').lower()) - 97

            if self.valid_position((row, col)):
                return (row, col)

    def sel_cp_dir(self) -> tuple:
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

    def sel_mv_dir(self) -> tuple:
        while True:
            dir = input('Direction (NW|N|NE): ').upper()
            if dir == 'NW':
                return Direction.NORTHWEST
            elif dir == 'N':
                return Direction.NORTH
            elif dir == 'NE':
                return Direction.NORTHEAST

    def in_last_row(self, state, pos: tuple) -> bool:
        return (state.player == 1 and pos[0] == 0) or (state.player == 2 and pos[0] == 7)

    def check_capture(self, state: State) -> bool:
        dir = state.move_direction()
        for row in range(len(state.board)):
            for col in range(len(state.board[row])):
                if not state.is_ally((row, col)):
                    continue

                if (self.can_capture(state, dir, (row, col), Direction.WEST) or 
                    self.can_capture(state, dir, (row, col), Direction.NORTHWEST) or 
                    self.can_capture(state, dir, (row, col), Direction.NORTH) or 
                    self.can_capture(state, dir, (row, col), Direction.NORTHEAST) or 
                    self.can_capture(state, dir, (row, col), Direction.EAST)):
                    return True
        return False
    
    def valid_position(self, pos: tuple) -> bool:
        return pos[0] in range(0, 8) and pos[1] in range(0, 8)

    # ORDINARY MOVE OPERATORS
    def move(self, state: State, pos: tuple, vec: tuple) -> State:
        if not state.is_ally(pos):
            return None
        
        dir = state.move_direction()
        n_pos = add(pos, mult(vec, dir))

        if not self.valid_position(n_pos):
            return None
        if not state.is_empty(n_pos):
            return None
        
        n_state = state.copy()
        n_state.remove_piece(pos)

        if self.in_last_row(state, n_pos):
            self.enter_place_mode(n_state)
        else:
            n_state.place_piece(n_pos, state.player)
            n_state.next_turn()

        return n_state


    # JUMP MOVE OPERATORS
    def can_jump(self, state: State, dir: int, pos: tuple, vec: tuple) -> bool:
        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not state.is_ally(t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not state.is_empty(n_pos):
            return False
        
        return True

    def jump(self, state: State, pos: tuple, vec: tuple) -> State:
        if not state.is_ally(pos):
            return None

        dir = state.move_direction()

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not state.is_ally(t_pos):
            return None
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not state.is_empty(n_pos):
            return None

        n_state = state.copy()
        n_state.remove_piece(pos)

        if self.in_last_row(state, n_pos):
            self.enter_place_mode(n_state)
        else:
            n_state.place_piece(n_pos, state.player)
            if  not (self.can_jump(n_state, dir, n_pos, Direction.NORTHWEST) or 
                self.can_jump(n_state, dir, n_pos, Direction.NORTH) or 
                self.can_jump(n_state, dir, n_pos, Direction.NORTHEAST)):
                n_state.next_turn()
            else:
                n_state.action = Jump(n_pos)

        return n_state

    # CAPTURE OPERATORS
    def can_capture(self, state: State, dir: int, pos: tuple, vec: tuple) -> bool:
        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not state.is_enemy(t_pos):
            return False
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not state.is_empty(n_pos):
            return False
        
        return True

    def capture(self, state: State, pos: tuple, vec: tuple) -> State:
        if not state.is_ally(pos):
            return None
        
        dir = state.move_direction()

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not state.is_enemy(t_pos):
            return None
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not state.is_empty(n_pos):
            return None

        n_state = state.copy()
        n_state.remove_piece(pos)
        n_state.remove_piece(t_pos)

        if self.in_last_row(state, n_pos):
            self.enter_place_mode(n_state)
        else:
            n_state.place_piece(n_pos, state.player)
            if not (self.can_capture(n_state, dir, n_pos, Direction.WEST) or 
                self.can_capture(n_state, dir, n_pos, Direction.NORTHWEST) or 
                self.can_capture(n_state, dir, n_pos, Direction.NORTH) or 
                self.can_capture(n_state, dir, n_pos, Direction.NORTHEAST) or 
                self.can_capture(n_state, dir, n_pos, Direction.EAST)):
                n_state.next_turn()
            else:
                n_state.action = Capture(n_pos)
        
        return n_state

    def place(self, state: State, pos: tuple) -> State:
        row = 2 if state.player == 2 else 8
        if  pos[1] not in range(1, 8) or pos[0] not in range(row - 2, row) or not state.is_empty(pos):
            return None

        n_state = state.copy()
        n_state.place_piece(pos, n_state.player)
        n_state.action.pieces -= 1
        
        if n_state.action.pieces == 0:
            n_state.next_turn()
        
        return n_state

    def enter_place_mode(self, state: State) -> None:
        row = 1 if (state.player == 2) else 7
        available = state.board[row][1:6].count(0) + state.board[row - 1][1:6].count(0)
        
        if available > 1:
            state.action = Place(2)
        elif available > 0:
            state.action = Place(1)
        else:
            state.next_turn()

    def player_move(self, state: State) -> State:
        n_state = None
        while n_state == None:

            if state.action.type == "start":
                pos = self.sel_cell()
                if self.check_capture(state):
                    vec = self.sel_cp_dir()
                    n_state = self.capture(state, pos, vec)
                else:
                    vec = self.sel_mv_dir()
                    n_state = self.move(state, pos, vec) or self.jump(state, pos, vec)

            elif state.action.type == "jump":
                pos = state.action.pos
                vec = self.sel_mv_dir()
                n_state = self.jump(state, pos, vec)

            elif state.action.type == "capture":
                pos = state.action.pos
                vec = self.sel_cp_dir()
                n_state = self.capture(state, pos, vec)

            elif state.action.type == "place":
                pos = self.sel_cell()
                n_state = self.place(state, pos)

        return n_state

    def get_children(self, state: State) -> list:

        ret_states = []

        if state.action.type == "start":
            # TODO: check if any piece can capture
            # TODO: if no piece can capture then try jumps and moves for each piece on the board

            regular_arr = []

            for row in range(0,8): 
                for col in range(0,8):
                    pos = (row, col)

                    for vec in [Direction.WEST, Direction.EAST]:
                        n_state = self.capture(state, pos, vec)
                        if n_state != None: ret_states.append(n_state)

                    for vec in [Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST]:
                        n_state = self.capture(state, pos, vec)
                        if n_state != None: ret_states.append(n_state)

                        if ret_states: continue
                        
                        n_state = self.move(state, pos, vec) or self.jump(state, pos, vec)
                        if n_state != None: 
                            regular_arr.append(n_state)

            if not ret_states:
                # TODO: check if it is possible to assign
                ret_states.extend(regular_arr)

        elif state.action.type == "place":
            # TODO: generate all possible placing possibilities
            row_c = 0 if (state.player == 2) else 6

            for row in range(0, 2):
                for col in range(1, 7):
                    n_state = self.place(state, (row_c + row, col))
                    if n_state != None: ret_states.append(n_state)

        elif state.action.type == "capture":
            # TODO: check all the moves that the capturing piece can do
            for vec in [Direction.WEST, Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST, Direction.EAST]:
                n_state = self.capture(state, state.action.pos, vec)
                if n_state != None: ret_states.append(n_state)
            
        elif state.action.type == "jump":
            # TODO: check all the jumps that the jumping piece can do
            for vec in [Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST]:
                n_state = self.jump(state, state.action.pos, vec)
                if n_state != None: ret_states.append(n_state)

        # check if a r_state is a start action, if not get_children of that state until a start state          
        tmp_states = []
        for state in ret_states:
            if state.action.type == "start":
                continue
            
            tmp_states.extend(self.get_children(state))
            ret_states.remove(state)
            
        ret_states.extend(tmp_states)
        return ret_states

    # TODO: deal with the case when the player has no more moves
    def minimax(self, state: State, depth: int, max_player: int) -> State:
        if depth == 0: # or no more possible moves
            return state

        if state.player == max_player:
            max_score = -1
            max_state = state
            for child in self.get_children(state):
                n_state = self.minimax(child, depth - 1, max_player)
                if n_state.score[max_player] > max_score:
                    max_score = n_state.score[max_player]
                    max_state = n_state
            return max_state
        
        else:
            min_score = 65
            min_state = state
            for child in self.get_children(state):
                n_state = self.minimax(child, depth - 1, max_player)
                if n_state.score[max_player] < min_score:
                    min_score = n_state.score[max_player]
                    min_state = n_state
            return min_state
