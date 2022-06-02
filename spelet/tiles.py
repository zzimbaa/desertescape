import pygame
from .settings import Settings

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(img, (Settings.TILE_SIZE, Settings.TILE_SIZE))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.og = x

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(img_path)
        self.image = pygame.transform.scale(img, (Settings.TILE_SIZE // 2, Settings.TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.og = x

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(img_path)
        self.image = pygame.transform.scale(img, (Settings.TILE_SIZE * 4, Settings.TILE_SIZE * 4))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.og = x

class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(img_path)
        self.image = pygame.transform.scale(img, (Settings.TILE_SIZE *4, Settings.TILE_SIZE *3))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.og = x

class Healthpotion(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(img_path)
        self.image = pygame.transform.scale(img, (Settings.TILE_SIZE // 2, Settings.TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.og = x

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(img_path)
        self.image = pygame.transform.scale(img, (Settings.TILE_SIZE , Settings.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.og = x

class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(img_path)
        self.image = pygame.transform.scale(img, (Settings.TILE_SIZE *3, int(Settings.TILE_SIZE * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.og = x