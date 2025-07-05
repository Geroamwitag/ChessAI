import pygame
from board import Board

WIDTH, HEIGHT = 800, 800

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = Board()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle clicks, moves, etc.

            self.board.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
