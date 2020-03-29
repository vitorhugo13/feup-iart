from eximo import Eximo
import signal
import sys

def signal_handler(sig, frame):
    print('\n')
    print('Exiting game. Hope to see you soon!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# game = Eximo('P', 'P')
# print(game.sel_piece(game.start_state))
# game.play()
# print(game.sel_direction())
# print(game.can_move(game.start_state, (5, 2), (1, 0)))
# print(game.is_dropzone_full(game.start_state, 1))

# test operators
game = Eximo('P', 'C')
game.play()
