from pieces import *
import pygame


class Board:
    def __init__(self):
        self.tile_size = 80
        self.rows = 8
        self.cols = 8
        self.selected_piece = None
        
        # empty "chess board" 2D list to manage piece locations
        self.pieces = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.setup_pieces()


    def setup_pieces(self):
        # Pawns
        for col in range(self.cols):
            self.pieces[1][col] = Pawn(1, col, "black")
            self.pieces[6][col] = Pawn(6, col, "white")

        # Rooks
        self.pieces[0][0] = Rook(0, 0, "black")
        self.pieces[0][7] = Rook(0, 7, "black")
        self.pieces[7][0] = Rook(7, 0, "white")
        self.pieces[7][7] = Rook(7, 7, "white")

        # Knights
        self.pieces[0][1] = Knight(0, 1, "black")
        self.pieces[0][6] = Knight(0, 6, "black")
        self.pieces[7][1] = Knight(7, 1, "white")
        self.pieces[7][6] = Knight(7, 6, "white")

        # Bishops
        self.pieces[0][2] = Bishop(0, 2, "black")
        self.pieces[0][5] = Bishop(0, 5, "black")
        self.pieces[7][2] = Bishop(7, 2, "white")
        self.pieces[7][5] = Bishop(7, 5, "white")

        # Queens
        self.pieces[0][3] = Queen(0, 3, "black")
        self.pieces[7][3] = Queen(7, 3, "white")

        # Kings
        self.pieces[0][4] = King(0, 4, "black")
        self.pieces[7][4] = King(7, 4, "white")


    def handle_click(self, pos):
        x,y = pos # exact co. of click

        # clever method to get the row and col of the pos
        row = y // self.tile_size
        col = x // self.tile_size
       
        if self.selected_piece:
            # second click
            self.move_piece(self.selected_piece, row, col)
        else:
            # first click
            piece = self.pieces[row][col]
            
            if piece: 
                self.selected_piece = piece
                print(f"selected {self.selected_piece} at {self.selected_piece.row}, {self.selected_piece.col}")
            else:
                print("no piece selected") 

    
    def move_piece(self, piece, row, col):
        current_row = piece.row
        current_col = piece.col

        # remove piece from current position
        self.pieces[current_row][current_col] = None

        # move piece to next pos
        piece.row = row
        piece.col = col
        self.pieces[row][col] = piece
        print(f"{piece} to {piece.row}, {piece.col}")

        # revert selected piece to none
        self.selected_piece = None
        pass


    def draw(self, screen):
        tile_color_1 = (238, 238, 210) # light, pale beige
        tile_color_2 = (118, 150, 86)  # dark, darkish green
        colors = [tile_color_1, tile_color_2]

        # draw board
        for row in range(self.rows):
            for col in range(self.cols):
                # use a boolean to select the color of the tile.
                # if (row + col), the index of the tile, is even. select color index 1, True
                # if it is not even select color index 0, False
                color = colors[(row + col) % 2]

                # draw a rectangle as a tile
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(col * self.tile_size,  # X pos
                                row * self.tile_size,  # Y pos
                                self.tile_size,        # Width
                                self.tile_size         # Height
                                )
                )

        # draw pieces
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.pieces[row][col]
                if piece is not None:
                    piece.draw(screen, self.tile_size)
