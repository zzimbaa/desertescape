import pygame
from .settings import Settings

class Button():
    def __init__(self, screen, x, y, img_path):
        self.screen = screen
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        action = False

        #mouse position
        pos = pygame.mouse.get_pos()

        #mouseover and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.screen.blit(self.image, self.rect)
        return action

class ScreenFade():
    def __init__(self, screen, direction, colour, speed):
        self.screen = screen
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
    
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:#vertical screen fade down
            pygame.draw.rect(self.screen, self.colour, (0, 0, Settings.SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= Settings.SCREEN_WIDTH:
            fade_complete = True

        return fade_complete