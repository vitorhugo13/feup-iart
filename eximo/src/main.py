from eximo import Eximo
import signal
import sys

TGREEN =  '\033[32m' # Green Text
TRED =  '\033[31m' # Green Text

ENDC = '\033[m' # reset to the defaults

def signal_handler(sig, frame):
    print('\n')
    print('Exiting game. Hope to see you soon!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def valid_game_mode(opt: int) -> bool:
        return opt in range(1, 6)

def print_horizontal():
    print('----------------------------------------------', end="")

def print_vertical():
    for i in range(15):
        if i == 2:
            print( '|' + '                ' + TGREEN +'    EXIMO                  ', ENDC +'|')
        elif i == 4:
            print('|' + '              ' + TRED +'Choose a game mode:          ', ENDC+'|')
        elif i == 7:
            print('|' + '             ' + TGREEN+'1)',ENDC+'Player vs Player            '+'|')
        elif i == 8:
            print('|' + '             '+ TGREEN+'2)',ENDC+'Player vs Computer          '+'|')
        elif i == 9:
            print('|' + '             '+ TGREEN+'3)',ENDC+'Computer vs Player          '+'|')
        elif i == 10:
            print('|' + '             '+ TGREEN+'4)',ENDC+'Computer vs Computer        '+'|')
        elif i == 12:
            print('|' + '             '+ TGREEN+'5)',ENDC+'Exit                        '+'|')
        else:
            print('|                                            |')

def game_mode():
    while True:
        mode = input(TRED +'Game Mode: '+ ENDC)

        while len(mode) > 1 or len(mode) == 0:
            mode = input(TRED +'Game Mode: '+ ENDC)

        game_mode = ord(mode) - 48

        if valid_game_mode(game_mode):
            return game_mode

def show_main_menu():
    print_horizontal()
    print()
    print_vertical()
    print_horizontal()
    print('\n')
    game = game_mode()
    print(game)

show_main_menu()
#game = Eximo('P', 'C')
#game.play()
