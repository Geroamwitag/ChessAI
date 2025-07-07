import pygame

class Piece:
    def __init__(self, row, col, color, image):
        self.row = row
        self.col = col
        self.color = color

        # load piece image and resize
        self.image = pygame.image.load(image)
        self.image_size = 60
        self.image = pygame.transform.scale(self.image, (self.image_size, self.image_size)) # 80x80 is a tile size


    def get_valid_moves(self, board):
        return []
    

    def draw(self, screen, tile_size):
        # piece position
        x = self.col * tile_size
        y = self.row * tile_size

        # take the piece’s image and draw it at position (x, y) with offset to center on the main screen.
        offset_x = (tile_size - self.image_size) // 2 # mid point x
        offset_y = (tile_size - self.image_size) // 2 # mid point y
        screen.blit(self.image, (x + offset_x, y + offset_y))
