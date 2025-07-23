from pieces import Piece

class Pawn(Piece):
    def __init__(self, row, col, color):
        self.color = color
        if color == "white":
            image_path = "assets/wP.png"
        else:
            image_path = "assets/bP.png"
        super().__init__(row, col, color, image_path, name="pawn")

    
    def get_valid_moves(self, board, for_attack=False):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # one square forward
        one_step_row = self.row + direction
        if 0 <= one_step_row < board.rows and board.pieces[one_step_row][self.col] is None:
            moves.append((one_step_row, self.col))

            # Two squares forward from starting row
            two_step_row = self.row + 2 * direction
            if self.row == start_row and board.pieces[two_step_row][self.col] is None:
                moves.append((two_step_row, self.col))

        # diagonal captures
        if 0 <= one_step_row < board.rows:
            for dc in [-1, 1]:
                new_col = self.col + dc
                if 0 <= new_col < board.cols:
                    target = board.pieces[one_step_row][new_col]
                    if target and target.color != self.color:
                        moves.append((one_step_row, new_col))

        # en passant capture
        for dc in [-1, 1]:
            r, c = self.row, self.col + dc
            if 0 <= c < board.cols and board.en_passant_target:
                target_row, target_col = board.en_passant_target
                if (target_row, target_col) == (self.row + direction, c):
                    target_pawn = board.pieces[self.row][c]
                    if (
                        isinstance(target_pawn, Pawn) and
                        target_pawn.color != self.color
                    ):
                        moves.append((target_row, target_col))
        return moves
