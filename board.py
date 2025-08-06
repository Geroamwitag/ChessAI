from pieces import *
from copy import deepcopy
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
        self.simulating = True
        
        self.pieces = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.setup_pieces()
        self.turn_color = "white"
        self.undo = False
        self.vs_ai = False
        self.ai_color = "white"

        self.game_over = False
        self.game_result = None
        self.play_again_rect = None
        self.quit_rect = None


    def reset(self):
        self.__init__()


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
        if self.game_over:
            return
        
        x,y = pos # exact co. of click

        # clever method to get the row and col of the pos
        row = y // self.tile_size
        col = x // self.tile_size
       
        if self.selected_piece and self.selected_piece.color == self.turn_color:
            # second click
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, row, col)

            # deselect after any second click
            self.selected_piece = None
            self.valid_moves = []

        else:
            # first click
            piece = self.pieces[row][col]
            
            if piece and piece.color == self.turn_color: 
                self.selected_piece = piece
                self.valid_moves = self.get_legal_moves(piece)
                print(f"selected {self.selected_piece} at {self.selected_piece.row}, {self.selected_piece.col}")
            else:
                print("no piece selected")


    def is_in_check(self, color):
        # find king
        king = None
        for row in self.pieces:
            for piece in row:
                if piece and isinstance(piece, King) and piece.color == color:
                    king = piece
                    break

        # check if the king tile is in the pieces validmoves                
        for row in self.pieces:
            for piece in row:
                if piece and piece.color != color:
                    if (king.row, king.col) in piece.get_valid_moves(self, for_attack=True):
                        return True
        return False
    

    def is_safe_for_castling(self, king, squares):
        for r, c in squares:
            # make a copy and check if king would be in check at each square
            board_copy = deepcopy(self)
            board_copy.pieces[king.row][king.col] = None
            board_copy.pieces[r][c] = king
            if board_copy.is_in_check(king.color):
                return False
        return True


    def get_legal_moves(self, piece):
        legal_moves = []
        # test all moves in valid moves
        for move in piece.get_valid_moves(self):
            # copy current board
            board_copy = deepcopy(self)
            board_copy.move_piece(board_copy.pieces[piece.row][piece.col], move[0], move[1], is_simulation=True)
            # if a next move would leave the king in check do not allow that move
            if not board_copy.is_in_check(piece.color):
                legal_moves.append(move)
        return legal_moves


    def get_all_legal_moves(self, color):
        moves = []
        for row in self.pieces:
            for piece in row:
                if piece and piece.color == color:
                    legal_moves = self.get_legal_moves(piece)
                    if legal_moves:
                        moves.append((piece, legal_moves))
        return moves


    def get_piece_at(self, row, col):
        return self.pieces[row][col] 


    def move_piece(self, piece, new_row, new_col, is_simulation=False):
        current_row = piece.row
        current_col = piece.col

        is_en_passant = False
        # the captured piece if any
        captured = self.pieces[new_row][new_col]

        # promote if applicable
        promotion = False
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and new_row == 0) or \
            (piece.color == 'black' and new_row == 7):
                promotion = True

        # en passant
        if isinstance(piece, Pawn):
            if self.en_passant_target == (new_row, new_col) and captured is None:
                is_en_passant = True
                # the captured pawn is behind the target square
                captured_pawn_row = new_row + (1 if piece.color == 'white' else -1)
                captured = self.pieces[captured_pawn_row][new_col]


        # check if a rook or king moved for castling
        if isinstance(piece, (King, Rook)):
            piece.has_moved = True

        # detect castling
        if isinstance(piece, King) and abs(new_col - piece.col) == 2:
            row = piece.row
            if new_col == 6:  # Kingside
                rook = self.pieces[row][7]
                self.pieces[row][5] = rook
                self.pieces[row][7] = None
                rook.col = 5
                rook.has_moved = True
            elif new_col == 2:  # Queenside
                rook = self.pieces[row][0]
                self.pieces[row][3] = rook
                self.pieces[row][0] = None
                rook.col = 3
                rook.has_moved = True

        # create Move record
        move = Move(piece, (piece.row, piece.col), (new_row, new_col), captured, is_en_passant=is_en_passant)
        self.move_history.append(move)

        # remove piece from current position
        self.pieces[current_row][current_col] = None

        # if en passant, remove captured pawn
        if is_en_passant:
            self.pieces[captured_pawn_row][new_col] = None

        # move piece to next pos
        piece.row = new_row
        piece.col = new_col
        self.pieces[new_row][new_col] = piece
        if not is_simulation:
            print(f"{piece} to {piece.row}, {piece.col}")

        # set new en passant target, ONLY if pawn just moved two squares
        if isinstance(piece, Pawn):
            if abs(new_row - current_row) == 2:
                dir = -1 if piece.color == 'white' else 1
                self.en_passant_target = (new_row - dir, new_col)
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None

        if not is_simulation:
            self.turn_color = "black" if self.turn_color == "white" else "white"
            print(f"turn: {self.turn_color}")
        if promotion: # and not is_simulation
            self.pieces[new_row][new_col] = Queen(new_row, new_col, piece.color)

        if not is_simulation:
            self.check_game_state()

    
    def undo_move(self):
        if not self.move_history:
            return
        
        self._undo_last_move()

        if self.vs_ai:
            if self.move_history:
                self._undo_last_move()
        
        
    def _undo_last_move(self):
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


    def check_game_state(self):
        in_check = self.is_in_check(self.turn_color)
        has_moves = False

        for row in self.pieces:
            for piece in row:
                if piece and piece.color == self.turn_color:
                    if self.get_legal_moves(piece):  # Use your legal moves method!
                        has_moves = True
                        break
            if has_moves:
                break

        if not has_moves:
            if in_check:
                self.game_over = True
                self.game_result = f"Checkmate! {'White' if self.turn_color == 'black' else 'Black'} wins!"
                print(self.game_result)
            else:
                self.game_over = True
                self.game_result = "Stalemate! It's a draw."
                print(self.game_result)


    def draw_game_over_popup(self, screen):
        width, height = screen.get_size()

        # draw semi-transparent overlay
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)  # 0=transparent, 255=opaque
        overlay.fill((0, 0, 0))  # black overlay
        screen.blit(overlay, (0, 0))

        # popup box
        box_width, box_height = 300, 200
        box_x = (width - box_width) // 2
        box_y = (height - box_height) // 2
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 4)  # Border

        # texts on pop up
        font = pygame.font.SysFont(None, 36)
        text = f"{self.game_result}"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(width // 2, box_y + 60))
        screen.blit(text_surface, text_rect)

        # buttons
        button_font = pygame.font.SysFont(None, 28)

        self.play_again_rect = pygame.Rect(box_x + 40, box_y + 120, 100, 40)
        self.quit_rect = pygame.Rect(box_x + 160, box_y + 120, 100, 40)

        pygame.draw.rect(screen, (0, 200, 0), self.play_again_rect)
        pygame.draw.rect(screen, (200, 0, 0), self.quit_rect)

        play_again_text = button_font.render("Play Again", True, (255, 255, 255))
        quit_text = button_font.render("Quit", True, (255, 255, 255))

        # overlay buttoms and texts onto the screen
        screen.blit(play_again_text, play_again_text.get_rect(center=self.play_again_rect.center))
        screen.blit(quit_text, quit_text.get_rect(center=self.quit_rect.center))


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

    def copy(self):
        copied_board = deepcopy(self)
        return copied_board



class Move:
    def __init__(self, piece, start_pos, end_pos, captured=None, is_en_passant=False, is_castling=False):
        self.piece = piece
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.captured = captured
        self.is_en_passant = is_en_passant
        self.is_castling = is_castling