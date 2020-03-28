from colorama import Fore, Back, Style 
from copy import copy

from state import State, start_state
from aux import Direction
import sys


class Eximo:
    def __init__(self, p1: str, p2: str):
        self.player = {}
        self.player[1] = p1
        self.player[2] = p2

    def play(self):
        state = start_state
        while not state.game_over():
            state.print()

            if self.player[state.player] == 'P':
                state = self.player_move(state)
            else:
                print("------- MINIMAX START --------")
                state = self.minimax(state, 3, state.player, True)
                print("------- MINIMAX END --------")

    @staticmethod
    def sel_cell() -> tuple:
        while True:
            row = int(input('Row (1-8): ')) - 1
            col = ord(input('Col (A-H): ').lower()) - 97

            if State.valid_position((row, col)):
                return (row, col)

    @staticmethod
    def sel_cp_dir() -> tuple:
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

    @staticmethod
    def sel_mv_dir() -> tuple:
        while True:
            dir = input('Direction (NW|N|NE): ').upper()
            if dir == 'NW':
                return Direction.NORTHWEST
            elif dir == 'N':
                return Direction.NORTH
            elif dir == 'NE':
                return Direction.NORTHEAST

    @staticmethod
    def player_move(state) -> State:
        n_state = None
        while n_state == None:

            if state.action.type == "start":
                pos = Eximo.sel_cell()
                if state.check_capture():
                    vec = Eximo.sel_cp_dir()
                    n_state = state.capture(pos, vec)
                else:
                    vec = Eximo.sel_mv_dir()
                    n_state = state.move(pos, vec) or state.jump(pos, vec)

            elif state.action.type == "jump":
                pos = state.action.pos
                vec = Eximo.sel_mv_dir()
                n_state = state.jump(pos, vec)

            elif state.action.type == "capture":
                pos = state.action.pos
                vec = Eximo.sel_cp_dir()
                n_state = state.capture(pos, vec)

            elif state.action.type == "place":
                pos = Eximo.sel_cell()
                n_state = state.place(pos)

        return n_state

    @staticmethod
    def minimax(state: State, depth: int, max_player: int, root: bool) -> State:
        
        if depth == 0: # or no more possible moves
            return state
        children = state.get_children()
        if len(children) == 0:
            return state

        if state.player == max_player:
            max_score = -1
            max_index = -1
            max_state = state
            

            for i, child in enumerate(children):
                n_state = Eximo.minimax(child, depth - 1, max_player, False)
                if n_state.score[max_player] > max_score:
                    max_score = n_state.score[max_player]
                    max_state = n_state
                    max_index = i
            if not root:
                return max_state
            else:
                return children[max_index]
        
        else:
            min_score = sys.maxsize
            min_state = state
            min_index = -1

            for i, child in enumerate(children):
                n_state = Eximo.minimax(child, depth - 1, max_player, False)
                if n_state.score[max_player] < min_score:
                    min_score = n_state.score[max_player]
                    min_state = n_state
                    min_index = i
            if not root:
                return min_state
            else:
                return children[min_index]
