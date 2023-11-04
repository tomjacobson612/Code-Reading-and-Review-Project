import pygame

class Window():
    def __init__(self, height, width, backgroundColor, caption):
        self.height = height
        self.width = width
        self.backgroundColor = backgroundColor
        self.caption = caption
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.caption)

WINDOW = Window(1200, 1100, (251, 247, 245), 'Sudoku Solver')