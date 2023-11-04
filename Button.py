import pygame
from Window import WINDOW

class ButtonRectangular():
    def __init__(self, x, y, icon):
        self.icon = icon
        self.rectangle = self.icon.get_rect()
        self.rectangle.topleft = (x, y)
        self.pressedByUser = False

    def draw(self):
        WINDOW.screen.blit(self.icon, (self.rectangle.x, self.rectangle.y))
    
    def buttonPress(self):
        action = False
        mousePosition = pygame.mouse.get_pos()

        if self.rectangle.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0] == 1 and self.pressedByUser == False:
                self.pressedByUser = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.pressedByUser = False
        return action