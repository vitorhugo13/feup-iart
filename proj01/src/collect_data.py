from eximo import *


file = open("data.csv", "w")

file.write('Player,Depth,Heuristic,Total Plays,Total Time,Total Leaves,Total Cuts,Won\n')

for depth_p1 in range(1, 5):
    for depth_p2 in range(1, 5):
        for h_p1 in [subtraction, num_pieces, side, center]:
            for h_p2 in [subtraction, num_pieces, side, center]:
                
                game = Eximo(['C', depth_p1, h_p1], ['C', depth_p2, h_p2])
                game.statistics(file)

file.close()
