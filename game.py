from random import shuffle

from piece import Piece
from config import *

class Game():
    bag = []
    
    def __init__(self, window, shapes, shape_colors):
        self.win = window
        self.shapes = shapes
        self.shape_colors = shape_colors
        
    def get_shape(self):
        return Piece(4, 1, self.get_random_piece(), self.shapes, self.shape_colors)

    def create_grid(self, locked_pos={}):
        grid = [[BLACK for _ in range(10)] for _ in range(20)]   
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j, i)]
                    grid[i][j] = c
                    
        return grid 
    
    def valid_space(self, shape, grid):
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        
        formatted = self.convert_shape_format(shape)
        
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        
        return True
        
    def convert_shape_format(self, shape):
        positions = []
        shape_format = shape.shape[shape.rotation % len(shape.shape)]  # rotation of all shape formats
        
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
                    
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)  # to start falling out of the game screen     
            
        return positions
    
    def clear_rows(self, grid, locked):
        # Delering rows
        inc = 0  # how many rows to be shifted down by
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            if BLACK not in row:
                inc += 1
                index = i  # from which position to shift
                for j in range(len(row)):
                    try: 
                        del locked[(j, i)]
                    except Exception:
                        continue
        
        # Shifting
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < index:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
        
        return inc
                    
    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        
        return False
    
    def get_random_piece(self):
        cls = self.__class__
        
        if len(cls.bag) == 0:
            cls.bag = self.shapes[:]
            shuffle(cls.bag)
        
        return cls.bag.pop()
        
    def update_max_score(self, score):            
        max_score = int(self.get_max_score())
        
        with open(filename, 'w') as file:
            if score > max_score:
                file.write(str(score))
            else:
                file.write(str(max_score))
                
    def get_max_score(self):
        with open(filename, 'r') as file:
            score = file.readline().strip()
        
        return score
        
        
        
                    
            
        