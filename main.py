import pygame
from board import Board
from ai import randomAI, MinimaxAI

pygame.init()
pygame.display.set_caption("Chess")
icon = pygame.image.load("assets/bQ.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

board = Board()
board.ai_color = "black"
ai = randomAI(board.ai_color)
board.vs_ai = True

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
        # handle clicks on the reset and quit buttons
        if board.game_over and event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if board.play_again_rect and board.play_again_rect.collidepoint(pos):
                board.reset()
            elif board.quit_rect and board.quit_rect.collidepoint(pos):
                running = False


    screen.fill((255, 255, 255))

    # draw board
    board.draw(screen)

    if board.game_over:
        board.draw_game_over_popup(screen)

    # cleanest way to draw the game every frame
    pygame.display.flip()

    # ai move
    if (
        not board.game_over
        and board.turn_color == ai.color
    ):
        piece, move = ai.generate_move(board)
        if piece and move:
            board.move_piece(piece, move[0], move[1])
        board.waiting_for_ai = False

    # game fps
    clock.tick(60)
pygame.quit()