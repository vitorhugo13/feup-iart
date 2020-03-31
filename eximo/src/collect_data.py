from eximo import *



for depth_p1 in range(2, 6):
    for depth_p2 in range(2, 6):
        for h_p1 in [subtraction, num_pieces, available_moves, side, center]:
            for h_p2 in [subtraction, num_pieces, available_moves, side, center]:
                
                # exclude special cases
                # if depth_p1 == 1 and depth_p2 == 1 and h_p1 == subtraction and h_p2 == subtraction:
                #     continue
                
                game = Eximo(['C', depth_p1, h_p1], ['C', depth_p2, h_p2])
                game.statistics('data.csv')