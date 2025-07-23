from pieces import Piece, Rook

class King(Piece):
    def __init__(self, row, col, color):
        self.color = color
        self.has_moved = False
        if color == "white":
            image_path = "assets/wK.png"
        else:
            image_path = "assets/bK.png"
        super().__init__(row, col, color, image_path, name="king")


    def get_valid_moves(self, board, for_attack=False):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)
        ]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < board.rows and 0 <= c < board.cols:
                target = board.pieces[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))

        if for_attack:
            return moves

        # castling
        if not self.has_moved and not board.is_in_check(self.color):
            row = self.row
            # kingside
            kingside_rook = board.pieces[row][7]
            if (isinstance(kingside_rook, Rook)
                and not kingside_rook.has_moved
                and board.pieces[row][5] is None
                and board.pieces[row][6] is None):
                # must not pass through check
                if board.is_safe_for_castling(self, [(row, 5), (row, 6)]):
                    moves.append((row, 6))  # Kingside castling target

            # queenside
            queenside_rook = board.pieces[row][0]
            if (isinstance(queenside_rook, Rook)
                and not queenside_rook.has_moved
                and board.pieces[row][1] is None
                and board.pieces[row][2] is None
                and board.pieces[row][3] is None):
                if board.is_safe_for_castling(self, [(row, 2), (row, 3)]):
                    moves.append((row, 2))  # Queenside castling target

        return moves

