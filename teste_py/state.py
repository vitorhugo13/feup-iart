import pygame, sys

from eximo import *
# ----------------------  CONSTANTS --------------------------
WIDTH = 700
HEIGHT = 600
MARK_SIZE = 50

WOOD = [99, 70, 49]
WHITE   = [255, 255, 255]

class State:
    score = {}

    def __init__(self, board, player, s1, s2, moves):
        self.board = board
        self.player = player
        self.score[1] = s1
        self.score[2] = s2
        self.moves = moves


    def draw(self):
        for i in range(9):
            pygame.draw.line(screen, WHITE, [i * WIDTH / 8, 0], [i * WIDTH / 8, HEIGHT], 5)
            pygame.draw.line(screen, WHITE, [0, i * HEIGHT / 8], [WIDTH, i * HEIGHT / 8], 5)
        font = pygame.font.SysFont('Calibri', MARK_SIZE, False, False)
        for r in range(len(self.board)):
            print(r)


# pygame functions

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EXIMO")
screen.fill(WOOD)


pygame.display.flip()

done = False
clock = pygame.time.Clock()

while not done:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    

    # Limit to 60 frames per second
    clock.tick(60)


pygame.quit()