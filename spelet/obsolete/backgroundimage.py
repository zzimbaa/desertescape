import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode([1000,1000])

keep_going = True
pic = pygame.image.load("C:/dev/platformerspelTest/bilder/glaciärbild1000.jpg")


tilesize = 200

# alla olika block
class World():
    def __init__(self, data):
        self.tile_list = []

        iceblock_img = pygame.image.load("C:/dev/platformerspelTest/bilder/iceblockdark.jpg")
        clearice_img = pygame.image.load("C:/dev/platformerspelTest/bilder/icemine.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                   img = pygame.transform.scale(clearice_img, (tilesize, tilesize))
                   img_rect = img.get_rect()
                   img_rect.x = col_count * tilesize
                   img_rect.y = row_count * tilesize
                   tile = (img, img_rect)
                   self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(iceblock_img, (tilesize, tilesize))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tilesize
                    img_rect.y = row_count * tilesize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
        
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
[1, 1, 1, 1, 1],
[0, 0, 0, 0, 1],
[1, 0, 0, 0, 1],
[1, 0, 0, 0, 1],
[1, 2, 2, 2, 1],
]

world = World(world_data)

print(world.tile_list)

while keep_going:

    screen.blit(pic, (0,0))
    world.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False

    pygame.display.update()

pygame.quit()