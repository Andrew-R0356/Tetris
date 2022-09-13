import pygame as pg
from config import *

class DrawEngine():
    def __init__(self, window):
        self.surface = window
        
    def draw_text_middle(self, text, t_size, color):
        font = pg.font.Font(fontname, t_size, bold=True)
        label = font.render(text, 1, color)
        label_rect = label.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.surface.blit(label, label_rect)

    def draw_window(self, grid):
        self.surface.fill(BLACK)
        pg.font.init()
        
        # Tetris
        font = pg.font.Font('EvilEmpire-4BBVK.ttf', 60)
        label = font.render('Tetris', 1, WHITE)
        self.surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pg.draw.rect(self.surface, grid[i][j], (TOP_LEFT_X + j * SIZE,
                                                        TOP_LEFT_Y + i * SIZE,
                                                        SIZE, 
                                                        SIZE), 0)
        
        # Grid
        self.draw_grid(grid)
        
        # Border
        pg.draw.rect(self.surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 2)
        
    def draw_grid(self, grid):
        x = TOP_LEFT_X
        y = TOP_LEFT_Y
        
        for i in range(len(grid)):
            pg.draw.line(self.surface,
                         GREY,
                         (x, y + i * SIZE),
                         (x + PLAY_WIDTH, y + i * SIZE))
            for j in range(len(grid[i])):
                pg.draw.line(self.surface,
                             GREY,
                             (x + j * SIZE, y),
                             (x + j * SIZE, y + PLAY_HEIGHT))
    
    def draw_next_shape(self, shape):
        font = pg.font.Font(fontname, 30)
        label = font.render('Next Shape', 1, WHITE)
        x = TOP_LEFT_X + PLAY_WIDTH + 50
        y = TOP_LEFT_Y + 30
        format_shape = shape.shape[shape.rotation % len(shape.shape)]
        
        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pg.draw.rect(self.surface, shape.color, (x + j * SIZE,
                                                             y + i * SIZE,
                                                             SIZE, 
                                                             SIZE), 0)
        self.surface.blit(label, (x + 20, y - 30))
        
    def draw_hold_shape(self, shape):
        font = pg.font.Font(fontname, 30)
        label = font.render('Hold', 1, WHITE)
        x = 50
        y = TOP_LEFT_Y + 30
        
        if shape is not None:
            format_shape = shape.shape[shape.rotation % len(shape.shape)]
            
            for i, line in enumerate(format_shape):
                row = list(line)
                for j, column in enumerate(row):
                    if column == '0':
                        pg.draw.rect(self.surface, shape.color, (x + j * SIZE,
                                                                y + i * SIZE, 
                                                                SIZE,
                                                                SIZE), 0)
        self.surface.blit(label, (x + 50, y - 30))
                        
    def draw_score(self, score):
        font = pg.font.Font(fontname, 30)
        label = font.render("Score", 1, WHITE)
        score_text = font.render(str(score), 1, WHITE)
        x = 20
        y = TOP_LEFT_Y + 200
        
        self.surface.blit(label, (x, y))
        self.surface.blit(score_text, (x + 90, y))
        
    def draw_level(self, level):
        font = pg.font.Font(fontname, 30)
        label = font.render("Level", 1, WHITE)
        level_text = font.render(str(level), 1, WHITE)
        x = 20
        y = TOP_LEFT_Y + 250
        
        self.surface.blit(label, (x, y))
        self.surface.blit(level_text, (x + 90, y))
        
    def draw_max_score(self, score):
        font = pg.font.Font(fontname, 30)
        label = font.render("Max score", 1, WHITE)
        max_score_text = font.render(str(score), 1, WHITE)
        x = 20
        y = TOP_LEFT_Y + 300
        
        self.surface.blit(label, (x, y))
        self.surface.blit(max_score_text, (x + 140, y))
        