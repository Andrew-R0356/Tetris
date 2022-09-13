import pygame as pg
from copy import deepcopy
from os import path
from sys import exit

from config import *
from game import Game
from drawEngine import DrawEngine

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

# SHAPE FORMATS

S_shape = [['.....',
            '......',
            '..00..',
            '.00...',
            '.....'],
           ['.....',
            '..0..',
            '..00.',
            '...0.',
            '.....']]

Z_shape = [['.....',
            '.....',
            '.00..',
            '..00.',
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '.0...',
            '.....']]

I_shape = [['..0..',
            '..0..',
            '..0..',
            '..0..',
            '.....'],
           ['.....',
            '0000.',
            '.....',
            '.....',
            '.....']]

O_shape = [['.....',
            '.....',
            '.00..',
            '.00..',
            '.....']]

J_shape = [['.....',
            '.0...',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..00.',
            '..0..',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '...0.',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '.00..',
            '.....']]

L_shape = [['.....',
            '...0.',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '..00.',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '.0...',
            '.....'],
           ['.....',
            '.00..',
            '..0..',
            '..0..',
            '.....']]

T_shape = [['.....',
            '..0..',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..00.',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '..0..',
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '..0..',
            '.....']]

# index 0 - 6 represent shape
shapes = [S_shape, Z_shape, I_shape, O_shape, J_shape, L_shape, T_shape]
shape_colors = [GREEN, RED, CYAN, YELLOW, BLUE, ORANGE, PURPLE]

pg.init()

if not path.exists(filename):
    file = open(filename, 'w')
    file.write('0')
    file.close()

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Tetris')

def game_logic(win):
    locked_positions = {}  # (x, y): (0, 0, 0)
    change_piece = False
    run = True
    hold_piece = None
    can_hold = True
    lines_cleared = 0
    level = 0
    score = 0
    
    fall_time = 0
    fall_speed = 1
    clock = pg.time.Clock()

    game = Game(win, shapes, shape_colors)
    drawEng = DrawEngine(win)
    
    current_piece = game.get_shape()
    next_piece = game.get_shape()
    
    while run:
        grid = game.create_grid(locked_positions)
        
        fall_time += clock.get_rawtime()
        clock.tick()

        # Piece falling code
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (game.valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True    

        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                exit()
                 
            if event.type == pg.KEYDOWN:
                # LEFT
                if event.key == pg.K_LEFT:
                    current_piece.x -= 1
                    if not(game.valid_space(current_piece, grid)):
                        current_piece.x += 1
                        
                # RIGHT
                if event.key == pg.K_RIGHT:
                    current_piece.x += 1
                    current_piece.y += 1
                    if not(game.valid_space(current_piece, grid)):
                        current_piece.y += 1
                        current_piece.x -= 1
                        
                # UP(rotation)
                if event.key == pg.K_UP or event.key == pg.K_z:
                    current_piece.rotation += 1
                    if not(game.valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                        
                # DOWN
                if event.key == pg.K_DOWN:
                    current_piece.y += 1
                    if not(game.valid_space(current_piece, grid)):
                        current_piece.y -= 1
                        
                # HARD DROP
                if event.key == pg.K_SPACE:
                    while (game.valid_space(current_piece, grid)) and current_piece.y > 0:
                        current_piece.y += 1
                    current_piece.y -= 1
                    
                # HOLD PIECE
                if event.key == pg.K_c or event.key == pg.K_LSHIFT:
                    if can_hold:
                        if hold_piece is None:
                            hold_piece = deepcopy(current_piece)
                            current_piece = next_piece
                            next_piece = game.get_shape()
                        else:
                            t = deepcopy(hold_piece)
                            hold_piece = deepcopy(current_piece)
                            current_piece = deepcopy(t)
                            current_piece.x = 4
                            current_piece.y = 0
                        can_hold = False
                        
        shape_pos = game.convert_shape_format(current_piece)
        
        # Add color of piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:  # if not above the screen
                grid[y][x] = current_piece.color
                
        # If piece hits ground
        if change_piece:
            can_hold = True
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = game.get_shape()
            change_piece = False
            
            # Update score
            score += 20
            rows = game.clear_rows(grid, locked_positions)
            lines_cleared += rows
            if rows == 1:
                score += 100
            elif rows == 2:
                score += 300
            elif rows == 3:
                score += 500
            elif rows == 4:
                score += 800
            game.update_max_score(score)
            
        # Update level and speed
        if lines_cleared >= (level + 1) * 5:
            level += 1   
            fall_speed -= (fall_speed / 3)
            
        drawEng.draw_window(grid)
        drawEng.draw_next_shape(next_piece)
        drawEng.draw_hold_shape(hold_piece)
        drawEng.draw_score(score)
        drawEng.draw_level(level)
        drawEng.draw_max_score(game.get_max_score())
        pg.display.update()
        
        # Check the lose
        if game.check_lost(locked_positions):
            drawEng.draw_text_middle("YOU LOST", 80, WHITE)
            pg.display.update()
            pg.time.delay(1500)
            run = False
        
def main(win):
    run = True
    while run:
        win.fill(BLACK)
        drawEng = DrawEngine(win)
        drawEng.draw_text_middle('Press Any Key To Play',
                                 60,
                                 WHITE)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                game_logic(win)
    pg.quit()
    exit()
                
if __name__ == "__main__":
    main(window)