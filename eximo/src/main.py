from eximo import Eximo
from eval import *
import signal
import sys

TGREEN =  '\033[32m' # Green Text
TRED =  '\033[31m' # Green Text

ENDC = '\033[m' # reset to the defaults

def signal_handler(sig, frame):
    # print('\n')
    print('Exiting game. Hope to see you soon!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# interface functions

def print_main_menu():
    print('----------------------------------------------')
    print('|                                            |')
    print('|' + '                ' + TGREEN +'    EXIMO                  ', ENDC +'|')
    print('|                                            |')
    print('|' + '              ' + TRED +'Choose a game mode:          ', ENDC+'|')
    print('|                                            |')
    print('|                                            |')
    print('|' + '             ' + TGREEN+'1)',ENDC+'Player vs Player            '+'|')
    print('|' + '             ' + TGREEN+'2)',ENDC+'Player vs Computer          '+'|')
    print('|' + '             ' + TGREEN+'3)',ENDC+'Computer vs Player          '+'|')
    print('|' + '             ' + TGREEN+'4)',ENDC+'Computer vs Computer        '+'|')
    print('|                                            |')
    print('|' + '             ' + TGREEN+'0)',ENDC+'Exit                        '+'|')
    print('|                                            |')
    print('|                                            |')
    print('----------------------------------------------', end="")

def print_heuristic_menu(player):
    print('----------------------------------------------')
    print('|                                            |')
    print('|                                            |')
    print('|' + '                ' + TGREEN + '    EXIMO                  ', ENDC + '|')
    print('|' + '         ' + TRED + 'Choose computer ' + str(player) + '\'s heuristic:    ', ENDC + '|')
    print('|                                            |')
    print('|                                            |')
    print('|' + '             ' + TGREEN + '1)', ENDC + 'Centralized                 ' + '|')
    print('|' + '             ' + TGREEN + '2)', ENDC + 'Decentralized               ' + '|')
    print('|' + '             ' + TGREEN + '3)', ENDC + 'Subtraction                 ' + '|')
    print('|' + '             ' + TGREEN + '4)', ENDC + 'Number of pieces            ' + '|')
    print('|                                            |')
    print('|                                            |')
    print('|                                            |')
    print('----------------------------------------------', end="")


def game_mode():
    while True:
        mode = input(TRED +'Game Mode: '+ ENDC)

        while len(mode) > 1 or len(mode) == 0:
            mode = input(TRED +'Game Mode: '+ ENDC)

        game_mode = ord(mode) - 48

        if game_mode in range(0, 5):
            return game_mode

def computer_level(player):
    while True:
        level = input(TRED +'Computer level [player ' + str(player) + '] (> 0): '+ ENDC)

        while len(level) > 1 or len(level) == 0:
            level = input(TRED +'Computer level [player ' + str(player) + '] (> 0): '+ ENDC)

        computer_level = ord(level) - 48

        if computer_level in range(0, 10):
            return computer_level

def sel_heuristic(player):
    while True:
        print_heuristic_menu(player)
        print()

        h = input(TRED +'Computer ' + str(player) + '\'s heuristic : '+ ENDC)

        if len(h) == 0 or len(h) > 1: continue

        h = ord(h) - 48
        
        if not h in range(0, 6): continue

        if h == 1:
            return center
        elif h == 2:
            return side
        elif h == 3:
            return subtraction
        elif h == 4:
            return num_pieces

def main_menu():
    player = {}

    while True:
        player[1] = ['P', 0, None]
        player[2] = ['P', 0, None]

        print_main_menu()
        print('\n')

        game = game_mode()

        if game == 2:
            h = sel_heuristic(2)
            level = computer_level(2)
            
            player[2][0] = 'C'
            player[2][1] = level
            player[2][2] = h

        elif game == 3:
            h = sel_heuristic(1)
            level = computer_level(1)
            
            player[1][0] = 'C'
            player[1][1] = level
            player[1][2] = h
            
        elif game == 4:
            h = sel_heuristic(1)
            level = computer_level(1)
            
            player[1][0] = 'C'
            player[1][1] = level
            player[1][2] = h

            h = sel_heuristic(2)
            level = computer_level(2)
            
            player[2][0] = 'C'
            player[2][1] = level
            player[2][2] = h

        elif game == 0:
            print(TGREEN + 'Thank you for playing.', ENDC)
            sys.exit()

        game = Eximo(player[1], player[2])
        game.play()


main_menu()


