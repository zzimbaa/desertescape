



tilesize = 200

class World():
    def__init__(self, data):
        self.tile_list = []

       iceblock_img = pygame.image.load("E:/dev/platformerspelTest/bilder/iceblockdark.jpg")

       for row in data():
           for tile in row:
               col_count = 0
               if tile == 1:
                   img = pygame.transforme.scale(iceblock_img, (tilesize, tilesize))
                   img=rect = img.get_rect()
                   img_rect.x = col_count * tilesize
                   img_rect.y = row_count * tilesize
                   self.tile_list.append(tile)
                col_count += 1
            row_count += 1

world_data = [
[1, 1, 1, 1, 1],
[1, 0, 0, 0, 1],
[1, 0, 0, 0, 1],
[1, 0, 0, 0, 1]
[1, 1, 1, 1, 1]
]

world = World(world_data)

print(world.title_list)
