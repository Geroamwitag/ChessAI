from pieces import Piece

class Pawn(Piece):
    def __init__(self, row, col, color):
        self.color = color
        if color == "white":
            image_path = "assets/wP.png"
        else:
            image_path = "assets/bP.png"
        super().__init__(row, col, color, image_path)


    def __str__(self):
        return f"{self.color} pawn"
    

    def get_valid_moves(self,):
        # depending on board orientation

        # 1 tile ahead

        # 2 tiles ahead
        pass