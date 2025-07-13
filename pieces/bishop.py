from pieces import Piece

class Bishop(Piece):
    def __init__(self, row, col, color):
        self.color = color
        if color == "white":
            image_path = "assets/wB.png"
        else:
            image_path = "assets/bB.png"
        super().__init__(row, col, color, image_path)


    def __str__(self):
        return f"{self.color} bishop"


    def get_valid_moves(self,):
        # Return list of valid positions for the bishop
        pass