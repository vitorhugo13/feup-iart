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
        print('Moves left: ' + str(self.moves))


class Action:
    def __init__(self, type: str):
        self.type = type 

class Start(Action):
    def __init__(self):
        self = Action("start")

class Jump(Action):
    def __init__(self, pos: tuple):
        self = Action("jump")
        self.pos = pos
        
class Capture(Action):
    def __init__(self, pos: tuple):
        self = Action("capture")
        self.pos = pos

class Place(Action):
    def __init__(self, pieces_left):
        self = Action("place")
        self.pieces_left = pieces_left

