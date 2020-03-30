from eximo import Eximo
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

def print_level_menu():
    print('----------------------------------------------')
    print('|                                            |')
    print('|                                            |')
    print('|' + '                ' + TGREEN + '    EXIMO                  ', ENDC + '|')
    print('|' + '          ' + TRED + 'Choose the computer level:       ', ENDC + '|')
    print('|                                            |')
    print('|                                            |')
    print('|                                            |')
    print('|' + '             '+ TGREEN+'1)',ENDC + 'Easy                        ' + '|')
    print('|' + '             '+ TGREEN+'2)',ENDC + 'Hard                        ' + '|')
    print('|                                            |')
    print('|' + '             '+ TGREEN+'0)',ENDC + 'Return to main menu         ' + '|')
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
        print_level_menu()
        print('\n')

        level = input(TRED +'Computer level [player ' + str(player) + ']: '+ ENDC)

        while len(level) > 1 or len(level) == 0:
            level = input(TRED +'Computer level [player ' + str(player) + ']: '+ ENDC)

        computer_level = ord(level) - 48

        if computer_level in range(0, 3):
            return computer_level

def main_menu():
    player = {}

    while True:
        player[1] = 'P'
        player[2] = 'P'

        print_main_menu()
        print('\n')

        game = game_mode()

        if game == 2:
            level = computer_level(2)
            if level == 0: continue
            player[2] = 'C' + str(level)
        elif game == 3:
            level = computer_level(1)
            if level == 0: continue
            player[1] = 'C' + str(level)
        elif game == 4:
            level1 = computer_level(1)
            if level1 == 0: continue
            level2 = computer_level(2)
            if level2 == 0: continue
            player[1] = 'C' + str(level1)
            player[2] = 'C' + str(level2)
        elif game == 0:
            print(TGREEN + 'Thank you for playing.', ENDC)
            sys.exit()

        game = Eximo(player[1], player[2])
        game.play()


main_menu()


