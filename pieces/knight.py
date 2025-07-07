from pieces import Piece

class Knight(Piece):
    def __init__(self, row, col, color):
        if color == "white":
            image_path = "assets/wN.png"
        else:
            image_path = "assets/bN.png"
        super().__init__(row, col, color, image_path)


    def get_valid_moves(self,):
        # Return list of valid positions for the knight
        pass