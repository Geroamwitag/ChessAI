from pieces import Piece

class King(Piece):
    def __init__(self, row, col, color):
        self.color = color
        if color == "white":
            image_path = "assets/wK.png"
        else:
            image_path = "assets/bK.png"
        super().__init__(row, col, color, image_path)


    def __str__(self):
        return f"{self.color} king"


    def get_valid_moves(self, board):
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
        return moves

