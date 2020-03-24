from eximo import Eximo


# game = Eximo('P', 'P')
# print(game.sel_piece(game.start_state))
# game.play()
# print(game.sel_direction())
# print(game.can_move(game.start_state, (5, 2), (1, 0)))
# print(game.is_dropzone_full(game.start_state, 1))


# test operators
game = Eximo('P', 'P')
state = game.move(game.start_state, (5, 1), (1,0))
if (state != None): state.print()