from pieces import Piece

class Knight(Piece):
    def __init__(self, row, col, color):
        self.color = color
        if color == "white":
            image_path = "assets/wN.png"
        else:
            image_path = "assets/bN.png"
        super().__init__(row, col, color, image_path)


    def __str__(self):
        return f"{self.color} knight"
    

    def get_valid_moves(self, board, for_attack=False):
        moves = []
        directions = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            ( 1, -2), ( 1, 2), ( 2, -1), ( 2, 1)
        ]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < board.rows and 0 <= c < board.cols:
                target = board.pieces[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves

