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


    def __getstate__(self):
        state = self.__dict__.copy()
        # images don’t matter for copies
        # important when checking for king check
        state['image'] = None  
        return state

        
    def get_valid_moves(self, board):
        # if piece has no get_valid_moves method, default to allowing all moves except for tiles with same color
        valid_moves = []
        for r in range(board.rows):
            for c in range(board.cols):
                # if tile is empty, or the tile has a piece with the oposite color
                if board.pieces[r][c] is None or board.pieces[r][c].color != self.color:
                    valid_moves.append((r, c))
        return valid_moves
    

    def draw(self, screen, tile_size):
        # piece position
        x = self.col * tile_size
        y = self.row * tile_size

        # take the piece’s image and draw it at position (x, y) with offset to center on the main screen.
        offset_x = (tile_size - self.image_size) // 2 # mid point x
        offset_y = (tile_size - self.image_size) // 2 # mid point y
        screen.blit(self.image, (x + offset_x, y + offset_y))
