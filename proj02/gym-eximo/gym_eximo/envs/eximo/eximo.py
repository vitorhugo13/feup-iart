from colorama import Fore, Back, Style 
from copy import copy

from state import State, start_state
from utils import Direction


#main game class
class Eximo:
    prv_player = 2

    #game builder who receives the necessary information about each player
    def __init__(self, p1: list, p2: list):
        self.player = {}
        self.player[1] = p1
        self.player[2] = p2
        self.state = start_state


    #funtion that checks if the game reachs the end and prints the winner
    def game_over(self, state: State) -> bool:
        if state.score[1] <= 0:
            state.print()
            print("Player 2 won!")
            return True
        elif state.score[2] <= 0:
            state.print()
            print("Player 1 won!")
            return True
        elif self.prv_player == state.player:
            state.print()
            print('Player ' + str(state.player) + ' has ran out of moves...')
            print('Player ' + str(state.player % 2 + 1) + ' won!')
            return True
        return False

    #function responsible for the beginning of the game and that contains the cycle that allows the game to continue until reaching a final state
    def play(self):
        self.prv_player = self.state.player % 2 + 1

        while not self.game_over(state):
            self.state.print()

            self.prv_player = self.state.player

            if self.player[self.state.player][0] == 'P':
                self.state = self.player_move(self.state)

    #verification of the selected piece
    @staticmethod
    def sel_cell() -> tuple:
        while True:
            
            row_number = input('Row (1-8): ')
            while len(row_number) > 1 or len(row_number) == 0:
                row_number = input('Row (1-8): ') 
            row = ord(row_number) - 49

            col_number = input('Col (A-H): ').lower()
            while len(col_number) > 1 or len(col_number) == 0:
                col_number = input('Col (A-H): ').lower()
            col = ord(col_number) - 97

            if State.valid_position((row, col)):
                return (row, col)

    #allows you to choose the capture direction
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

    #allows you to choose the move/jump direction
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

    #function that performs the move through the piece and the direction
    @staticmethod
    def player_move(state) -> State:
        n_state = None
        while n_state == None:
            
            # start mode
            if state.action[0] == 1:
                pos = Eximo.sel_cell()
                if not state.is_ally(pos):
                    continue

                if state.check_capture():
                    vec = Eximo.sel_cp_dir()
                    n_state = state.capture(pos, vec)
                else:
                    vec = Eximo.sel_mv_dir()
                    n_state = state.move(pos, vec) or state.jump(pos, vec)

            # jump mode
            elif state.action[0] == 2:
                pos = state.action[1]
                vec = Eximo.sel_mv_dir()
                n_state = state.jump(pos, vec)

            # capture mode
            elif state.action[0] == 3:
                pos = state.action[1]
                vec = Eximo.sel_cp_dir()
                n_state = state.capture(pos, vec)

            # place mode
            elif state.action[0] == 4:
                pos = Eximo.sel_cell()

                row = 2 if state.player == 2 else 8
                if pos[1] not in range(1, 8) or pos[0] not in range(row - 2, row) or not state.is_empty(pos):
                    continue

                n_state = state.place(pos)

        return n_state
