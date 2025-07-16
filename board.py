from pieces import *
import pygame


class Board:
    def __init__(self):
        self.tile_size = 80
        self.rows = 8
        self.cols = 8

        self.selected_piece = None
        self.valid_moves = []
        self.move_history = []
        self.en_passant_target = None
        
        self.pieces = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.setup_pieces()
        self.turn_color = "white"

        
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
       
        if self.selected_piece and self.selected_piece.color == self.turn_color:
            # second click
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, row, col)
                print(f"turn: {self.turn_color}")


            # deselect after any second click
            self.selected_piece = None
            self.valid_moves = []

        else:
            # first click
            piece = self.pieces[row][col]
            
            if piece and piece.color == self.turn_color: 
                self.selected_piece = piece
                self.valid_moves = piece.get_valid_moves(self)
                print(f"selected {self.selected_piece} at {self.selected_piece.row}, {self.selected_piece.col}")
            else:
                print("no piece selected") 

    
    def move_piece(self, piece, new_row, new_col):
        current_row = piece.row
        current_col = piece.col

        # move details
        captured = self.pieces[new_row][new_col] # None if no piece at index
        move = Move(piece, (piece.row, piece.col), (new_row, new_col), captured)
        self.move_history.append(move)

        # remove piece from current position
        self.pieces[current_row][current_col] = None

        # move piece to next pos
        piece.row = new_row
        piece.col = new_col
        self.pieces[new_row][new_col] = piece
        print(f"{piece} to {piece.row}, {piece.col}")

        # if a pawn moves 2 squares, set en passant target to the tile behind the pawn
        if isinstance(piece, Pawn):
            # if old row and new row difference is 2
            if abs(new_row - piece.row) == 2:
                # store square behind pawn as en passant target, direction depends on piece color
                dir = 1 if piece.color == 'white' else -1
                self.en_passant_target = (new_row - dir, new_col)
            # if pawn moves once remove en passant target
            else:
                self.en_passant_target = None
        # if any other piece moves remove en passant target
        else:
            self.en_passant_target = None

        # revert selected piece to none
        self.selected_piece = None
        self.turn_color = "black" if self.turn_color == "white" else "white"
    

    def undo_move(self):
        if not self.move_history:
            return

        move = self.move_history.pop() # .pop removes last index by default
        piece = move.piece

        # restore piece to original square
        self.pieces[piece.row][piece.col] = None
        self.pieces[move.start_pos[0]][move.start_pos[1]] = piece

        piece.row, piece.col = move.start_pos

        # restore captured piece if any
        if move.captured:
            self.pieces[move.end_pos[0]][move.end_pos[1]] = move.captured

        # switch turn
        self.turn_color = 'black' if self.turn_color == 'white' else 'white'


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

        # draw selected piece highlights, highlight the piece and its valid moves
        if self.selected_piece:
            highlight_color = (255, 255, 0, 100)  # yellowish
            surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            surf.fill(highlight_color)
            row, col = self.selected_piece.row, self.selected_piece.col
            screen.blit(surf, (col * self.tile_size, row * self.tile_size))


        # highlight valid moves
        for move in self.valid_moves:
            r, c = move
            surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            surf.fill((0, 255, 0, 100))  # greenish
            screen.blit(surf, (c * self.tile_size, r * self.tile_size))


        # draw pieces
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.pieces[row][col]
                if piece is not None:
                    piece.draw(screen, self.tile_size)


class Move:
    def __init__(self, piece, start_pos, end_pos, captured=None, is_en_passant=False, is_castling=False):
        self.piece = piece
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.captured = captured
        self.is_en_passant = is_en_passant
        self.is_castling = is_castling