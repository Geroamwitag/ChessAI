import pygame
from board import Board

pygame.init()
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

board = Board()

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # draw board
    board.draw(screen)

    # cleanest way to draw the game every frame
    pygame.display.flip()

    # game fps
    clock.tick(60)
pygame.quit()