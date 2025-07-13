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

