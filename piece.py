class Piece(object):
    def __init__(self, x, y, shape, shapes, shape_colors):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        
    