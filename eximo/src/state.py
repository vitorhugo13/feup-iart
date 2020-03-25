from colorama import Fore, Back, Style 
from copy import copy

class State:
    score = {}

    def __init__(self, board, player, s1, s2, action):
        self.board = board
        self.player = player
        self.action = action 
        self.score[1] = s1
        self.score[2] = s2

    def copy(self):
        board = [row.copy() for row in self.board]
        player = self.player + 0
        action = self.action
        return State(board, player, self.score[1], self.score[2], action)

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

    def get_piece(self, pos: tuple) -> bool:
        return self.board[pos[0]][pos[1]]

    def is_empty(self, pos: tuple) -> bool:
        return self.get_piece(pos) == 0



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

