from pieces import Piece

class Queen(Piece):
    def __init__(self, row, col, color):
        self.color = color
        if color == "white":
            image_path = "assets/wQ.png"
        else:
            image_path = "assets/bQ.png"
        super().__init__(row, col, color, image_path)


    def __str__(self):
        return f"{self.color} queen"


    def get_valid_moves(self,):
        # Return list of valid positions for the queen
        pass