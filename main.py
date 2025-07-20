import pygame
from board import Board

pygame.init()
pygame.display.set_caption("Chess")
icon = pygame.image.load("assets/bQ.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

board = Board()

# game loop
running = True
while running:  

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False
        # handling tile clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos() # x,y co. of click
            board.handle_click(pos)
        # undo last move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_BACKSPACE:  # If 'Z' key is pressed
                board.undo_move()

    screen.fill((255, 255, 255))

    # draw board
    board.draw(screen)

    # cleanest way to draw the game every frame
    pygame.display.flip()

    # game fps
    clock.tick(60)
pygame.quit()