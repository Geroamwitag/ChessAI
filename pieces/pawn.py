from pieces import Piece

class Pawn(Piece):
    def __init__(self, row, col, color):
        if color == "white":
            image_path = "assets/wP.png"
        else:
            image_path = "assets/bP.png"
        super().__init__(row, col, color, image_path)


    def get_valid_moves(self,):
        # Return list of valid positions for the pawn
        pass