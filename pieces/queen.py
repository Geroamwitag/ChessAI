from pieces import Piece

class Queen(Piece):
    def __init__(self, row, col, color):
        self.color = color
        if color == "white":
            image_path = "assets/wQ.png"
        else:
            image_path = "assets/bQ.png"
        super().__init__(row, col, color, image_path, name="queen")
    

    def get_valid_moves(self, board, for_attack=False):
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),   # rook directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # bishop directions
        ]

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
                        break # first enemy
                    else:
                        break # first ally
                else:
                    break
        return moves
