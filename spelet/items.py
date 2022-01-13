import pygame
from settings import Settings
from character import Character

# class Itembox(pygame.sprite.Sprite):

#     def __init__(self, item_type, x, y, scale):
#         pygame.sprite.Sprite.__init__(self)

#         heal_img = pygame.image.load(f"bilder/items/healpotionblue.png").convert_alpha()
#         heal_img = pygame.transform.scale(heal_img, (Settings.HEALPOTION_WIDTH*scale, Settings.HEALPOTION_HEIGHT*scale))

#         coin_img = pygame.image.load(f"bilder/items/coingold.png").convert_alpha()
#         coin_img = pygame.transform.scale(coin_img, (Settings.COIN_WIDTH*scale, Settings.COIN_HEIGHT*scale))

#         item_boxes_group = pygame.sprite.Group()

#         item_boxes = {
#             "Health" : heal_img,
#             "Score" : coin_img
#         }

#         #self.screen = screen
#         self.item_type = item_type
#         self.scale = scale
#         self.image = item_boxes[self.item_type]
#         self.rect = self.image.get_rect()
#         self.rect.midtop = (x + Settings.TILE_SIZE, y + (Settings.TILE_SIZE - self.image.get_height()))
    
#     # def update(self):
#         # #kolla om tagit upp item
#         # if pygame.sprite.collide_rect(self, player):
#         #     #typ av item
#         #     if self.item_type == "Health":
#         #         player.health += 25
#         #         if player.health > player.max_health:
#         #             player.health = player.max_health
#         #     elif self.item_type == "Score":
#         #         player.score += 1


