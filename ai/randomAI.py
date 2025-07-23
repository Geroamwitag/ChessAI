import random

class randomAI:
    def __init__(self, color):
        self.color = color

    def generate_move(self, board):
        pieces = []
        for row in board.pieces:
            for piece in row:
                if piece and piece.color == self.color:
                    legal_moves = board.get_legal_moves(piece)
                    if legal_moves:
                        pieces.append((piece, legal_moves))

        if not pieces:
            return None  # should be checkmate/stalemate anyway

        piece, legal_moves = random.choice(pieces)
        move = random.choice(legal_moves)

        return piece, move  # piece, (row, col)
