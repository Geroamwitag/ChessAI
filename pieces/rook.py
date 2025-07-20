from pieces import Piece

class Rook(Piece):
    def __init__(self, row, col, color):
        self.color = color
        self.has_moved = False
        if color == "white":
            image_path = "assets/wR.png"
        else:
            image_path = "assets/bR.png"
        super().__init__(row, col, color, image_path)


    def __str__(self):
        return f"{self.color} rook"


    def get_valid_moves(self, board, for_attack=False):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row, self.col
            while True:
                r += dr
                c += dc
                if 0 <= r < board.rows and 0 <= c < board.cols:
                    target = board.pieces[r][c]
                    if target is None:
                        moves.append((r, c))
                    elif target.color != self.color:
                        moves.append((r, c))
                        break  # stop at first enemy piece.
                    else:
                        break  # stop at friendly piece.
                else:
                    break  # out of bounds.
        return moves